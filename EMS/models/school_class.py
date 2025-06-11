from odoo import models, fields, api, _

class Schoolclass(models.Model):
    _name='school.class'
    _description='School Class'

    name=fields.Char(string='Class Name', required=True)

class Schoolmedium(models.Model):
    _name='school.medium'
    _description='School Medium'
    _rec_name='medium'

    medium = fields.Char(string='Medium', required=True)

class Schoolname(models.Model):
    _name='school.name'
    _description='School Name'
    _rec_name='name'

    name = fields.Char(string='School Name', required=True)