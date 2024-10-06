from odoo import models,api, fields, _
from datetime import date
from odoo.exceptions import ValidationError

class ManufacturingDetailExcel(models.TransientModel):
    _name = "mrp.detail.reports"
    _description = "Manufacturing Detail Report Wizard"

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)

    product_nature_id = fields.Many2one(
        'product.nature',
        string='Product Nature',
        domain=[('code', 'in', ['SFG', 'FG'])],
        required=False
    )
    product_id = fields.Many2many(
        'product.product',
        string='Products',
        domain="[('product_nature_id', '=', product_nature_id)]",
        required=False
    )

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.end_date < record.start_date:
             raise ValidationError(_('End Date cannot be earlier than Start Date.'))

    def print_mrp_detail_report_xlsx(self):
        """Generates and prints the Manufacturing Detail Report."""
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_nature_id': self.product_nature_id.id,
            'product_ids': self.product_id.ids
        }
        return self.env.ref('manufacture_excel_report.report_manufacturing_order_xls').report_action(self,data=data)

    weight = fields.Float(string='Weight', compute='_compute_weight')

