from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductNature(models.Model):
    _name = 'product.nature'
    _description = 'Product Nature'

    name = fields.Char(string='Nature', required=True)
    code = fields.Char(string='Short Code', required=True)


    @api.constrains('code')
    def _check_unique_code_case_insensitive(self):
        for record in self:
            existing = self.search([
                ('id', '!=', record.id),
                ('code', '=', record.code)
            ])
            if existing:
                raise ValidationError(_('The short code must be unique'))
            

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_nature_id = fields.Many2one('product.nature', 'Product Nature')

