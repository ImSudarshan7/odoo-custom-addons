from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class AuditSession(models.Model):
    _name = 'audit.session'
    _description = 'Audit Session'

    name = fields.Char(string='Session Name', default="/", copy=False, readonly=True)
    auditor_id = fields.Many2one(
        'res.users', string='Auditor', required=True, default=lambda self: self.env.user)
    location_id = fields.Many2one(
        'audit.location', string='Location', required=True, domain="[('auditor_ids', 'in', [uid])]")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], string='Status', default='draft', required=True)
    session_date = fields.Date(
        string='Session Date', default=fields.Date.today, required=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    session_line_ids = fields.One2many(
        'audit.session.line', 'session_id', string='Audit Lines')
    
    @api.model
    def default_get(self, fields_list):
        """Automatically assign the first location assigned to the user"""
        defaults = super(AuditSession, self).default_get(fields_list)
        
        user = self.env.user
        assigned_locations = self.env['audit.location'].search([('auditor_ids', 'in', user.id)], limit=1)
        
        if assigned_locations:
            defaults['location_id'] = assigned_locations.id
        
        return defaults
    
    @api.model
    def create(self, vals):
        """Generate a session name based on Date, Auditor, and Location"""
        existing_sessions = self.env['audit.session'].sudo().search([
            ('auditor_id', '=', vals.get('auditor_id')),
            ('state', 'not in', ['completed']),
        ])
        if existing_sessions:
            raise ValidationError('You cannot create a new session as there is an existing session that is not completed for this auditor.')

        record = super(AuditSession, self).create(vals)  # Create record first
        
        if record.auditor_id and record.location_id and record.session_date:
            session_date = record.session_date.strftime('%d-%m-%Y')
            record.name = f"Audit {session_date} - {record.auditor_id.name} - {record.location_id.name}"
        
        return record

    def start_audit(self):
        """
        Assigns items dynamically based on priority and starts the audit session.
        """
        if self.state != 'draft':
            raise ValidationError("Only draft sessions can be started.")

        uncompleted_items = self.env['audit.item'].sudo().search([
            ('location_id', '=', self.location_id.id),
            ('is_assigned', '=', False),
            ('audit_not_required', '=', False),
            ('audit_completed', '=', False)
        ])
        
        if not uncompleted_items:
            self.sudo().location_id.item_ids.write({'audit_completed': False})
            uncompleted_items = self.env['audit.item'].sudo().search([
                ('location_id', '=', self.location_id.id),
                ('is_assigned', '=', False),
                ('audit_not_required', '=', False),
                ('audit_completed', '=', False)
            ])

        def sort_key(item):
            if item.item_type == 'fast':
                return (1, -item.total_value)
            elif item.item_type == 'slow':
                return (2, -item.total_value)
            elif not item.last_audit_date:
                return (3, -item.total_value)
            elif item.last_audit_status in ('mismatch_short', 'mismatch_excess'):
                return (4, -item.total_value)
            return (5, -item.total_value)

        sorted_items = sorted(uncompleted_items, key=sort_key)

        items_to_assign = self.sudo().location_id.items_to_assign
        assigned_items = sorted_items[:items_to_assign]

        if not assigned_items:
            raise ValidationError("No items available for assignment.")

        for item in assigned_items:
            self.env['audit.session.line'].sudo().create({
                'session_id': self.id,
                'item_id': item.id,
            })
            item.is_assigned = True
            item.auditor_id = self.auditor_id.id
            
        self.sudo().start_date = datetime.now()
        self.sudo().state = 'in_progress'

    def complete_audit(self):
        """Marks the session as 'Completed' only if all lines are audited."""
        non_audited_lines = self.sudo().session_line_ids.filtered(lambda line: line.state != 'audited')
        if non_audited_lines:
            non_audited_lines.sudo().unlink()

        self.sudo().end_date = datetime.now()
        self.sudo().write({'state': 'completed'})


class AuditSessionLine(models.Model):
    _name = 'audit.session.line'
    _description = 'Audit Session Line'

    session_id = fields.Many2one(
        'audit.session', string='Audit Session', required=True, ondelete='cascade')
    item_id = fields.Many2one('audit.item', string='Item', required=True)
    system_qty = fields.Float(
        string='System Quantity', compute='_compute_system_qty', store=True)
    audited_qty = fields.Float(string='Audited Quantity')
    audit_status = fields.Selection([
        ('verified', 'Verified'),
        ('mismatch_short', 'Mismatched Short'),
        ('mismatch_excess', 'Mismatched Excess')
    ], string='Audit Status', compute='_compute_audit_status', store=True)
    remarks = fields.Text(string='Remarks')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('audited', 'Audited'),
    ], string='Line Status', default='draft')

    @api.depends('item_id.inventory_qty', 'state')
    def _compute_system_qty(self):
        """
        Computes the `system_qty` field. If the line is in 'draft', it takes the value 
        from `item_id.inventory_qty`. If the line is 'audited', it retains the last value.
        """
        for line in self:
            if line.state == 'draft' and line.item_id:
                line.system_qty = line.item_id.inventory_qty

    @api.depends('audited_qty', 'system_qty')
    def _compute_audit_status(self):
        """
        Computes the `audit_status` based on the comparison of `audited_qty` and `system_qty`.
        """
        for line in self:
            if line.audited_qty == line.system_qty:
                line.audit_status = 'verified'
            elif line.audited_qty < line.system_qty:
                line.audit_status = 'mismatch_short'
            elif line.audited_qty > line.system_qty:
                line.audit_status = 'mismatch_excess'
            else:
                line.audit_status = False

    def mark_as_audited(self):
        """Marks the line as audited, creates logs, and updates the item."""
        if not self.audited_qty:
            raise ValidationError(
                "Please enter the Audited Quantity before marking the line as audited.")

        self.env['audit.log'].sudo().create({
            'item_id': self.item_id.id,
            'audit_date': fields.Date.today(),
            'auditor_id': self.session_id.auditor_id.id,
            'remarks': self.remarks,
            'audit_status': self.audit_status,
            'system_qty': self.system_qty,
            'audited_qty': self.audited_qty,
        })

        self.item_id.sudo().write({
            'last_audit_date': fields.Date.today(),
            'last_audit_status': self.audit_status,
            'is_assigned': False,
            'audit_completed': True,
        })

        self.sudo().write({'state': 'audited'})
