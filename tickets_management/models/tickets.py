from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random
import string
import requests


class TicketsManagement(models.Model):
    _name = 'ticket.management'
    _description = 'Ticket Module'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'random_ticket'

     # Core Fields

    team_id = fields.Many2one('ticket.team', string='Team')

    employee_ids = fields.Many2many(
        'hr.employee',
        related='team_id.employee_ids',
        string='Team Members',
        readonly=True
    )

    employee_ids_id = fields.Many2one(
        'hr.employee',
        string='Assign User',
        domain="[('id', 'in', employee_ids)]"
    )

    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user,tracking=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company,tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)

    customer_id = fields.Many2one('res.partner', string='Customer', default=lambda self: self.env.user.partner_id,tracking=True)
    ticket_type = fields.Many2one('ticket.type', string='Ticket Type')

    priority = fields.Selection([
        ('urgent', 'P1-Urgent'),
        ('high', 'P2-High'),
        ('medium', 'P3-Medium'),
        ('low', 'P4-Low'),

    ],store=True, tracking=True,required=True)

    def action_open_priority_wizard(self):
        return {
            'name': 'Change Priority',
            'type': 'ir.actions.act_window',
            'res_model': 'priority.change.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
    # Menu Fields
    parent = fields.Many2one('solution.type', string='Parent Module')
    child_menu = fields.Many2one('menu.module', string='Child Module', domain="[('parent_id', '=', parent)]")
    grandchild_menu = fields.Many2one('menu.option', string='Grandchild Module',domain="[('child_id', '=', child_menu)]")

    child_menu_ids = fields.Many2many('menu.module', string='Child Menus')

    grandchild_menu_ids = fields.Many2many('menu.option', string='Grandchild Menus')

    # State Fields
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('acknowledgement', 'Acknowledgement'),
        ('work_in', 'Work In Progress'),
        ('work_out', 'Work Delivered'),
        ('client_feedback', 'Client Feedback'),
        ('closed', 'Closed'),
    ], default='draft', tracking=True)

    # Remark Fields
    remark = fields.Text(string='Remarks', required=True, tracking=True, store=True)
    all_remarks = fields.Text("All Remarks", compute='_compute_all_remarks', store=True)

    @api.depends('remark')
    def _compute_all_remarks(self):
        stages = self.state
        for record in self:
            if record.remark:
                remark_count = len(record.all_remarks.split("\n")) if record.all_remarks else 0
                stage_label = stages[remark_count] if remark_count < len(stages) else "Extra Remark"
                new_remark = f"{self.state}: {self.env.user.name}: {record.remark}"
                record.all_remarks = (record.all_remarks + "\n" if record.all_remarks else "") + new_remark

    # Date Fields
    create_date = fields.Datetime(string='Created Date', default=fields.Datetime.now, store=True)
    last_stage_update = fields.Datetime(string='Last Stage Update')

    assigned_date = fields.Datetime(string='Assigned Date', default=fields.Datetime.now)
    feedback_date = fields.Datetime(string='Feedback Date')
    closed_date = fields.Datetime(string='Closed Date')

    # other information
    phone = fields.Char(string='Phone Number', compute='_compute_phone', store=True)

    @api.depends('customer_id.phone')
    def _compute_phone(self):
        for rec in self:
            rec.phone = rec.customer_id.phone if rec.customer_id else ''

    email = fields.Char(string='Email', compute='_compute_email', store=True)

    @api.depends('customer_id')
    def _compute_email(self):
        for record in self:
            record.email = record.customer_id.email if record.customer_id else ''

    description = fields.Html(string='Description', store=True)
    customer_rating = fields.Selection(selection=[
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent')
    ],
        string="Customer Rating?",
        help="Rating given to the customer."
    )
    comment = fields.Text(string="Comment", help="Additional comments or feedback about the customer.")

    # Image Attachments Fields
    capture_images = fields.One2many('image.storage', 'image_id', string='Attached Images', store=True, tracking=True)

    # Random Code and Sequence Fields
    random_code = fields.Char(string='Random Code', readonly=True)
    sequence_number = fields.Integer(string='Sequence Number', default=1)
    random_ticket = fields.Char(string='Random Ticket', readonly=True)

#SLA POLICY

    respond_deadline = fields.Datetime(string='Respond Deadline', compute='_compute_deadline', store=True,
                                       readonly=True)
    resolve_deadline = fields.Datetime(string='Resolve Deadline', compute='_compute_deadline', store=True,
                                       readonly=True)
    sla_response_status = fields.Char(string='SLA  Response Status', store=True, readonly=True)
    sla_resolve_status = fields.Char(string='SLA Resolve Status', store=True, readonly=True)


    @api.depends('priority')
    def _compute_deadline(self):
        for record in self:
            if record.priority:
                now = datetime.now()
                if record.priority == 'urgent':
                    record.respond_deadline = now + timedelta(minutes=30)
                    record.resolve_deadline = now + timedelta(hours=6)
                elif record.priority == 'high':
                    record.respond_deadline = now + timedelta(hours=1)
                    record.resolve_deadline = now + timedelta(hours=8)
                elif record.priority == 'medium':
                    record.respond_deadline = now + timedelta(hours=1)
                    record.resolve_deadline = now + timedelta(hours=36)
                elif record.priority == 'low':
                    record.respond_deadline = now + timedelta(hours=2)
                    record.resolve_deadline = now + timedelta(hours=48)
            else:
                record.respond_deadline = False
                record.resolve_deadline = False

    @api.model
    def auto_change_sla_respond_status(self):
        records = self.env['ticket.management'].search([])
        for record in records:
            now = fields.Datetime.now()
            sla_pass_respond = False
            # Only check the SLA status for 'open' state or after
            if record.state in ['open', 'acknowledgement', 'work_in', 'work_out', 'client_feedback',
                                'closed'] and record.respond_deadline:
                sla_pass_respond = now <= record.respond_deadline  # Respond deadline must be before or equal to now

            if record.state in ['open', 'acknowledgement', 'work_in', 'work_out', 'client_feedback',
                                'closed']:  # Update SLA status if the state is any after 'open'
                if sla_pass_respond:
                    record.sla_response_status = 'SLA RESPOND DONE'
                else:
                    record.sla_response_status = 'SLA RESPOND INCOMPLETE'


    def auto_change_sla_resolve_status(self):
        records = self.env['ticket.management'].search([])
        for record in records:
            now = fields.Datetime.now()
            sla_pass_resolve = False
            # Only check the SLA status for 'closed' state
            if record.state == 'closed' and record.resolve_deadline:
                sla_pass_resolve = now <= record.resolve_deadline

            if record.state == 'closed':  # Only update SLA status if the state is 'closed'
                if sla_pass_resolve:
                    record.sla_resolve_status = 'SLA RESOLVE DONE'
                else:
                    record.sla_resolve_status = 'SLA RESOLVE INCOMPLETE'

    sla_status_done_count = fields.Integer(
        string="SLA Status Done Count",
        compute='_compute_sla_status_done_count',
        store=True
    )

    @api.depends('sla_response_status', 'sla_resolve_status')
    def _compute_sla_status_done_count(self):
        for record in self:
            # Search for records where both SLA statuses are "DONE"
            done_records = self.env['ticket.management'].search([
                ('sla_response_status', '=', 'SLA RESPOND DONE'),
                ('sla_resolve_status', '=', 'SLA RESOLVE DONE')
            ])
            # Set the count to the number of matching records
            record.sla_status_done_count = len(done_records)


    # State Management Methods
    def action_confirm(self):
        self._check_state('draft', 'open', "Only draft tickets can be confirmed.")
        if self.user_id and self.user_id.partner_id:
            self.message_notify(
                partner_ids=[self.user_id.partner_id.id],
                subject="Ticket confirmed",
                body=f"The ticket number {self.random_ticket} has been confirmed.",
                type="notification",
            )

    def action_done(self):
        self._check_state('acknowledgement', 'work_in', "Please assign the ticket first!")
        if self.employee_ids_id:
            # Send in-app notification
            self.message_notify(
                partner_ids=[self.employee_ids_id.user_id.partner_id.id],  # Notify the user linked to the employee
                subject="Ticket Assigned",
                body=f"The ticket number {self.random_ticket} has been assigned to you.",
                type="notification",
            )

    def action_complete(self):
        self._check_state('work_in', 'work_out', "Please check the ticket first!")

    def action_closed(self):
        self._check_state('client_feedback', 'closed', "Only client feedback tickets can be closed.")
        if self.user_id and self.user_id.partner_id:
            self.message_notify(
                partner_ids=[self.user_id.partner_id.id],
                subject="Ticket confirmed",
                body=f"The ticket number {self.random_ticket} has been Closed.",
                type="notification",
            )
        return {
            'effect': {

                'message': 'Boom!!!!!! Your Ticked has Been Closed!!!',
                'type': 'rainbow_man',
            }
        }

    # for email
    def action_send_email(self):
        template = self.env.ref('tickets_management.ticket_mail_template')
        for rec in self:
            if rec.customer_id.email:  # Corrected to use `rec` instead of `self`
                email_values = {
                    'email_cc': False,
                    'auto_delete': True,
                    'recipient_ids': [],
                    'partner_ids': [],
                    'scheduled_date': False,
                }
                template.send_mail(rec.id, force_send=True, email_values=email_values)
            else:
                raise UserError("Email not found for record: %s" % rec.random_ticket)

    def get_signup_url(self):
        """Generate URL to open the specific ticket"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/web#id={self.id}&model=ticket.management&view_type=form"

    def action_open(self):
        self._check_state('client_feedback', 'draft', "Only client feedback tickets can be closed.")

    def action_assign(self):
        self._check_state('open', 'acknowledgement', "Please confirm the ticket first.")

    def action_acknowledgement(self):
        self._check_state('open', 'work_in', "Please confirm the ticket first.")

    def action_feedback(self):
        self._check_state('work_out', 'client_feedback', "Please deliver the work first.")

    def _check_state(self, required_state, new_state, error_message):
        for ticket in self:
            if ticket.state != required_state:
                raise UserError(error_message)
            ticket.state = new_state

    # Create and Write Methods
    # @api.model
    # def create(self, vals):
    #     vals['random_code'] = self.generate_random_code
    #     if 'sequence_number' not in vals:
    #         vals['sequence_number'] = self.search_count([]) + 1
    #     record = super().create(vals)
    #     record.random_ticket = record.generate_random_ticket()
    #     return record
    @api.model
    def create(self, vals):
        vals['random_code'] = self.generate_random_code
        if vals.get("random_ticket", "New") == "New":
            vals["random_ticket"] = self.env["ir.sequence"].next_by_code("ticket.management") or 'New'

        return super(TicketsManagement, self).create(vals)

    def write(self, vals):
        if 'state' in vals:
            vals['last_stage_update'] = fields.Datetime.now()

            if vals['state'] == 'closed':
                vals['closed_date'] = fields.Datetime.now()

            if vals['state'] == 'client_feedback':
                vals['feedback_date'] = fields.Datetime.now()

            if vals.get('state') != 'closed' and self.state != 'closed':
                vals['remark'] = ''
            # if vals['state'] != self.state:
            #     vals['remark'] = ''  # Clear remarks if the state changes
        return super().write(vals)

    # Utility Methods
    @property
    def generate_random_code(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=4))
        last_letter = random.choice(string.ascii_uppercase)
        return f"{letters}{digits}{last_letter}"

    def generate_random_ticket(self):
        company_name = ''.join([word[0] for word in self.env.company.name.split() if word]).upper()
        digits_part = f"{self.sequence_number:04d}"
        return f"{company_name}-{digits_part}"

    @api.model
    def auto_close_tickets(self):
        # Get the current time and subtract 2 minutes to find tickets to close
        now = fields.Datetime.now()  # Get the current date and time
        two_days_ago = now - timedelta(days=2)  # Get the time from 2 minutes ago

        # Find all tickets in 'client_feedback' state with a feedback_date older than 2 minutes
        tickets_to_close = self.search([
            ('state', '=', 'client_feedback'),
            ('feedback_date', '<=', two_days_ago),
        ])

        # Close tickets that meet the criteria
        for ticket in tickets_to_close:
            ticket.write({
                'state': 'closed',  # Update the ticket state to 'closed'
                'closed_date': now  # Optionally, set the closed date to now
            })