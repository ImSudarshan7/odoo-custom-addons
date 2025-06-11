from odoo import models, api, fields

class Team(models.Model):

    _name = "ticket.team"
    _description = "Ticket Team"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='name'

    name = fields.Char(required=True)

    name_id = fields.Many2one('ticket.team', string="Team", ondelete='cascade')

    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, tracking=True)

    email=fields.Char(string='Email')

    employee_ids = fields.Many2many('hr.employee', string='Member')
