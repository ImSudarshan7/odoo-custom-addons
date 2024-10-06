from odoo import models, fields, api, _


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
