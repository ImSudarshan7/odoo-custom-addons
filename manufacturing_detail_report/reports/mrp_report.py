# -*- coding: utf-8 -*-
from odoo import models, api, fields
from datetime import timedelta
import nepali_datetime


class ManufacturingReport(models.AbstractModel):
    _name = 'report.manufacturing_detail_report.mrp_report'

    def get_mrp_report(self, docs):
        domain = [
            ('date_planned_start', '>=', docs.date),
            ('date_planned_start', '<', docs.date + timedelta(days=1))
        ]

        if docs.product_nature_id:
            domain.append(('product_nature_id', '=', docs.product_nature_id.id))

        if docs.product_id:
            domain.append(('product_id', 'in', docs.product_id.ids))

        rec = self.env['mrp.production'].search(domain)
        return rec

    def get_nepali_date(self, english_date):
        """Convert Gregorian (English) date to Nepali date in the format 'Month Day, Year'."""
        if english_date:
            nepali_date = nepali_datetime.date.from_datetime_date(fields.Date.from_string(english_date))

            # Convert to 'Month Day, Year' format (e.g., Kartik 2, 2081)
            month_name = nepali_date.strftime('%B')  # Nepali month name
            day = nepali_date.day  # Nepali day
            year = nepali_date.year  # Nepali year

            formatted_nepali_date = f"{month_name} {day}, {year}"
            return formatted_nepali_date
        return ''


    @api.model
    def _get_report_values(self, docids, data=None):
        active_model = self.env.context.get('active_model')
        docs = self.env[active_model].browse(self.env.context.get('active_id'))
        datas = self.get_mrp_report(docs)
        # Get the Nepali equivalent of the date
        nepali_prod_date = self.get_nepali_date(docs.date)

        return {
               'doc_ids': docids,
               'doc_model': active_model,
               'docs': docs,
               'datas': datas,     
               'prod_date': docs.date,
               'nepali_prod_date': nepali_prod_date  # Nepali date

        }