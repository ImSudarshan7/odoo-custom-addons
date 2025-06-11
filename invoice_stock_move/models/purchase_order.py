from odoo.exceptions import UserError
from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    picking_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="Picking Status", compute='_compute_picking_state', store=True )

    @api.depends('picking_ids.state')
    def _compute_picking_state(self):
        for order in self:
            pickings = order.picking_ids
            if pickings:
                if all(picking.state == 'done' for picking in pickings):
                    order.picking_state = 'done'
                else:
                    latest_picking = max(
                        (picking for picking in pickings if picking.state != 'done'),
                        key=lambda p: p.scheduled_date,
                        default=None
                    )
                    order.picking_state = latest_picking.state if latest_picking else 'done'
            else:
                order.picking_state = None
                
    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        picking = self.picking_ids.filtered(lambda p: p.state == 'done')[:1]
        if picking:
            invoice_vals.update({
                'ref': picking.challan_no or self.partner_ref or '',
                'invoice_date': picking.challan_date or fields.Date.today(),
            })
        return invoice_vals