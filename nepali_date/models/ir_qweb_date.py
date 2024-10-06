# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2019-Present Lekhnath Rijal <mail@lekhnathrijal.com.np>
#
##########################################################################

from odoo import models, fields, api, _
from odoo.addons.nepali_date.convert_date import BikramSamvat
from six import string_types

class NepaliDateConverterMixin(models.AbstractModel):
    _name = 'nepali_date.qweb.field.converter.mixin'
    _description = 'Nepali Date Converter Mixin'

    @api.model
    def nepali_date_config(self):
        IRConfig = self.env['ir.config_parameter'].sudo()

        return dict(
            display_option =  IRConfig.get_param('nepali_date.report.date_mode', 'both'),
            date_format = IRConfig.get_param('nepali_date.date_format', '')
        )

    @api.model
    def convert_to_nepali_date(self, value, ad_date, options):
        bs_date = BikramSamvat(value)
        calendar_config = self.nepali_date_config()

        display_option = calendar_config.get('display_option', 'both')
        date_format = calendar_config.get('date_format', '')

        #NOTE: Inline option overrides global configuration
        display_option = options.get('date_mode', display_option)

        bs_date_formatted = f"{bs_date.format(date_format)} {_('B.S.')}"

        if display_option == 'ad':
            return ad_date
        elif display_option == 'bs':
            return bs_date_formatted
        else:
            return f"{ad_date} ({bs_date_formatted})"

class DateConverter(models.AbstractModel):
    _name = 'ir.qweb.field.date'
    _inherit = ['ir.qweb.field.date', 'nepali_date.qweb.field.converter.mixin']

    @api.model
    def get_available_options(self):
        options = super(DateConverter, self).get_available_options()
        options.update(
            date_mode=dict(type='string', string=_('Date Mode'))
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        ad_date = super(DateConverter, self).value_to_html(value, options)
        date_value = fields.Date.from_string(value) if isinstance(value, string_types) else value
        return self.convert_to_nepali_date(date_value, ad_date, options)

class DateTimeConverter(models.AbstractModel):
    _name = 'ir.qweb.field.datetime'
    _inherit = ['ir.qweb.field.datetime', 'nepali_date.qweb.field.converter.mixin']

    @api.model
    def get_available_options(self):
        options = super(DateTimeConverter, self).get_available_options()
        options.update(
            date_mode=dict(type='string', string=_('Date Mode'))
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        ad_date = super(DateTimeConverter, self).value_to_html(value, options)
        date_value = fields.Datetime.from_string(value) if isinstance(value, string_types) else value
        return self.convert_to_nepali_date(date_value, ad_date, options)
