# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo import api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    area_id = fields.Many2one(comodel_name="salesperson.area", string="Area", required=False)
    day_selection = fields.Selection(string="Day", selection=[('monday', 'Monday'),
                                                              ('tuesday', 'Tuesday'),
                                                              ('wednesday', 'Wednesday'),
                                                              ('thursday', 'Thursday'),
                                                              ('friday', 'Friday'),
                                                              ('saturday', 'Saturday'),
                                                              ('sunday', 'Sunday')], required=False,
                                     )

    user_type = fields.Selection(string="User Type", required=True,
                                 selection=[('customer', 'Customer'),
                                            ('user', 'User')],
                                 default='customer')

    @api.model
    def create(self, vals):
        self.clear_caches()
        return super(ResPartnerInherit, self).create(vals)

    def write(self, vals):
        self.clear_caches()
        return super(ResPartnerInherit, self).write(vals)

    # current_user = fields.Many2one('res.users', compute='_get_current_user', default=1)

    # @api.depends()
    # def _get_current_user(self):
    #     for rec in self:
    #         rec.current_user = self.env.user

    #     self.update({'current_user': self.env.user.id})

    # current_user = fields.Many2one("res.users", string="Current User", readonly=True,
    #                                default=lambda self: self.env.user)


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    sale_person_area = fields.Many2many("salesperson.area", string="Salesperson Area", )

    @api.model
    def create(self, vals):
        self.clear_caches()
        new_rec = super(ResUserInherit, self).create(vals)
        new_rec.partner_id.user_type = 'user'

        return new_rec

    def write(self, vals):
        self.clear_caches()
        return super(ResUserInherit, self).write(vals)

    def get_user_wise_contact(self):
        self.clear_caches()
        record = self.env['res.partner'].sudo().search(
            ['|', ('area_id', 'in', self.sale_person_area.ids),
             ('area_id', '=', False)]).ids
        record_users = self.env['res.partner'].sudo().search(
            ['|', ('user_type', '=', 'user'), ('user_type', '=', False)]).ids

        # print(record)
        # print('uper wala partner ')
        # print (record_users)

        users = self.env['res.users'].sudo().search([]).mapped('partner_id').ids

        # print(users)
        # print('upser wala partner users')

        final_list = []
        final_list = record + users + record_users

        # print(record)
        # print(users)
        # print(sorted(set(final_list)))
        # print("____")

        final_list = sorted(set(final_list))
        return final_list
