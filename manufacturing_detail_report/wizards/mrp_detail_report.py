from odoo import models, fields, _
from datetime import date

class ManufacturingDetailReport(models.TransientModel):
    _name = "mrp.detail.report"

    date = fields.Date('Start Date',required='True',default=date.today())
    product_nature_id = fields.Many2one(
        'product.nature', 
        string='Product Nature', 
        domain=[('code', 'in', ['SFG', 'FG'])]
    )
    
    product_id = fields.Many2many('product.product',
        domain="[('product_nature_id', '=', product_nature_id)]")

    def print_mrp_detail_report(self):
        data = {
            'date': self.date,
            'nature': self.product_nature_id,
            'products': self.product_id
        }
        return self.env.ref('manufacturing_detail_report.action_report_print_mrp_detail').report_action(self, data=data)
