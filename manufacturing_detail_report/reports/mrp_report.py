# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import timedelta

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

    @api.model
    def _get_report_values(self, docids, data=None):
        active_model = self.env.context.get('active_model')
        docs = self.env[active_model].browse(self.env.context.get('active_id'))
        datas = self.get_mrp_report(docs)
        return {
               'doc_ids': docids,
               'doc_model': active_model,
               'docs': docs,
               'datas': datas,     
               'prod_date': docs.date           
            }