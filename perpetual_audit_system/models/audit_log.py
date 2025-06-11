from odoo import models, fields, api

class AuditLog(models.Model):
    _name = 'audit.log'
    _description = 'Audit Log'

    item_id = fields.Many2one('audit.item', string='Item', required=True)
    audit_date = fields.Date(string='Audit Date', required=True)
    auditor_id = fields.Many2one('res.users', string='Auditor')
    remarks = fields.Text(string='Remarks')
    audit_status = fields.Selection([
        ('verified', 'Verified'),
        ('mismatch_short', 'Mismatched Short'),
        ('mismatch_excess', 'Mismatched Excess'),
    ], string='Audit Status', required=True)
    system_qty = fields.Float(string='System Quantity', required=True)
    audited_qty = fields.Float(string='Audited Quantity', required=True)
