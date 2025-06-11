from odoo import models, api, fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class TicketType(models.Model):
    _name = 'ticket.type'
    _description = 'Ticket Type'
    _rec_name = 'ticket_type_id'
    ticket_type_id = fields.Char(string='Ticket Type')


class SolutionType(models.Model):
    _name = 'solution.type'
    _description = 'Solution Type'

    name = fields.Char(string="Parent Name", required=True)
    child_ids = fields.One2many('menu.module', 'parent_id', string="Children")


class MenuModule(models.Model):
    _name = 'menu.module'
    _description = 'Menu Module'

    name = fields.Char(string="Child Name", required=True)
    parent_id = fields.Many2one('solution.type', string="Parent", ondelete='cascade', required=True)
    grandchild_ids = fields.One2many('menu.option', 'child_id', string="Grandchildren")


class MenuOption(models.Model):
    _name = 'menu.option'
    _description = 'Menu Option'

    name = fields.Char(string="Grandchild Name", required=True)
    child_id = fields.Many2one('menu.module', string="Child", ondelete='cascade', required=True)


class TaskSchedule(models.Model):
    _name = 'sla.policy'
    _rec_name = 'sla_name'
    sla_name = fields.Char(string='Name', required=True)
    sla_name_id = fields.Many2one('sla.policy', string="Tags", ondelete='cascade')

    description = fields.Text()
    note = fields.Text(string='Note')
    minutes = fields.Integer(string='Minutes')
    days = fields.Integer(string='Days')
    hours = fields.Integer(string='Hours')
    working_hours = fields.Many2one(
        'resource.calendar',
        string="Working Hours",
        help="Define the working hours schedule."
    )
    priority = fields.Selection([
        ('p4', 'P3-Low'),
        ('p3', 'P3-Normal'),
        ('p2', 'P2-Important'),
        ('p1', 'P1-Urgent'),
    ], tracking=True,)


class ImageStorage(models.Model):
    _name = 'image.storage'
    _description = 'Image Storage'
    _rec_name = 'capture_image'

    capture_image = fields.Binary(string='Attached Image', store=True)
    image_id = fields.Many2one('ticket.management', string='Image List')

    @api.model
    def create(self, vals):
        res = super(ImageStorage, self).create(vals)
        # Create an attachment when a new image is added
        if res.capture_image:
            self._create_attachment(res)
        return res

    def write(self, vals):
        res = super(ImageStorage, self).write(vals)
        # Create an attachment if an image is added or updated
        for record in self:
            if 'capture_image' in vals and vals['capture_image']:
                self._create_attachment(record)
        return res

    def _create_attachment(self, image_record):
        # Create an attachment record
        attachment = self.env['ir.attachment'].create({
            'name': f"Image for {image_record.image_id.capture_images if image_record.image_id else 'Unknown'}",
            'type': 'binary',
            'datas': image_record.capture_image,  # The binary image field
            'res_model': 'ticket.management',
            'res_id': image_record.image_id.id,  # Link the attachment to the related ticket
        })
        return attachment


class PriorityChangeWizard(models.TransientModel):
    _name = 'priority.change.wizard'
    _description = 'Priority Change Wizard'

    reason = fields.Text(string="Reason", required=True,store=True)

    def confirm_priority_change(self):
        active_id = self.env.context.get('active_id')
        if not active_id:
            raise UserError("No active record found to change the priority.")

        record = self.env['ticket.management'].browse(active_id)
        record.message_post(
            body=f"Priority change reason: {self.reason}",
            subject="Priority Change:"
        )
        record.write({'priority': False})

