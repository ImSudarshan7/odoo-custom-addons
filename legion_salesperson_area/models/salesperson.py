# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SalesPersonArea(models.Model):
    _name = 'salesperson.area'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string=" Area Name")
    name_seq = fields.Char(string='Area ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    image = fields.Binary(string="Image", attachment=True)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('salesperson.area.sequence') or _('New')
        result = super(SalesPersonArea, self).create(vals)
        return result
