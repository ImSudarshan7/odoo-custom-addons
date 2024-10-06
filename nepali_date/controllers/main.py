# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2019-Present Lekhnath Rijal <mail@lekhnathrijal.com.np>
#
##########################################################################


from odoo.addons.web.controllers.main import CSVExport, ExcelExport
from odoo.http import request
from datetime import datetime, date
from odoo.addons.nepali_date.convert_date import BikramSamvat
from odoo.tools import pycompat

def format_data(fields, rows):
    IRConfig = request.env['ir.config_parameter'].sudo()
    (display_option, ) =  IRConfig.get_param('nepali_date.report.date_mode', ('both', )),
    date_format = IRConfig.get_param('nepali_date.date_format', 'MM dd, yyyy')

    def convert_date(value):
        if not isinstance(value, (datetime, date)):
            return value

        date_formatted = pycompat.to_text(value)
        bs_date_formatted = BikramSamvat(value).format(date_format)

        if display_option == 'ad':
            return date_formatted
        elif display_option == 'bs':
            return bs_date_formatted
        else:
            return f'{date_formatted} ({bs_date_formatted})'

    converted = [convert_date(d) for row in rows for d in row]
    column_count = len(fields)
    rows = [converted[i:i+column_count] for i in range(0, len(converted), column_count)]

    return rows

class CSVExportBSDate(CSVExport):
    def from_data(self, fields, rows):
        return super(CSVExportBSDate, self).from_data(
            fields,
            format_data(fields, rows)
        )

class ExcelExportBSDate(ExcelExport):
    def from_data(self, fields, rows):
        return super(ExcelExportBSDate, self).from_data(
            fields,
            format_data(fields, rows)
        )
