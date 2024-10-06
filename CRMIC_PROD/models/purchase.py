from odoo import models, fields, api
from num2words import num2words

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    date_approve = fields.Datetime('Purchase Date', readonly=1, index=True, copy=False)
    date_planned = fields.Datetime(
        string='Due Date', index=True, copy=False, compute='_compute_date_planned', store=True, readonly=False,
        help="Delivery date promised by vendor. This date is used to determine expected arrival of products.")

    @api.model
    def action_rfq_send(self):
        return False  # Implement functionality or remove if not needed

    @api.model
    def print_quotation(self):
        # Implement functionality or return appropriate result
        return False

    @api.depends('order_line.date_planned')
    def _compute_date_planned(self):
        """ date_planned = the earliest date_planned across all order lines. """
        for order in self:
            dates_list = order.order_line.filtered(lambda x: not x.display_type and x.date_planned).mapped(
                'date_planned')
            if dates_list:
                order.date_planned = fields.Datetime.to_string(min(dates_list))
            else:
                order.date_planned = False

# To convert the amount into words
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