import json
import requests
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import nepali_datetime


class AccountMoveInherited(models.Model):
    _inherit = 'account.move'

    @api.model
    def run_sql_my(self, qry):
        self._cr.execute(qry)

    @api.depends('company_id')
    def _perform_compute_action(self):
        for rec in self:
            if rec.company_id:
                if rec.company_id.ird_integ == True:
                    rec.ird_integ = True
                else:
                    rec.ird_integ = False

    copy_count = fields.Integer(default=0, string='Print Count', help="used for invoice printcount", store=True)
    bill_post = fields.Boolean(string='Sync state', track_visibility='always', default=False)
    bill_data = fields.Char(string='Bill Data', track_visibility='always')
    last_printed = fields.Datetime(string='Last Printed', default=lambda self: fields.datetime.now(),
                                   track_visibility='always')
    ird_integ = fields.Boolean('Connect to IRD', compute='_perform_compute_action')

    @api.model
    def post_invoices_ird(self):
        inv_objs = self.env['account.move'].search(
            [('state', '=', 'posted'), ('move_type', 'in', ('out_invoice', 'out_refund')), ('bill_post', '=', False)])
        if inv_objs:
            for invoice in inv_objs:
                comp_obj = self.env['res.company'].search([('id', '=', invoice.company_id.id)], limit=1)
                if comp_obj.ird_integ:
                    headers = {'charset': 'utf-8'}
                    if comp_obj.fy_start < invoice.invoice_date < comp_obj.fy_end:
                        fy_yr = comp_obj.fy_prefix
                        if invoice.move_type == 'out_invoice':
                            url = 'https://cbapi.ird.gov.np/api/bill'
                            data = {
                                "username": str(comp_obj.ird_user),
                                "password": str(comp_obj.ird_password),
                                "seller_pan": str(invoice.company_id.vat),
                                "buyer_pan": str(invoice.partner_id.vat),
                                "buyer_name": str(invoice.partner_id.name),
                                "fiscal_year": fy_yr,
                                "invoice_number": str(invoice.name),
                                "invoice_date": nepali_datetime.date.from_datetime_date(invoice.invoice_date).strftime('%Y.%m.%d'),
                                "total_sales": invoice.amount_total,
                                "taxable_sales_vat": invoice.amount_untaxed,
                                "vat": invoice.amount_tax,
                                "excisable_amount": 0,
                                "excise": 0,
                                "taxable_sales_hst": 0,
                                "hst": 0,
                                "amount_for_esf": 0,
                                "esf": 0,
                                "export_sales": 0,
                                "tax_exempted_sales": 0,
                                "isrealtime": True,
                                "datetimeclient": str(datetime.now().isoformat())
                            }
                            try:
                                response = requests.post(url, json=data, headers=headers)
                                data["password"] = "*****"
                                invoice.bill_data = json.dumps(data) + str(response)
                                invoice.bill_post = True
                            except:
                                pass
                        elif invoice.move_type == 'out_refund':
                            url = 'https://cbapi.ird.gov.np/api/billreturn'
                            data = {
                                "username": str(comp_obj.ird_user),
                                "password": str(comp_obj.ird_password),
                                "seller_pan": str(invoice.company_id.vat),
                                "buyer_pan": str(invoice.partner_id.vat),
                                "buyer_name": str(invoice.partner_id.name),
                                "fiscal_year": fy_yr,
                                "ref_invoice_number": str(invoice.ref),
                                "credit_note_number": str(invoice.name),
                                "credit_note_date": nepali_datetime.date.from_datetime_date(invoice.invoice_date).strftime('%Y.%m.%d'),
                                "reason_for_return": invoice.ref,
                                "total_sales": invoice.amount_total,
                                "taxable_sales_vat": invoice.amount_untaxed,
                                "vat": invoice.amount_tax,
                                "excisable_amount": 0,
                                "excise": 0,
                                "taxable_sales_hst": 0,
                                "hst": 0,
                                "amount_for_esf": 0,
                                "esf": 0,
                                "export_sales": 0,
                                "tax_exempted_sales": 0,
                                "isrealtime": True,
                                "datetimeclient": str(datetime.now().isoformat())
                            }
                            try:
                                response = requests.post(url, json=data, headers=headers)
                                data["password"] = "*****"
                                invoice.bill_data = json.dumps(data) + str(response)
                                invoice.bill_post = True
                            except:
                                pass
                    else:
                        print('Invalid date i.e out of current Fiscal Year.')
                else:
                    print("IRD Disabled in this company")
        else:
            print("All bills posted to IRD")

    @api.depends('amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.currency_id.amount_to_text(self.amount_total)
        return amount_in_words


class ResCompanyInherited(models.Model):
    _inherit = 'res.company'

    ird_integ = fields.Boolean('Connect to IRD', default=False)
    ird_user = fields.Char('IRD Username')
    ird_password = fields.Char('IRD Password')
    fy_start = fields.Date('Fiscal Year Start')
    fy_end = fields.Date('Fiscal Year End')
    fy_prefix = fields.Char('FY prefix')


class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'

    @api.onchange('vat')
    def _valid_pan(self):
        if self.vat:
            if ((len(self.vat) == 0 or len(self.vat) == 9) and self.vat[0:].isdigit() == True):
                pass
            else:
                raise ValidationError(_('Invalid Pan Number'))
