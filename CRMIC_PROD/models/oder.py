from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    bom_id = fields.Many2one('mrp.bom', string='REF (BOM)')
    date_planned_start = fields.Datetime(string='Production Date')
    number_of_labours = fields.Integer(string='Men Hours', required=True)
    bleached = fields.Boolean(string='Is Bleached')
    remarks = fields.Text(string="Remarks")
