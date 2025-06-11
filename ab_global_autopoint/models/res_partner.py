from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    @api.constrains('mobile')
    def check_mobile(self):
        if self.mobile:
            for rec in self:
                if not re.match("^[0-9]{10}$", rec.mobile):
                    raise ValidationError(_('The mobile number cannot contain character other than number and must be ten digits'))

    # @api.constrains('name')
    # def check_name(self):
    #     for rec in self:
    #         if re.search(r'\d', rec.name):
    #             raise ValidationError(_('The Name of Person cannot contain number'))

    @api.onchange('name')
    def caps_name(self):
        if self.name:
            self.name = str(self.name).title()