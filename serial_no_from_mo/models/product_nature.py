from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

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


@api.model
def create(self, vals):
    if vals.get('product_nature_id'):
        product_nature = self.env['product.nature'].browse(vals['product_nature_id'])
        if product_nature:
            prefix = product_nature.code.upper()

            last_product = self.search([
                ('default_code', '=like', f"{prefix}%")
            ], order="default_code desc", limit=1)

            # Extract numeric part after prefix
            numeric_part = re.search(r'\d+$', last_product.default_code.replace(prefix, ''))
            last_number = int(numeric_part.group()) if numeric_part else 0

            # Generate new default code
            new_number = last_number + 1
            new_default_code = f"{prefix}{str(new_number).zfill(4)}"
            vals['default_code'] = new_default_code

    return super(ProductTemplate, self).create(vals)
