# -*- coding: utf-8 -*-

import re
import uuid
import base64

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    theme_background_image = fields.Binary(
        related='company_id.background_image',
        readonly=False
    )

    color_brand_secondary = fields.Char(
        string='Brand secondary Color'
    )
    
    color_brand_primary = fields.Char(
        string='Brand Primary Color'
    )
    
    theme_color_brand = fields.Char(
        string='Theme Brand Color'
    )
    
    theme_color_primary = fields.Char(
        string='Theme Primary Color'
    )
    
    theme_color_required = fields.Char(
        string='Theme Required Color'
    )
    
    theme_color_menu = fields.Char(
        string='Theme Menu Color'
    )
    
    theme_color_appbar_color = fields.Char(
        string='Theme AppBar Color'
    )
    
    theme_color_appbar_background = fields.Char(
        string='Theme AppBar Background'
    )
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        variables = [
            'o-brand-odoo',
            'o-brand-primary',
            'mk-required-color',
            'mk-apps-color',
            'mk-appbar-color',
            'mk-appbar-background',
        ]
        variables2 = [
            'brand-secondary',
            'brand-primary',
        ]
        colors = self.env['web_editor.assets'].get_variables_values(
            '/web_o2b_responsive/static/src/colors.scss', 'web._assets_primary_variables', variables
        )
        colors2 = self.env['web_editor.assets'].get_variables_values(
            '/web_o2b_responsive/static/src/legacy/scss/colors.scss', 'web._assets_primary_variables', variables2
        )
        colors_changed = []
        colors_changed.append(self.theme_color_brand != colors['o-brand-odoo'])
        colors_changed.append(self.theme_color_primary != colors['o-brand-primary'])
        colors_changed.append(self.color_brand_secondary != colors2['brand-secondary'])
        colors_changed.append(self.color_brand_primary != colors2['brand-primary'])
        colors_changed.append(self.theme_color_required != colors['mk-required-color'])
        colors_changed.append(self.theme_color_menu != colors['mk-apps-color'])
        colors_changed.append(self.theme_color_appbar_color != colors['mk-appbar-color'])
        colors_changed.append(self.theme_color_appbar_background != colors['mk-appbar-background'])
        if(any(colors_changed)):
            variables = [
                {'name': 'o-brand-odoo', 'value': self.theme_color_brand or "#243742"},
                {'name': 'o-brand-primary', 'value': self.theme_color_primary or "#5D8DA8"},
                {'name': 'mk-required-color', 'value': self.theme_color_required or "#d1dfe6"},
                {'name': 'mk-apps-color', 'value': self.theme_color_menu or "#f8f9fa"},
                {'name': 'mk-appbar-color', 'value': self.theme_color_appbar_color or "#dee2e6"},
                {'name': 'mk-appbar-background', 'value': self.theme_color_appbar_background or "#000000"},
            ]
            variables2 = [
                {'name': 'brand-secondary', 'value': self.color_brand_secondary or "#6a4533"},
                {'name': 'brand-primary', 'value': self.color_brand_primary or "#84563f"},
            ]
            self.env['web_editor.assets'].replace_variables_values(
                '/web_o2b_responsive/static/src/colors.scss', 'web._assets_primary_variables', variables
            )
            self.env['web_editor.assets'].replace_variables_values(
                '/web_o2b_responsive/static/src/legacy/scss/colors.scss', 'web._assets_primary_variables', variables2
            )
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        variables = [
            'o-brand-odoo',
            'o-brand-primary',
            'mk-required-color',
            'mk-apps-color',
            'mk-appbar-color',
            'mk-appbar-background',
        ]
        variables2 = [
            'brand-secondary',
            'brand-primary',
        ]
        colors = self.env['web_editor.assets'].get_variables_values(
            '/web_o2b_responsive/static/src/colors.scss', 'web._assets_primary_variables', variables
        )
        colors2 = self.env['web_editor.assets'].get_variables_values(
            '/web_o2b_responsive/static/src/legacy/scss/colors.scss', 'web._assets_primary_variables', variables2
        )
        res.update({
            'color_brand_primary': colors2['brand-primary'],
            'color_brand_secondary': colors2['brand-primary'],
            'theme_color_brand': colors['o-brand-odoo'],
            'theme_color_primary': colors['o-brand-primary'],
            'theme_color_required': colors['mk-required-color'],
            'theme_color_menu': colors['mk-apps-color'],
            'theme_color_appbar_color': colors['mk-appbar-color'],
            'theme_color_appbar_background': colors['mk-appbar-background'],
        })
        return res
