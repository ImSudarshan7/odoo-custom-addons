# # -*- coding: utf-8 -*-

import logging
from num2words import num2words
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.move"
    _description = "Invoice"

    invoice_count = fields.Integer(string='Count', default=0)
    mode_of_payment = fields.Selection([
        ('cash', 'CASH'),
        ('cheque', 'CHEQUE'),
        ('credit', 'CREDIT'),
        ('other', 'OTHERS'),
    ], string='Mode of Payment', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        track_visibility='always', default='cash')
    first_invoice = fields.Boolean()

    def print_invoice(self):
        if self.state == 'draft':
            # self.first_invoice = False
            self.write({'first_invoice': False})
        else:
            # self.first_invoice = True
            self.write({'first_invoice': True})
        return self.env.ref('abgroup_invoice.report_tax_invoice').report_action(self)

    @api.model
    def run_sql(self, query):
        self._cr.execute(query)

    def duplicate_invoice(self):
        self.ensure_one()
        new_count = self.invoice_count + 1
        self.invoice_count = new_count
        return self.env.ref('abgroup_invoice.report_tax_invoice_duplicate').report_action(self)

    @api.constrains('invoice_date')
    def _check_invoice_date(self):
        for rec in self:
            if rec.invoice_date:
                today = fields.Date.context_today(self)
                if rec.invoice_date < today:
                    raise ValidationError(_('Backdate entry is prohibited. Invoice Date cannot be earlier than today.'))

    @api.constrains('date')
    def _check_accounting_date(self):
        for rec in self:
            if rec.date:
                today = fields.Date.context_today(self)
                if rec.date < today:
                    raise ValidationError(_('Backdate restriction. Accounting Date cannot be earlier than today.'))

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        if 'invoice_date' in fields_list:
            defaults['invoice_date'] = fields.Date.context_today(self)

        return defaults
    @api.model
    def amount_to_text(self, amount, currency):
        # Handle zero amount explicitly
        if amount == 0:
            return "ZERO ONLY".upper()

        # Split the amount into integer and decimal parts
        integer_part = int(amount)
        decimal_part = round((amount - integer_part) * 100)  # Converts decimal part to integer percentage

        # Convert integer and decimal parts to words
        integer_in_words = num2words(integer_part, lang='en')
        decimal_in_words = num2words(decimal_part, lang='en')

        # Handle NPR currency
        if currency.upper() == 'NPR':
            currency_in_words = 'Rupee' if integer_part == 1 else 'Rupees'
            result = f"{integer_in_words} {currency_in_words} and {decimal_in_words} Paisa only"
        else:
            # Handle other currencies
            result = f"{integer_in_words} {currency} and {decimal_in_words} {currency} only"

        return result.upper()
 
