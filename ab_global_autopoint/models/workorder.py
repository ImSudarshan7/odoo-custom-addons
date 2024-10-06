from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import re


class WorkOrder(models.Model):
    _name = 'job.order'
    _inherit = ['mail.thread']
    _description = 'Job Order for Vehicle Servicing'
    _order = 'name'

    @api.model
    def print_report(self):
        return self.env["report"].get_action(self, 'ab_global_autopoint.report_jobcard')

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_set_to_requisition(self):
        for rec in self:
            rec.state = 'to request'

    def action_requisition(self):
        for rec in self:
            rec.state = 'to request'
        if self.odometer:
            self.vehicle_id.odometer = self.odometer

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        if self.odometer:
            self.vehicle_id.odometer = self.odometer

    @api.onchange('customer_id')
    def onchange_customer_id(self):
        for rec in self:
            if rec.customer_id:
                rec.email = rec.customer_id.email
                rec.mobile = rec.customer_id.mobile
                address = ''

                if rec.customer_id.state_id:
                    address += rec.customer_id.state_id.name + ", "

                # if rec.customer_id.address_district:
                #     address += rec.customer_id.address_district + ", "
                #
                # if rec.customer_id.address_local:
                #     address += rec.customer_id.address_local

                # if rec.customer_id.ward_no:
                #     address += "-" + rec.customer_id.ward_no

                if rec.customer_id.street:
                    address += ", " + rec.customer_id.street

                rec.address = address

        return {'domain': {'vehicle_id': [('owner_id.id', '=', rec.customer_id.id)]}}

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        for rec in self:
            if rec.vehicle_id:
                if rec.vehicle_id.model_no:
                    rec.model_no = rec.vehicle_id.model_no
                if rec.vehicle_id.chasis_no:
                    rec.chasis_no = rec.vehicle_id.chasis_no
                if rec.vehicle_id.insurance_company:
                    rec.insurance_company = rec.vehicle_id.insurance_company
                if rec.vehicle_id.insurance_validity:
                    rec.insurance_validity = rec.vehicle_id.insurance_validity

    # Overriding the create method to assign sequence for the record
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('job.order') or _('New')
        result = super(WorkOrder, self).create(vals)
        return result

    @api.model
    def unlink(self):
        for rec in self:
            # if rec.state == 'to request' or rec.state == 'done' or rec.state == 'requisition':
            raise UserError(_(
                'The Job Order cannot be deleted once it is created.'))
        return super(WorkOrder, self).unlink()

    # @api.depends('vehicle_id')
    # def set_odometer(self):
    #     if self.vehicle_id:
    #         if self.vehicle_id.odometer:
    #             self.last_odometer = self.vehicle_id.odometer

    @api.depends('vehicle_id.odometer')
    def set_odometer(self):
        for record in self:
            if record.vehicle_id and record.vehicle_id.odometer:
                record.last_odometer = record.vehicle_id.odometer
            else:
                record.last_odometer = 0.0  # Set a default value if odometer is not available


    @api.depends('time')
    def compute_time(self):
        if self.time:
            self.result_time = str('{0:02.0f}:{1:02.0f}'.format(*divmod(float(self.time) * 60, 60)))

    @api.constrains('contact_person')
    def check_contact_name(self):
        if self.contact_person:
            for rec in self:
                if re.search(r'\d', rec.contact_person):
                    raise ValidationError(_('The Name of Contact Person cannot contain number'))

    @api.onchange('contact_person')
    def caps_contact_name(self):
        if self.contact_person:
            self.contact_person = str(self.contact_person).title()

    # Fields for Customer
    name = fields.Char(string='Order ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New Joborder'))
    customer_id = fields.Many2one('res.partner', string='Customer', required=1, help='Customer Name',
                                  track_visibility='always', states={'done': [('readonly', True)]})
    address = fields.Char(string='Address', track_visibility='always', states={'done': [('readonly', True)]})
    contact_person = fields.Char(string='Contact Person', help='Contact Person', track_visibility='always',
                                 states={'done': [('readonly', True)]})
    email = fields.Char(string='Email', readonly=0, track_visibility='always', states={'done': [('readonly', True)]})
    mobile = fields.Char(string='Mobile No.', help='Ten Digit Mobile number', track_visibility='always',
                         states={'done': [('readonly', True)]})

    # Fields for Vehicle
    vehicle_id = fields.Many2one('vehicle.create', string='Vehicle', required=1,
                                 help='Choose your Vehicle or Register your Vehicle', track_visibility='always',
                                 states={'done': [('readonly', True)]})
    model_no = fields.Char(string='Engine No.', readonly=0, track_visibility='always',
                           states={'done': [('readonly', True)]})
    chasis_no = fields.Char(string='Chasis No.', readonly=0, track_visibility='always',
                            states={'done': [('readonly', True)]})
    insurance_company = fields.Char(string="Insurance Company", readonly=0, track_visibility='always',
                                    states={'done': [('readonly', True)]})
    insurance_validity = fields.Date(string="Valid Upto", readonly=0, track_visibility='always',
                                     states={'done': [('readonly', True)]})
    last_odometer = fields.Float(string='Last Odometer Reading', required=0, compute='set_odometer',
                                 help='Leave blank if it is your First Servicing')
    odometer = fields.Float(string='Current Odometer Reading', required=1, help='Odometer Reading',
                            track_visibility='always', states={'done': [('readonly', True)]})
    appointment = fields.Selection([
        ('yes', 'YES'),
        ('no', 'NO')
    ], string='Appointment', track_visibility='always', states={'done': [('readonly', True)]})
    estimate = fields.Text(string='Estimate', readonly=0, track_visibility='always')
    dq_no = fields.Char(string='DQ No.', readonly=0, track_visibility='always')
    done_by = fields.Char(string='Done By', readonly=0, track_visibility='always')
    # temp=last_odometer

    # Field for Multi-company
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.user.company_id.id)

    # Fields for Servicing
    service_type = fields.Selection([
        ('paid', 'Paid Service'),
        ('free', 'Free Service'),
        ('pdi', 'Pre-delivery Inspection'),
        ('warranty', 'Warranty'),
        ('ssc', 'Special Service Campaign'),
        ('general', 'General Service')
    ], string='Service Type', track_visibility='always', states={'done': [('readonly', True)]})

    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('Card', 'Card')
    ], string='Payment Method', track_visibility='always', states={'done': [('readonly', True)]})
    date_in = fields.Date(string="Date In", track_visibility='always', states={'done': [('readonly', True)]})
    date_out = fields.Date(string="Promise Del. Date", track_visibility='always', states={'done': [('readonly', True)]})
    time = fields.Float(string='Delivery Time', track_visibility='always', states={'done': [('readonly', True)]})

    result_time = fields.Char(string='Time', compute='compute_time')

    # Instruction Fields
    job_instruction = fields.Text(string="Job Instruction", track_visibility='always',
                                  states={'done': [('readonly', True)]})
    technician_report = fields.Text(string="Technician Report", track_visibility='always',
                                    states={'done': [('readonly', True)]})

    additional_job = fields.Text(string="Additional Job", track_visibility='always',
                                 states={'done': [('readonly', True)]})
    revised_del_date = fields.Date(string="Revised Del. Date", track_visibility='always',
                                   states={'done': [('readonly', True)]})

    ordered_part_lines = fields.One2many('part.order.lines', 'order_id', string=' Ordered Part Lines',
                                         states={'done': [('readonly', True)]})

    # Fields for Technician
    technician_id = fields.Many2one('hr.employee', string="Responsible Technician", track_visibility='always',
                                    states={'done': [('readonly', True)]})
    job_start_time = fields.Datetime(string="Job Start Time", track_visibility='always',
                                     states={'done': [('readonly', True)]})
    job_completion_time = fields.Datetime(string="Job Completion Time", track_visibility='always',
                                          states={'done': [('readonly', True)]})
    recommendation = fields.Text(string="Recommendation", track_visibility='always',
                                 states={'done': [('readonly', True)]})

    # Fields for Supervisor and Inspector
    job_taking_supervisor_id = fields.Many2one('hr.employee', string="Job Taken By", track_visibility='always',
                                               states={'done': [('readonly', True)]})
    final_inspecting_supervisor_id = fields.Many2one('hr.employee', string="Final Inspection Done By",
                                                     track_visibility='always', states={'done': [('readonly', True)]})

    supervisor_remarks = fields.Text(string="Remarks (if Any)", track_visibility='always',
                                     states={'done': [('readonly', True)]})
    inspector_remarks = fields.Text(string="Remarks (if Any)", track_visibility='always',
                                    states={'done': [('readonly', True)]})

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to request', 'Requisition Allowed'),
        ('done', 'Done'),
        ('requisition', 'Requisition Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')


class OrderedPartLines(models.Model):
    _name = 'part.order.lines'
    _description = 'Parts Order Lines'

    part_id = fields.Many2one('product.product', string='Parts Name')
    order_id = fields.Many2one('job.order', string='Order ID')
