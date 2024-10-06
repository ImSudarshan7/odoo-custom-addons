from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(string='PAN/VAT', required=True)
    city = fields.Char(required=True)
    state_id = fields.Many2one('res.country.state', required=True)
    country_id = fields.Many2one('res.country', required=True)
    mobile = fields.Char(required=True)

@api.onchange('company_type')
def _onchange_company_type(self):
    if self.company_type == 'company':
        self.vat_required = True
    else:
        self.vat_required = False
