# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Add PAN Number'

    pan_number = fields.Char(string='PAN Number', )
