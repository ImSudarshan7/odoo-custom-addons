from odoo import models, fields, api, _

class ProductInherit(models.Model):
    _inherit = 'product.template'
    rac_ids =  fields.Many2many('stock.location', 'product_location_rel', 'product_id', 'location_id',
                                  string='Locations')
    # hs_code = fields.Char(string="HS CODE", track_visibility='always')
