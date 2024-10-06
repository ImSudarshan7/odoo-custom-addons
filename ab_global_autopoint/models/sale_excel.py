from odoo import models

class ReportSaleQuotationXlsx(models.AbstractModel):
    _name = 'report.report_sales_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, docs):
        for doc in docs:
            # Create a worksheet
            sheet = workbook.add_worksheet('Quotation')

            # Define formats
            bold = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            currency_format = workbook.add_format({'num_format': '#,##0.00'})

            # Title and headers
            # Create a format for the merged cell with bold text, centered alignment, and a larger font size
            merge_format = workbook.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 16
            })

            # Merge the cells and apply the format
            sheet.merge_range('A1:G1', 'Quotation', merge_format)

            # Customer Info
            sheet.write(3, 0, 'Customer Name:', bold)
            sheet.write(3, 1, doc.partner_id.name)

            sheet.write(4, 0, 'Address:', bold)
            sheet.write(4, 1, doc.partner_id.street)

            sheet.write(5, 0, 'Phone No.:', bold)
            sheet.write(5, 1, doc.partner_id.mobile)

            sheet.write(6, 0, 'Date:', bold)
            # sheet.write(6, 1, Date.to_string(doc.date_order))
            sheet.write(6, 1, doc.date_order.strftime('%d/%m/%Y'))

            # Quotation Info
            sheet.write(3, 3, 'Q. No:', bold)
            sheet.write(3, 4, doc.name)

            sheet.write(4, 3, 'Vehicle No:', bold)
            sheet.write(4, 4, doc.vehicle_num.vehicle_no)

            sheet.write(5, 3, 'Make:', bold)
            sheet.write(5, 4, doc.vehicle_num.name)

            sheet.write(6, 3, 'Model No:', bold)
            sheet.write(6, 4, doc.vehicle_num.model_no)

            sheet.write(7, 3, 'VIN:', bold)
            sheet.write(7, 4, doc.vehicle_num.chasis_no)

            # Table Headers
            sheet.write(10, 0, 'S.N', bold)
            sheet.write(10, 1, 'Parts No.', bold)
            sheet.write(10, 2, 'Description', bold)
            sheet.write(10, 3, 'QTY.', bold)
            sheet.write(10, 4, 'UoM', bold)
            sheet.write(10, 5, 'Unit Price', bold)
            sheet.write(10, 6, 'Amount', bold)

            # Table Rows
            row = 11
            for index, line in enumerate(doc.order_line):
                sheet.write(row, 0, index + 1)
                sheet.write(row, 1, line.product_id.product_tmpl_id.name)
                sheet.write(row, 2, line.name if line.product_id.type == 'service' else '')
                sheet.write(row, 3, line.product_uom_qty if line.product_id.type == 'product' else '')
                sheet.write(row, 4, line.product_uom.name if line.product_id.type == 'product' else '')
                sheet.write(row, 5, line.price_unit, currency_format)
                sheet.write(row, 6, line.dumy_subtotal, currency_format)
                row += 1

            # Totals
            sheet.write(row + 1, 5, 'Sub Total', bold)
            sheet.write(row + 1, 6, doc.amount_untaxed + doc.amount_discount, currency_format)

            sheet.write(row + 2, 5, 'Discount', bold)
            sheet.write(row + 2, 6, doc.amount_discount, currency_format)

            sheet.write(row + 3, 5, 'Taxable Amount', bold)
            sheet.write(row + 3, 6, doc.amount_untaxed, currency_format)

            sheet.write(row + 4, 5, '13 % VAT', bold)
            sheet.write(row + 4, 6, doc.amount_tax, currency_format)

            sheet.write(row + 5, 5, 'GRAND TOTAL', bold)
            sheet.write(row + 5, 6, doc.amount_total, currency_format)

            # Terms and Conditions
            sheet.write(row + 7, 0, 'Terms and Conditions', bold)
            # sheet.write(row + 8, 0, doc.note, workbook.add_format({'text_wrap': True}))

            # Remarks
            sheet.write(row + 10, 0, 'Remarks:', bold)
            sheet.write(row + 11, 0, 'Certain Parts may not be available with the parent Company at the time of Order Placement', workbook.add_format({'text_wrap': True}))
            sheet.write(row + 12, 0, 'Estimate may vary after dismantling vehicle thoroughly...', workbook.add_format({'text_wrap': True}))

            # Company Details
            sheet.write(row + 14, 5, 'For:', bold)
            sheet.write(row + 15, 5, doc.company_id.name)

