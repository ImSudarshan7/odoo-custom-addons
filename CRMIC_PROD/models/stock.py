from odoo import models, fields, api
from num2words import num2words

class StockPicking(models.Model):
    _inherit = 'stock.picking'

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