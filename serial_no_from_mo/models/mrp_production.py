from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class ProductCategory(models.Model):
    _inherit = 'product.category'

    prefix = fields.Char(string="Prefix")


class MrpBom(models.Model):
    _inherit = "mrp.bom"
    
    product_nature_id = fields.Many2one(
        'product.nature', 
        string='Product Nature', 
        domain=[('code', 'in', ['SFG', 'FG'])]
    )
    
    product_tmpl_id = fields.Many2one(
        domain="[('product_nature_id', '=', product_nature_id), ('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    product_nature_id = fields.Many2one(
        'product.nature', 
        string='Product Nature', 
        domain=[('code', 'in', ['SFG', 'FG'])]
    )
    
    product_id = fields.Many2one(
        domain="""[
            ('product_nature_id', '=', product_nature_id),
            ('type', 'in', ['product', 'consu']),
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id)
        ]
        """)

    def _get_category_prefix(self, category):
        """Recursively retrieve the prefix from the category hierarchy."""
        prefixes = []
        while category and category.parent_id:
            if category.prefix:
                prefixes.insert(0, category.prefix)
            category = category.parent_id
        return "/".join(prefixes)

    def action_confirm(self):
        parms = self.env['ir.config_parameter'].sudo()
        type = parms.get_param('serial_selection')
        today_str = self.date_planned_start.strftime('%y%m%d') if self.date_planned_start else fields.Datetime.today().strftime('%y%m%d')

        for rec in self:
            if type == 'global':
                prefix = parms.get_param('prefix')
                if not prefix:
                    raise UserError(
                        "Global prefix is not set in system parameters.")
                full_prefix = f"{prefix}/{today_str}/"
            else:
                category_prefix = self._get_category_prefix(
                    rec.product_id.categ_id)
                if not category_prefix:
                    raise UserError(f"Prefix is not set for the category hierarchy of the product '{rec.product_id.name}'.")
                full_prefix = f"{category_prefix}/{today_str}/"

            if rec.product_id.tracking == 'serial' or rec.product_id.tracking == 'lot':
                digit = parms.get_param('digit')
                seq_code = 'mrp.production.sequence' if type == 'global' else rec.product_id.name
                
                existing_lot = self.env['stock.production.lot'].sudo().search([
                    ('product_id', '=', rec.product_id.id),
                    ('name', 'like', full_prefix)
                ], order='name desc', limit=1)
                
                if existing_lot:
                    last_number = existing_lot.name.split('/')[-1]
                    next_number = int(last_number) + 1
                else:
                    next_number = 1
                    
                seq = self.env['ir.sequence'].sudo().search([('code', '=', seq_code)], limit=1)

                if seq:
                    if seq.prefix != full_prefix:
                        seq.sudo().write({
                            'prefix': full_prefix,
                            'padding': digit,
                            'number_next_actual': next_number
                        })
                else:
                    self.env['ir.sequence'].sudo().create({
                        'name': 'Mrp Production',
                        'implementation': 'standard',
                        'code': 'mrp.production.sequence' if type == 'global' else rec.product_id.name,
                        'prefix': full_prefix,
                        'padding': digit
                    })
                serial_id = self.env['stock.production.lot'].sudo().create({
                    'name': self.env['ir.sequence'].sudo().next_by_code('mrp.production.sequence' if type == 'global' else rec.product_id.name),
                    'product_id': rec.product_id.id,
                    'company_id': rec.company_id.id,
                })
                rec.lot_producing_id = serial_id

        return super(MrpProduction, self).action_confirm()
