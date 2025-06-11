##########################################################################
# Author      : O2b Technologies Pvt. Ltd.(<www.o2btechnologies.com>)
# Copyright(c): 2016-Present O2b Technologies Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
##########################################################################

from odoo import models, fields, api,_
from odoo import fields, models
from odoo import http
from odoo.exceptions import UserError, ValidationError, RedirectWarning
import requests
import datetime
from datetime import date 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
# import pandas as pd

import logging
import string 
import random 

import werkzeug.urls

from ast import literal_eval

from odoo import release, SUPERUSER_ID
from odoo.models import AbstractModel
from odoo.tools.translate import _
from odoo.tools import config, misc, ustr
import qrcode
import base64
from io import BytesIO
import random
from random import randint
from passlib.context import CryptContext
crypt_context = CryptContext(schemes=['pbkdf2_sha512', 'plaintext'],
                             deprecated=['plaintext'])

_logger = logging.getLogger(__name__)

class MapUrlUpadte(models.TransientModel):
    _name='update.barcode'
    _description='Map Url Upadte'

    def update_url(self):
        N = 12
        print("self@@@@@@@@@@@@",self)
        res = ''.join(random.choices(string.ascii_uppercase +
                         string.digits, k = N))
        barcode_random = randint(1000000, 9999999)
        self.barcode_for_app = res
        enc = crypt_context.encrypt(str(barcode_random))
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.full_barcode = base_url+'/web/barcodelogin?barcode='+enc+'+/-'+res
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(self.full_barcode)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.barcode_image = qr_image


class IrCron(models.Model):
    _inherit = 'ir.cron'

    no_del_scheduler = fields.Boolean(copy=False)

    @api.model
    def toggle(self, model, domain):
        if self.no_del_scheduler:
            return False
        active = bool(self.env[model].search_count(domain))
        return self.try_write({'active': active})

    def unlink(self):
        for var in self:
            if var.no_del_scheduler:
                raise UserError(
                    _('You\'re not allowed to delete this scheduler.'))
        return super(IrCron, self).unlink()

class UpgradeSchedulerClass(models.Model):
    _name = 'upgrade.database'
    _description = 'Upgrade Scheduler Class'

    def get_param_values(self):
        return self.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')

    def set_parameters_funct(self):
        subscription_id = self.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
        module_obj = self.env['ir.module.module'].search([('name','=','web_o2b_responsive')], limit=1)
        o2b_expire_date = self.env['ir.config_parameter'].sudo().search([('key','=', 'o2b_expire_date')])
        IrParamSudo = self.env['ir.config_parameter'].sudo()
        if subscription_id and subscription_id != 'trial':
            dbuuid = IrParamSudo.get_param('database.uuid')
            Users = self.env['res.users']
            limit_date = datetime.now()
            limit_date = limit_date - timedelta(15)
            limit_date_str = limit_date.strftime(misc.DEFAULT_SERVER_DATETIME_FORMAT)
            nbr_users = Users.search_count([('active', '=', True)])
            nbr_active_users = Users.search_count([("login_date", ">=", limit_date_str), ('active', '=', True)])
            domain = [('application', '=', True), ('state', 'in', ['installed', 'to upgrade', 'to remove'])]
            apps = self.env['ir.module.module'].sudo().search_read(domain, ['name'])
            parameters = {"subscription_id": subscription_id, 'dbuuid': dbuuid}
            base_domain = IrParamSudo.get_param('base_domain')
            url = base_domain + "/o2b/subscription_date"
            payload = {
                "params":{
                    "subscription_id": subscription_id,
                    "dbuuid": dbuuid,
                    "apps": ",".join(app['name'] for app in apps),
                    "nbr_users": nbr_users,
                    "nbr_active_users": nbr_active_users,
                }
            }
            payload = json.dumps(payload)
            headers = {
              'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data = payload)
            data = response.json()
            val = data.get('result')
            if val:
                dict_val = eval(val)
                date_string = False
                ext_apps = dict_val.get('ext_apps')
                ext_users = dict_val.get('ext_users')
                if self.env['ir.config_parameter'].sudo().get_param('ext_apps'):
                    self.env['ir.config_parameter'].sudo().set_param("ext_apps", str(ext_apps))
                else:
                    self.env['ir.config_parameter'].sudo().create({
                        'key': 'ext_apps',
                        'value': str(ext_apps)
                        })
                if self.env['ir.config_parameter'].sudo().get_param('ext_users'):
                    self.env['ir.config_parameter'].sudo().set_param("ext_users", str(ext_users))
                else:
                    self.env['ir.config_parameter'].sudo().create({
                        'key': 'ext_users',
                        'value': str(ext_users)
                        })
                
                date_string = dict_val.get('expiry_date')
                expire_date = datetime.strptime(date_string, '%m/%d/%Y')
                
                if expire_date < datetime.now():
                    subscription_id = self.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
                    if subscription_id:
                        set_subscription_id = self.env['ir.config_parameter'].set_param("o2b_subscription_id", subscription_id)
                    if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                        set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date.date().strftime("%Y-%m-%d"))
                    else:
                        set_date = self.env['ir.config_parameter'].sudo().create({
                            'key': 'o2b_expire_date',
                            'value': expire_date.date().strftime("%Y-%m-%d")
                            })
                else:
                    if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                        set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date.date().strftime("%Y-%m-%d"))
                    else:
                        set_date = self.env['ir.config_parameter'].sudo().create({
                            'key': 'o2b_expire_date',
                            'value': expire_date.date().strftime("%Y-%m-%d")
                            })
            else:
                subscription_id = self.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
                if subscription_id:
                    set_subscription_id = self.env['ir.config_parameter'].set_param("o2b_subscription_id", subscription_id)
                else:
                    set_subscription_id = self.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_subscription_id',
                        'value': 'trial'
                        })


                

        if subscription_id and subscription_id == 'trial':
            expire_values = self.env['ir.config_parameter'].sudo().get_param('database.create_date')
            if expire_values:
                datetime_create_date = datetime.strptime(expire_values, '%Y-%m-%d %H:%M:%S')
                expire_date = datetime_create_date.date() + relativedelta(months=0)
                expire_date = expire_date.strftime("%Y-%m-%d")
                if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                    set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date)
                else:
                    set_date = self.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_expire_date',
                        'value': expire_date
                        })
            else:
                module_obj = self.env['ir.module.module'].search([('name','=','web_o2b_responsive')], limit=1)
                if module_obj:
                    create_date = module_obj.create_date.strftime("%Y-%m-%d %H:%M:%S")
                    set_date = self.env['ir.config_parameter'].sudo().create({
                        'key': 'database.create_date',
                        'value': create_date
                        })
                    datetime_create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
                    expire_date = datetime_create_date.date() + relativedelta(months=0)
                    expire_date = expire_date.strftime("%Y-%m-%d")
                    if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                        set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date)
                    else:
                        set_date = self.env['ir.config_parameter'].sudo().create({
                            'key': 'o2b_expire_date',
                            'value': expire_date
                            })
            base_domain = IrParamSudo.get_param('base_domain')
            # url = base_domain + "/o2b/subscription_date"
            # dbuuid = IrParamSudo.get_param('database.uuid')

            # payload = {
            #     "params":{
            #         "subscription_id": 'trial',
            #         "dbuuid": dbuuid
            #     }
            # }
            # payload = json.dumps(payload)
            # headers = {
            #   'Content-Type': 'application/json'
            # }
            # response = requests.request("POST", url, headers=headers, data = payload)
            # values = response.json()
            # if values.get('result'):
            #     date_string = values.get('result')
            #     expire_date = datetime.strptime(date_string.replace('"',''), '%m/%d/%Y')
            #     set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date)

        if not subscription_id:
            subscription_id = self.env['ir.config_parameter'].sudo().create({
                'key': 'o2b_subscription_id',
                'value': 'trial'
                })
            expire_values = self.env['ir.config_parameter'].sudo().get_param('database.create_date')
            if expire_values:
                datetime_create_date = datetime.strptime(expire_values, '%Y-%m-%d %H:%M:%S')
                expire_date = datetime_create_date.date() + relativedelta(months=0)
                expire_date = expire_date.strftime("%Y-%m-%d")
                if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                    set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date)
                else:
                    set_date = self.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_expire_date',
                        'value': expire_date
                        })
                    set_base_domain = self.env['ir.config_parameter'].sudo().create({
                        'key': 'base_domain',
                        'value': 'https://crm.o2btechnologies.com'
                        })

            else:
                module_obj = self.env['ir.module.module'].search([('name','=','web_o2b_responsive')], limit=1)
                if module_obj:
                    create_date = module_obj.create_date.strftime("%Y-%m-%d %H:%M:%S")
                    set_date = self.env['ir.config_parameter'].sudo().create({
                        'key': 'database.create_date',
                        'value': create_date
                        })
                    datetime_create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
                    expire_date = datetime_create_date.date() + relativedelta(months=0)
                    expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
                    if self.env['ir.config_parameter'].sudo().get_param('o2b_expire_date'):
                        set_date = self.env['ir.config_parameter'].sudo().set_param("o2b_expire_date", expire_date)
                    else:
                        set_date = self.env['ir.config_parameter'].sudo().create({
                            'key': 'o2b_expire_date',
                            'value': expire_date
                            })
                        set_base_domain = self.env['ir.config_parameter'].sudo().create({
                            'key': 'base_domain',
                            'value': 'https://crm.o2btechnologies.com'
                            })
        return True

class ResUsers(models.Model):
    _inherit = 'res.users'

    chatter_position = fields.Selection([
        ('normal', 'Normal'),
        ('sided', 'Sided'),
    ], string="Chatter Position", default='normal')
    barcode_for_app = fields.Char("Barcode For App")
    barcode_image = fields.Binary("Barcode Image", attachment=True, store=True)
    full_barcode = fields.Char("Barcode")

    def write(self, vals):
        N = 12
        if 'password' in vals:
            res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
            barcode_random = randint(1000000, 9999999)
            vals['barcode_for_app'] = res
            enc = crypt_context.hash(str(barcode_random))
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            vals['full_barcode'] = base_url+'/web/barcodelogin?barcode='+enc+'+/-'+res
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
            qr.add_data(base_url+'/web/barcodelogin?barcode='+enc+'+/-'+res)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            vals['barcode_image'] = qr_image
        rec = super(ResUsers, self).write(vals)
        return rec

    def __init__(self, pool, cr):
        """Override of __init__ to add access rights.
        Access rights are disabled by default, but allowed on some specific
        fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        super(ResUsers, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(["chatter_position"])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(["chatter_position"])


# class ResUsers(models.Model):
#     _inherit = "res.users"

#     chatter_position = fields.Selection(
#         [("normal", "Normal"), ("sided", "Sided")],
#         default="sided",
#     )

#     """Override to add access rights.
#     Access rights are disabled by default, but allowed on some specific
#     fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
#     """

#     @property
#     def SELF_READABLE_FIELDS(self):
#         return super().SELF_READABLE_FIELDS + ["chatter_position"]

#     @property
#     def SELF_WRITEABLE_FIELDS(self):
#         return super().SELF_WRITEABLE_FIELDS + ["chatter_position"]
