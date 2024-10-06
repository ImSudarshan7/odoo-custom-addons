from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_location = fields.Selection([
        ('ktm', 'Kathmandu Office'),
        ('sif', 'Simara Office')
    ], string='Invoice Location', tracking=True,
        help="Select the office location where this invoice is being processed.", required=True)

    invoice_sequence = fields.Char('Invoice Sequence', tracking=True,
                                   help="Automatically generated sequence based on the invoice location.", required=True)

    @api.onchange('invoice_location')
    def _onchange_location_invoice(self):
        for rec in self:
            domain = [('warehouse_id.name', 'ilike', 'Kathmandu')] if rec.invoice_location == 'ktm' else [
                ('warehouse_id.name', 'not ilike', 'Kathmandu')]
            data = self.env['stock.picking.type'].search(domain)

            move_type = self._context.get('default_move_type')
            if move_type in ['out_invoice', 'in_invoice']:
                target_code = 'outgoing' if move_type == 'out_invoice' else 'incoming'
                picking_type = data.filtered(lambda p: p.code == target_code)
                if picking_type:
                    rec.picking_type_id = picking_type[0].id

    @api.onchange('invoice_location')
    def _onchange_invoice_location(self):
        """
        Update the invoice sequence based on the selected location.
        - If Kathmandu Office (ktm) is selected, the sequence will be 'KTM/81-82/'.
        - If Simara Office (sif) is selected, the sequence will be 'SIF/81-82/'.
        """
        if self.invoice_location == 'ktm':
            self.invoice_sequence = f'KTM/81-82/'
        elif self.invoice_location == 'sif':
            self.invoice_sequence = f'SIF/81-82/'
        else:
            self.invoice_sequence = ''


    @api.constrains('invoice_sequence', 'invoice_location')
    def _check_invoice_sequence(self):
        """
        Validates that the invoice sequence contains the correct prefix based on the location.
        - Kathmandu: 'KTM/81-82/' 
        - Simara: 'SIF/81-82/'
        Ensures the part after the final '/' is not empty.
        """
        for rec in self:
            if not rec.invoice_sequence:
                continue

            if rec.invoice_location == 'ktm' and not rec.invoice_sequence.startswith('KTM/81-82/'):
                raise ValidationError(
                    _("For Kathmandu location, the invoice sequence must start with 'KTM/81-82/'."))
            elif rec.invoice_location == 'sif' and not rec.invoice_sequence.startswith('SIF/81-82/'):
                raise ValidationError(
                    _("For Simara location, the invoice sequence must start with 'SIF/81-82/'."))

            parts = rec.invoice_sequence.split('/')
            if len(parts) < 3 or not parts[-1]:
                raise ValidationError(
                    _("The invoice sequence must not have an empty part after the final '/'."))
