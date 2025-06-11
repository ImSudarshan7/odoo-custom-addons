from odoo import models, fields, _


class AuditLocation(models.Model):
    _name = 'audit.location'
    _description = 'Audit Locations'

    name = fields.Char(string='Location Name', required=True)
    location_code = fields.Char(string='Location Code', required=True)
    auditor_ids = fields.Many2many('res.users', string='Assigned Auditors')
    item_ids = fields.One2many('audit.item', 'location_id', string='Items')
    items_to_assign = fields.Integer('Assign Items')
