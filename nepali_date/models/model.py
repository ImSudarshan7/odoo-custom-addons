# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from datetime import date
from . import bikram
from bikram import samwat


class NepDateInv(models.Model):
    _inherit = 'account.invoice'

    @api.depends('date_invoice')
    def mydate3(self):
        """:return the Nepalidate"""
        if self.date_invoice:
            date_str = str(self.date_invoice) 
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.nep_inv_date = samwat.from_ad(datetime_obj.date())

    @api.depends('date_due')
    def mydate4(self):
        if self.date_due:
            """:return the Nepalidate"""
            date_str2 = str(self.date_due)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj2 = datetime.strptime(date_str2, format_str)
            self.nep_due_date = samwat.from_ad(datetime_obj2.date())

    @api.depends('write_date')
    def mydate5(self):
        if self.write_date:
            """:return the Nepalidate"""
            date_str2 = str(self.write_date)
            format_str = '%Y-%m-%d %H:%M:%S'  # The format
            datetime_obj2 = datetime.strptime(date_str2, format_str)
            self.nep_write_date = samwat.from_ad(datetime_obj2.date())
    

    @api.depends('date')
    def mydate6(self):
        if self.date:
            """:return the Nepalidate"""
            date_str2 = str(self.date)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj2 = datetime.strptime(date_str2, format_str)
            self.nep_date = samwat.from_ad(datetime_obj2.date())

    nep_inv_date = fields.Char(string='Invoice Date BS', compute=mydate3, store=True)
    nep_due_date = fields.Char(string='Due Date BS', compute=mydate4, store=True)
    nep_write_date = fields.Char(string='Invoice Date BS', compute=mydate5, store=True)
    nep_date = fields.Char(string='Transaction Date BS', compute=mydate6, store=True)

class NepDateJv(models.Model):
    _inherit = 'account.move'

    @api.depends('date')
    def mydate3(self):
        """:return the Nepalidate"""
        if self.date:
            date_str = str(self.date) 
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.nep_jv_date = samwat.from_ad(datetime_obj.date())     

    nep_jv_date = fields.Char(string='Date BS', compute=mydate3, store=True)

    
class DateBsStock(models.Model):
    _inherit = 'stock.picking'

    @api.depends('date')
    def picking_date_bs(self):
        """:return the Nepalidate"""
        if self.date:
            date_str = str(self.date) 
            format_str = '%Y-%m-%d %H:%M:%S'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_bs = samwat.from_ad(datetime_obj.date())

    date_bs = fields.Char(string='Date BS', compute=picking_date_bs, store=True)


class DateBsPos(models.Model):
    _inherit = 'pos.order'

    @api.depends('date_order')
    def pos_date_bs(self):
        """:return the Nepalidate"""
        if self.date_order:
            date_str = str(self.date_order)
            format_str = '%Y-%m-%d %H:%M:%S'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_bs = samwat.from_ad(datetime_obj.date())

    date_bs = fields.Char(string='Date BS', compute=pos_date_bs, store=True)



class DateBsSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('date_order')
    def sale_date_bs(self):
        """:return the Nepalidate"""
        if self.date_order:
            date_str = str(self.date_order)
            format_str = '%Y-%m-%d %H:%M:%S'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_bs = samwat.from_ad(datetime_obj.date())

    date_bs = fields.Char(string='Date BS', compute=sale_date_bs, store=True)

class DateBsPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('date_order')
    def purchase_date_bs(self):
        """:return the Nepalidate"""
        if self.date_order:
            date_str = str(self.date_order)
            format_str = '%Y-%m-%d %H:%M:%S'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_bs = samwat.from_ad(datetime_obj.date())

    date_bs = fields.Char(string='Date BS', compute=purchase_date_bs, store=True)


class DateBsRequisitionForm(models.Model):
    _inherit = 'requisition.form'
    @api.depends('date_request')
    def request_date_bs(self):
        """:return the Nepalidate"""
        if self.date_request:
            date_str = str(self.date_request)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.request_date_bs = samwat.from_ad(datetime_obj.date())
    @api.depends('date_approve')
    def approve_date_bs(self):
        """:return the Nepalidate"""
        if self.date_approve:
            date_str = str(self.date_approve)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.approve_date_bs = samwat.from_ad(datetime_obj.date())
    request_date_bs = fields.Char(string='Request Date BS', compute=request_date_bs, store=True)
    approve_date_bs = fields.Char(string='Approve Date BS', compute=approve_date_bs, store=True)

class DateBsJobOrder(models.Model):
    _inherit = 'job.order'
    @api.depends('date_in')
    def date_in_bs(self):
        """:return the Nepalidate"""
        if self.date_in:
            date_str = str(self.date_in)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_in_bs = samwat.from_ad(datetime_obj.date())
    @api.depends('date_out')
    def date_out_bs(self):
        """:return the Nepalidate"""
        if self.date_out:
            date_str = str(self.date_out)
            format_str = '%Y-%m-%d'  # The format
            datetime_obj = datetime.strptime(date_str, format_str)
            self.date_out_bs = samwat.from_ad(datetime_obj.date())
    date_in_bs = fields.Char(string='Date In BS', compute=date_in_bs, store=True)
    date_out_bs = fields.Char(string='Date Out BS', compute=date_out_bs, store=True)

