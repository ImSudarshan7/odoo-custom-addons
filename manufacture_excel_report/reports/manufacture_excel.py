from odoo import models
import logging
from datetime import datetime
import nepali_datetime

_logger = logging.getLogger(__name__)

class ManufacturingOrderReportXlsx(models.AbstractModel):
    _name = 'report.manufacture_excel_report.report_manufacturing_order_xls'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Manufacturing Order Excel Report'

    def get_mrp_report(self, docs):
        _logger.info(docs)
        domain = [
            ('date_planned_start', '>=', docs['start_date']),
            ('date_planned_start', '<=', docs['end_date'])
        ]

        if docs['product_nature_id']:
            domain.append(('product_nature_id', '=', docs['product_nature_id']))

        if docs['product_ids']:
            domain.append(('product_id', 'in', docs['product_ids']))

        rec = self.env['mrp.production'].search(domain)
        return rec

    def convert_to_nepali_date(self, gregorian_date_str):
        """Converts a Gregorian date string to a Nepali date string (YYYY-MM-DD)."""
        gregorian_datetime = datetime.strptime(gregorian_date_str, '%Y-%m-%d')
        gregorian_date = gregorian_datetime.date()
        nepali_date = nepali_datetime.date.from_datetime_date(gregorian_date)
        return nepali_date.strftime('%Y-%m-%d')

    def generate_xlsx_report(self, workbook, data, orders):
        sheet = workbook.add_worksheet('Manufacturing Report')
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        border = workbook.add_format({'border': 1})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        wrap_format = workbook.add_format({'text_wrap': True, 'border': 1})
        normal_center = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1})

        sheet.merge_range('A1:H1', 'Manufacturing Report', workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'}))
        sheet.write(2, 0, 'Start Date:', bold)
        sheet.write(2, 1, data.get('start_date'))
        sheet.write(2, 2, 'End Date:', bold)
        sheet.write(2, 3, data.get('end_date'))

        sheet.write(3, 0, 'Printed By:', bold)
        sheet.write(3, 1, self.env.user.name)
        sheet.write(4, 0, 'Printed Date:', bold)
        sheet.write(4, 1, datetime.today().strftime('%Y-%m-%d'))

        headers = ['S.N.', 'Production No.', 'Production Date (A.D.)', 'Production Date (B.S.)', 'Component', 'Lot No.', 'Qty', 'UOM', 'Finished Product', 'Lot No.', 'Qty', 'UOM', 'Weight per unit', 'Total Weight']
        column_widths = {i: len(headers[i]) for i in range(len(headers))}

        # Write headers
        for col_num, header in enumerate(headers):
            sheet.write(5, col_num, header, bold_center)
            column_widths[col_num] = max(column_widths[col_num], len(header))

        row = 6
        index = 1
        records = self.get_mrp_report(data)

        for order in records:
            num_components = len(order.move_raw_ids)
            first_row = row
            last_row = row + num_components - 1 if num_components > 1 else row

            # Prepare weight and total weight
            weight_per_unit = order.product_id.product_tmpl_id.weight
            total_weight = order.product_qty * weight_per_unit

            # Convert production date to Nepali
            gregorian_date_str = order.date_planned_start.strftime('%Y-%m-%d')
            nepali_date_str = self.convert_to_nepali_date(gregorian_date_str)

            # Merge cells for orders with multiple components
            if num_components > 1:
                sheet.merge_range(first_row, 0, last_row, 0, index, normal_center)
                sheet.merge_range(first_row, 1, last_row, 1, order.name, normal_center)
                sheet.merge_range(first_row, 2, last_row, 2, gregorian_date_str, normal_center)
                sheet.merge_range(first_row, 3, last_row, 3, nepali_date_str, normal_center)
                sheet.merge_range(first_row, 8, last_row, 8, order.product_id.display_name, normal_center)
                sheet.merge_range(first_row, 9, last_row, 9, order.lot_producing_id.name or "", normal_center)
                sheet.merge_range(first_row, 10, last_row, 10, order.product_qty, normal_center)
                sheet.merge_range(first_row, 11, last_row, 11, order.product_uom_id.name, normal_center)
                sheet.merge_range(first_row, 12, last_row, 12, weight_per_unit, normal_center)
                sheet.merge_range(first_row, 13, last_row, 13, total_weight, normal_center)
            else:
                sheet.write(first_row, 0, index, normal_center)
                sheet.write(first_row, 1, order.name, border)
                sheet.write(first_row, 2, gregorian_date_str, border)
                sheet.write(first_row, 3, nepali_date_str, border)
                sheet.write(first_row, 8, order.product_id.display_name, normal_center)
                sheet.write(first_row, 9, order.lot_producing_id.name or "", normal_center)
                sheet.write(first_row, 10, order.product_qty, normal_center)
                sheet.write(first_row, 11, order.product_uom_id.name, normal_center)
                sheet.write(first_row, 12, weight_per_unit, normal_center)
                sheet.write(first_row, 13, total_weight, normal_center)

            # Adjust column widths based on content
            column_widths[0] = max(column_widths[0], len(str(index)))
            column_widths[1] = max(column_widths[1], len(order.name))
            column_widths[2] = max(column_widths[2], len(gregorian_date_str))
            column_widths[3] = max(column_widths[3], len(nepali_date_str))
            column_widths[8] = max(column_widths[8], len(order.product_id.display_name))
            column_widths[9] = max(column_widths[9], len(order.lot_producing_id.name or ""))
            column_widths[10] = max(column_widths[10], len(str(order.product_qty)))
            column_widths[11] = max(column_widths[11], len(order.product_uom_id.name))
            column_widths[12] = max(column_widths[12], len(str(weight_per_unit)))
            column_widths[13] = max(column_widths[13], len(str(total_weight)))

            # Write components
            for component in order.move_raw_ids:
                sheet.write(row, 4, component.product_id.display_name, border)
                lot_numbers = ", ".join([lot.name for lot in component.lot_ids])
                sheet.write(row, 5, lot_numbers, normal_center)
                sheet.write(row, 6, component.product_uom_qty, normal_center)
                sheet.write(row, 7, component.product_uom.name, normal_center)

                column_widths[4] = max(column_widths[4], len(component.product_id.display_name))
                column_widths[5] = max(column_widths[5], len(lot_numbers))
                column_widths[6] = max(column_widths[6], len(str(component.product_uom_qty)))
                column_widths[7] = max(column_widths[7], len(str(component.product_uom.name)))

                row += 1

            index += 1

        sheet.write(row + 4, 0, 'Authorized Signature', bold)

        # Adjust column widths for better readability
        for col_num, width in column_widths.items():
            sheet.set_column(col_num, col_num, width + 5)  # Adding some padding
