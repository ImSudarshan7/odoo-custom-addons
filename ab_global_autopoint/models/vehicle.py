# -*- coding: utf-8 -*-
##############################################################################

from odoo import models, fields, api, _


class VehicleMake(models.Model):
    _name = 'vehicle.make'
    _rec_name = 'name'
    _inherit = ['mail.thread', ]
    # 'ir.needaction_mixin'
    name = fields.Char(string="Make Name", required=True, track_visibility='always')
    image = fields.Binary(string='Image', store=True, attachment=True, track_visibility='always')


class Vehicle(models.Model):
    _name = 'vehicle.create'
    _rec_name = 'vehicle_no'
    _inherit = ['mail.thread']
    # ir.needaction_mixin'


    name = fields.Char(string="Model Name", required=True, track_visibility='always')
    owner_id = fields.Many2one('res.partner', string="Vehicle Owner", required=False, track_visibility='always')
    image = fields.Binary(string='Image', store=True, attachment=True, track_visibility='always')
    active = fields.Boolean(string="Active", default=True, track_visibility='always')
    odometer = fields.Float(string='Odometer Reading',required=1,help='Odometer Reading',track_visibility='always')
    make_id = fields.Many2one('vehicle.make', string="Make", required=True, track_visibility='always')
    vehicle_no = fields.Char(string="Vehicle Number", required=True, track_visibility='always')
    model_no = fields.Char(string="Model Number", required=0, track_visibility='always')
    chasis_no = fields.Char(string="Chasis Number", required=0, track_visibility='always')
    insurance_company = fields.Char(string="Insurance Company", track_visibility='always')
    insurance_validity = fields.Date(string="Valid Upto", track_visibility='always')


    # @api.model
    # def name_get(self):
    #     res = []
    #     for rec in self:
    #         res.append((rec.id, '%s %s' % (rec.name, rec.vehicle_no)))
    #     return res
