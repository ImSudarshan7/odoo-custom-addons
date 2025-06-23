# -*- coding: utf-8 -*-

import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import  timedelta,date,time
import datetime
from odoo.http import request
import re

class IrdReport(models.TransientModel):
    _name = "ird.report"

    from_date = fields.Date('Start Date',required='True',default=date.today())
    to_date = fields.Date('End date',required='True',default=date.today())

    def print_ird_report(self):
        """Redirects to the report with the values obtained from the wizard
        'data['form']': name of employee and the date duration"""
        data = {
            'start_date': self.from_date,
            'end_date': self.to_date,
        }
        return self.env.ref('ird_report.action_report_print_ird').report_action(self, data=data)


    


