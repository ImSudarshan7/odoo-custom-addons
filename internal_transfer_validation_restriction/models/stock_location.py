# models/stock_location.py
from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    allowed_user_ids = fields.Many2many(
        'res.users', string='Allowed Users', help='Users allowed to validate transfers for this location')
