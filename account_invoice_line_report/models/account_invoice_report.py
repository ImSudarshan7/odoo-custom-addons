from odoo import fields, api, models

class AccountInvoiceReportInherit(models.Model):

    _inherit="account.invoice.report"

    invoice_sequence = fields.Char(
        string='Invoice Sequence',
        readonly=True
    )

    def _select(self):
        # Add invoice_sequence to the SELECT clause
        return super(AccountInvoiceReportInherit, self)._select() + """
            , move.invoice_sequence AS invoice_sequence
        """

    def _from(self):
        # Prevent duplicate LEFT JOINs for account_move
        from_clause = super(AccountInvoiceReportInherit, self)._from()
        if 'account_move move' not in from_clause:
            from_clause += """
                LEFT JOIN account_move move ON move.id = account_move_line.move_id
            """
        return from_clause