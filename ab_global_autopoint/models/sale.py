from odoo import models, fields, api, _
from odoo.exceptions import UserError
# from nepali_datetime import date as nepali_date
# from pytz import timezone

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    # transfer_id= fields.Many2one('stock.picking', string='Add Transfer ID', help='When selected, the associated transfer lines are added to the Sale Order Line.',
    #                              readonly=True, states={'draft': [('readonly', False)]})
    # requisition_id = fields.Many2one('requisition.form', string='Add Requisition Order',
    #                                  help='Encoding help. When selected, the associated requisition form lines are added to the sale order.')
    job_card_no = fields.Many2one('job.order', string='JOB CARD NO.', readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  copy=True, required=0, track_visibility='onchange')

    vehicle_num = fields.Many2one('vehicle.create', string='Vehicle Number', readonly=True,
                                  states={'draft': [('readonly', False)]},
                                  copy=True, required=0, track_visibility='onchange')
    state_1 = fields.Selection([('validator', 'Validator')])
    # delivery_set = fields.Boolean()
    # is_all_service = fields.Boolean()

    # def get_nepali_date(self, dt):
    #     # Convert to Kathmandu timezone first
    #     if dt:
    #         kathmandu_tz = timezone('Asia/Kathmandu')
    #         dt_local = dt.astimezone(kathmandu_tz)
    #         ad_date = dt_local.date()
    #         nep_date = nepali_date.from_datetime_date(ad_date)
    #         return f"{nep_date.year}-{nep_date.month:02d}-{nep_date.day:02d} (B.S.)"
    #     return ''

    def button_validator1(self):
        self.state_1 = 'validator'
        self.write({'state': 'sent'})

    @api.model
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'ab_global_autopoint.report_quotation')

    @api.onchange('partner_id')
    def onchange_partner_id_vehicle_num(self):
        for rec in self:
            if rec.partner_id:
                return {'domain': {'vehicle_num': [('owner_id.id', '=', rec.partner_id.id)]}}
            else:
                return {'domain': {'vehicle_num': []}}

    # @api.model
    # def action_confirm(self):
    #     res = super(SaleOrderInherit, self).action_confirm()
    #     # if self.transfer_id:
    #     #     self.transfer_id.bill_status = 'billed'
    #     #     self.job_card_no.action_done()
    #     if self.requisition_id:
    #         self.requisition_id.bill_status = 'billed'
    #         self.job_card_no.action_done()
    #     return res

    @api.onchange('job_card_no')
    def onchange_job_card_no(self):
        for rec in self:
            if rec.job_card_no:
                if rec.job_card_no.vehicle_id:
                    rec.vehicle_num = rec.job_card_no.vehicle_id
                if rec.job_card_no.customer_id:
                    rec.partner_id = rec.job_card_no.customer_id

    def action_confirm(self):
        for order in self:
            insufficient_stock_products = []  # Collect insufficient stock details
            for line in order.order_line:
                product = line.product_id
                if product.type == 'product':  # Only check stockable products
                    if product.qty_available < line.product_uom_qty:
                        insufficient_stock_products.append(
                            _('Product: "%s", Available: %s, Required: %s') % (
                                product.display_name,
                                product.qty_available,
                                line.product_uom_qty
                            )
                        )
            if insufficient_stock_products:
                warning_message = _(
                    "The following products do not have sufficient stock:\n\n%s"
                ) % "\n".join(insufficient_stock_products)
                order.message_post(body=warning_message)
        return super(SaleOrderInherit, self).action_confirm()

    # @api.onchange('requisition_id')
    # def onchange_requisition_id(self):
    #     for rec in self:
    #         lines = []
    #         for line in self.requisition_id:
    #             vals = {
    #                 'product_id': line.product_id,
    #                 'name': line.product_id.product_tmpl_id.name,
    #                 'product_uom_qty': line.product_uom_qty,
    #                 'product_uom': line.product_id.product_tmpl_id.uom_id,
    #                 'price_unit': line.product_id.product_tmpl_id.list_price,
    #                 # 'order_id': line.id,
    #                 # 'customer_lead': 0.0
    #             }
    #             lines.append((vals))
    #         rec.order_line = lines

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     for rec in self:
    #         if rec.partner_id:
    #             return {'domain': {'vehicle_num': [('owner_id.id', '=', rec.partner_id.id)]}}

    # @api.onchange('transfer_id')
    # def onchange_transfer_id(self):
    #     for rec in self:
    #         lines=[]
    #         for line in self.transfer_id.move_lines:
    #             vals = {
    #                 'product_id': line.product_id,
    #                 'name': line.product_id.name,
    #                 'product_uom_qty': line.product_uom_qty,
    #                 'product_uom': line.product_id.product_tmpl_id.uom_id,
    #                 'price_unit': line.product_id.product_tmpl_id.list_price
    #                 # 'order_id': line.id
    #                 # 'customer_lead': 0.0
    #             }
    #             lines.append((vals))
    #         rec.order_line = lines
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_check_stock(self):
        """
        This method is triggered when a product is added or the quantity is changed in the order line.
        It checks if the stock is sufficient and raises an alert if not.
        """
        for line in self:
            if line.product_id and line.product_id.type == 'product':  # Check only for stockable products
                available_qty = line.product_id.qty_available
                if line.product_uom_qty > available_qty:
                    warning_message = {
                        'title': _('Insufficient Stock!'),
                        'message': _(
                            'The product "%s" does not have sufficient stock.\n\n'
                            'Available Quantity: %s\nRequired Quantity: %s'
                        ) % (line.product_id.display_name, available_qty, line.product_uom_qty),
                    }
                    return {'warning': warning_message}