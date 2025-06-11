from odoo import models,api, fields, _
from datetime import date
from odoo.exceptions import ValidationError


class PsReport(models.Model):
    _name = "ps.report"

    start_date = fields.Date('Start Date', required='True', default=date.today())
    end_date = fields.Date('End date', required='True', default=date.today())
    invoice_type = fields.Selection([
            ('out_invoice', 'Sales'),
            ('out_refund', 'Sales Return'),
            ('in_invoice', 'Purchase'),
            ('in_refund', 'Purchase Return'),
        ], string='Type', default='out_invoice', required=True)

    def get_label(self):
        if self.invoice_type:
            return dict(self._fields['invoice_type'].selection).get(self.invoice_type)
        return False

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_('End Date cannot be earlier than Start Date.'))

    def print_report(self):

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'invoice_type': self.invoice_type,
            'invoice_label': self.get_label()

        }
        return self.env.ref('sale_purchase_reports.reports_sale_purchase').report_action(self,data=data)

