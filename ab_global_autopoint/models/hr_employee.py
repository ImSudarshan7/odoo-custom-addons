# -*- coding: utf-8 -*-
##############################################################################

from odoo import models, fields, api, _


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    is_technician = fields.Boolean(string='Is Technician')
    is_supervisor = fields.Boolean(string='Is Supervisor')
