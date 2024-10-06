from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'res.company'

    image_field_1 = fields.Binary(string='Image1', attachment=True)
    image_field_2 = fields.Binary(string='Image2', attachment=True)
    image_field_3 = fields.Binary(string='Image3', attachment=True)