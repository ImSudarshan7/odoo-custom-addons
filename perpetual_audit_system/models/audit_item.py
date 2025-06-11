from odoo import models, fields, api


class AuditItem(models.Model):
    _name = 'audit.item'
    _description = 'Audit Items'
    _rec_name = 'item_name'

    item_code = fields.Char(string='Item Code', required=True)
    item_name = fields.Char(string='Item Name', required=True)
    item_category = fields.Char(string='Item Category', required=True)
    item_type = fields.Selection([
        ('fast', 'Fast Moving'),
        ('slow', 'Slow Moving'),
        ('non', 'Non-Moving')
    ], default="fast", string='Type', required=True)
    inventory_qty = fields.Float(string='Inventory Quantity')
    mrp_amount = fields.Float(string='MRP')
    total_value = fields.Float(
        string="Total Value", compute="_compute_total_value", store=True)
    scale_unit = fields.Char(string='Scale Unit')
    bin_no = fields.Char(string='BIN No', default='0')
    last_sync_date = fields.Date(string='Last Sync Date')
    last_audit_date = fields.Date(string='Last Audit Date')
    last_audit_status = fields.Selection([
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('mismatch_short', 'Mismatched Short'),
        ('mismatch_excess', 'Mismatched Excess'),
        ('overdue', 'Overdue')
    ], string='Last Audit Status', default='pending')
    audit_not_required = fields.Boolean(
        string='Audit Not Required', default=False)
    location_id = fields.Many2one('audit.location', string='Location')
    auditor_id = fields.Many2one('res.users', string='Assigned Auditor')
    audit_log_ids = fields.One2many(
        'audit.log', 'item_id', string='Audit Log')
    is_assigned = fields.Boolean(string='Is Assigned', default=False)
    audit_completed = fields.Boolean(string="Audit Completed", default=False)

    @api.depends('mrp_amount', 'inventory_qty')
    def _compute_total_value(self):
        for rec in self:
            rec.total_value = rec.inventory_qty * rec.mrp_amount
