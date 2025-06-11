from num2words import num2words
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Fields
    address = fields.Char(string='To Place')
    challan_date = fields.Date(string='Challan Date')
    challan_no = fields.Char(string='Invoice No/Challan')
    contact_no = fields.Char(string='Contact No')
    delivery_contact_name = fields.Char(string='Delivery Contact Name')
    gate_entry = fields.Char(string='Gate Entry', required=True)
    quality_check = fields.Boolean(string='Quality Check')
    quality_check_comment = fields.Text(string='Quality Remarks', required=True)
    scheduled_date = fields.Datetime(string='Received Date')
    to = fields.Char(string='From Place')
    transportation_mode = fields.Selection([
        ('courier', 'Courier'),
        ('tailer', 'Tailer'),
        ('truck', 'Truck'),
        ('other', 'Other'),
    ], string='Transportation Mode', required=True)
    vehicle_contact_name = fields.Char(string='Vehicle Contact Name')
    vehicle_contact_no = fields.Char(string='Vehicle Contact No')
    vehicle_no = fields.Char(string='Vehicle No', required=False)

    # Methods
    def action_quality_check(self):
        for picking in self:
            # Toggle the quality_check field
            picking.quality_check = not picking.quality_check
        return True  # Return True to refresh the view after the button click

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

    def write(self, vals):
        # Check for `quality_check` in `vals`, or use the current record value
        quality_check_value = vals.get('quality_check', None)
        for record in self:
            # Use the existing value if not updating
            if quality_check_value is None:
                quality_check_value = record.quality_check

            # Validation for `quality_check` field
            if record.picking_type_code not in ['outgoing', 'internal', 'mrp_operation']:
                if not quality_check_value:
                    raise ValidationError('The Quality Check field must be checked.')

        # Call the super method to perform the actual write operation
        res = super().write(vals)
        return res

    @api.constrains('quality_check', 'picking_type_code')
    def _check_quality_check(self):
        for record in self:
            if record.picking_type_code not in ['outgoing', 'internal', 'mrp_operation']:
                if not record.quality_check:
                    raise ValidationError('The Quality Check field must be checked for the selected picking type.')

class StockMove(models.Model):
    _inherit = 'stock.move'

    amount = fields.Monetary(compute='_compute_amount', string='Total Amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
    unit_price = fields.Float(string='Unit Price', required=True, digits='Product Price')
    @api.depends('product_uom_qty', 'unit_price')
    def _compute_amount(self):
        for line in self:
            amount = line.product_uom_qty * line.unit_price
            line.update({
                'amount': amount,
            })

