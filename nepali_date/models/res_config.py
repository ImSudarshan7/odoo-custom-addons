# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2019-Present Lekhnath Rijal <mail@lekhnathrijal.com.np>
#
##########################################################################

from odoo import models, api, fields
from odoo.addons.nepali_date.convert_date import BikramSamvat

class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    #NOTE: default_ prefix has special meaning in Odoo so not using that here
    datepicker_default = fields.Selection([
        ('bs', 'Nepali (B.S.)'),
        ('ad', 'Gregorian (A.D.)'),
    ], default='bs', string='Default Datepicker', config_parameter='nepali_date.default_datepicker')
    nepali_date_format = fields.Char(string='Date Format', config_parameter='nepali_date.date_format')
    nepali_date_preview = fields.Char('Date Preview', compute='_compute_nepali_date_preview')
    convert_date_report = fields.Selection([
        ('both', 'Display both dates'),
        ('ad', 'Display A.D. date only'),
        ('bs', 'Display B.S. date only'),
    ],string='Conversion on Report',config_parameter='nepali_date.report.date_mode')

    @api.depends('nepali_date_format')
    def _compute_nepali_date_preview(self):
        self.nepali_date_preview = BikramSamvat().format(self.nepali_date_format)
