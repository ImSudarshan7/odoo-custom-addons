# -*- coding: utf-8 -*-

# import json
# from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang
# from odoo.tools import amount_to_text_en

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.move'
    _description = "Invoice"

    vehicle_num = fields.Many2one('vehicle.create', string='Vehicle Number',
                                  copy=True, required=0, track_visibility='always')
    transcation_date = fields.Datetime(string='Transcation Date', editable=True)