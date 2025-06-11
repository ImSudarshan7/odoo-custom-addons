from datetime import datetime
from odoo import models, fields, api
import datetime


class SalesPurchaseExcelReport(models.TransientModel):
    _name = 'report.sale_purchase_reports.reports_sale_purchase'
    _description = 'Sales and Purchase Excel Report'
    _inherit = 'report.report_xlsx.abstract'

    def get_purchase_report(self, docs):
        # Determine the move_type based on the selected invoice type
        if docs['invoice_type'] == 'out_invoice':  # Sales invoices
            move_type = 'out_invoice'
        elif docs['invoice_type'] == 'in_invoice':  # Purchase invoices
            move_type = 'in_invoice'
        else:
            raise ValueError('Unsupported invoice type selected.')

        # Domain filter for date range and invoice type (move_type)
        domain = [
            ('move_type', '=', move_type),  # Filter by invoice type
            ('invoice_date', '>=', docs['start_date']),
            ('invoice_date', '<=', docs['end_date'])
        ]

        # Search the records in account.move based on the domain filter
        rec = self.env['account.move'].search(domain)
        return rec


    def generate_xlsx_report(self, workbook, data, orders):
        sheet = workbook.add_worksheet('Purchase Report')
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        border = workbook.add_format({'border': 1})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        wrap_format = workbook.add_format({'text_wrap': True, 'border': 1})
        normal_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})

        sheet.merge_range('A1:H1', data.get('invoice_label') + ' Reports',
                          workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'}))

        sheet.write(2, 0, 'Start Date:', bold)
        sheet.write(2, 1, data.get('start_date'))
        sheet.write(2, 2, 'End Date:', bold)
        sheet.write(2, 3, data.get('end_date'))
        sheet.write(3, 0, 'Printed By:', bold)
        sheet.write(3, 1, self.env.user.name)
        sheet.write(4, 0, 'Printed Date:', bold)
        sheet.write(4, 1, datetime.datetime.today().strftime('%Y-%m-%d'))
        headers = [
            'S.N.', 'Customer Invoice', 'Order Date', 'Vendor','Discount Amount','Tax Amount', 'Amount Untaxed','Amount Total']

        column_widths = {i: len(header) for i, header in enumerate(headers)}

        for col_num, header in enumerate(headers):
            sheet.write(5, col_num, header, bold_center)
            column_widths[col_num] = max(column_widths[col_num], len(header))

        row = 6
        index = 1
        records = self.get_purchase_report(data)
        for order in records:
            order_date = order.invoice_date.strftime('%Y-%m-%d') if order.invoice_date else ''
            vendor_name = getattr(order.partner_id, 'name', '')
            amount_total = "{:.2f}".format(getattr(order, 'amount_total', 0.0))
            amount_discount = "{:.2f}".format(getattr(order, 'amount_discount', 0.0))
            amount_tax = "{:.2f}".format(getattr(order, 'amount_tax', 0.0))
            amount_untaxed = "{:.2f}".format(getattr(order, 'amount_untaxed', 0.0))

            sheet.write(row, 0, index, normal_center)
            sheet.write(row, 1, order.name or '', border)
            sheet.write(row, 2, order_date, border)
            sheet.write(row, 3, vendor_name, border)
            sheet.write(row, 4, amount_discount, border)
            sheet.write(row, 5, amount_tax, border)
            sheet.write(row, 6, amount_untaxed, normal_center)
            sheet.write(row, 7, amount_total, normal_center)
            row += 1
            index += 1
        for col_num, width in column_widths.items():
            sheet.set_column(col_num, col_num, width + 5)  # Add some padding





