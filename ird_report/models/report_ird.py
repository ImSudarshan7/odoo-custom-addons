# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta, datetime
from odoo.http import request
from odoo.exceptions import UserError
import time
import odoo
import logging
_logger = logging.getLogger(__name__)
class ReportIrd(models.AbstractModel):
    _name = 'report.ird_report.report_ird'

    def get_ird_report(self, docs):
       
        if docs.from_date and docs.to_date:
            rec = self.env['account.move'].search([
                                                        ('invoice_date', '>=', docs.from_date),('invoice_date', '<=', docs.to_date),('move_type','in',('out_invoice','out_refund'))])
        elif docs.from_date:
            rec = self.env['account.move'].search([
                                                        ('invoice_date', '>=', docs.from_date),('move_type','in',('out_invoice','out_refund'))])
        elif docs.to_date:
            rec = self.env['account.move'].search([
                                                            ('invoice_date', '<=', docs.to_date),('move_type','in',('out_invoice','out_refund'))])
        records = []
        # total = 0
        for r in rec:
            vals = {
                    'fy':r.company_id.fy_prefix,
                    'number': r.name,
                    'vat': r.partner_id.vat,
                    'name': r.partner_id.name,
                    'amount_untaxed': r.amount_untaxed,
                    # 'amount_actual': r.amount_actual,
                    'amount_discount': "0.00",
                    'amount_total': r.amount_total,
                    'amount_tax': r.amount_tax,
                    'bill_post': r.bill_post,
                    'copy_count': r.copy_count,
                    'last_printed': r.last_printed,
                    'user_id': r.user_id.name,
                    'move_type': r.move_type,
                    'state': r.state,
                    'date': r.date,
                    'payment_state': r.payment_state,
                    }
            records.append(vals)
            print("==================karna================")
            print(records)
        return [records]

    @api.model
    def _get_report_values(self, docids, data=None):
        """we are overwriting this function because we need to show values from other models in the report
        we pass the objects in the docargs dictionary"""
        active_model = self.env.context.get('active_model')
        docs = self.env[active_model].browse(self.env.context.get('active_id'))  
        datas = self.get_ird_report(docs)
        print("==================fINSL================")
        print(datas)
        version_info = odoo.service.common.exp_version()
        k = version_info.get('server_version')
        j = version_info.get('server_version_info')
        _logger.info("*********++++++++++++++++++++++++++")
        _logger.info(k)
        _logger.info(j)
        if docs.from_date and docs.to_date:
            period = "From " + str(docs.from_date) + " To " + str(docs.to_date)
        elif docs.from_date:
            period = "From " + str(docs.from_date)
        elif docs.from_date:
            period = " To " + str(docs.to_date)
        return {
               'doc_ids': docids,
               'doc_model': active_model,
               'docs': docs,
               'time': time,
               'result': datas,
               'period': period,
               
            }