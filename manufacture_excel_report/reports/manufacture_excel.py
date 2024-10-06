from odoo import models
import logging

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

    def generate_xlsx_report(self, workbook, data, orders):
        sheet = workbook.add_worksheet('Manufacturing Report')
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        border = workbook.add_format({'border': 1})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        wrap_format = workbook.add_format({'text_wrap': True, 'border': 1})
        normal_center = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1})

        sheet.merge_range('A1:H1', 'Manufacturing Report', workbook.add_format({'bold': True, 'font_size': 20, 'align': 'center'}))
        sheet.write(2, 0, 'Production Date:', bold)
        sheet.write(2, 1, data.get('start_date'))

        headers = ['S.N.', 'Production No.', 'Component', 'Lot No.', 'Qty','UoM', 'Finished Product', 'Lot No.', 'Qty','UoM', 'Weight per unit', 'Total Weight']
        column_widths = {i: len(headers[i]) for i in range(len(headers))}

        for col_num, header in enumerate(headers):
            sheet.write(4, col_num, header, bold_center)
            column_widths[col_num] = max(column_widths[col_num], len(header))

        row = 5
        index = 1
        records = self.get_mrp_report(data)

        for order in records:
            num_components = len(order.move_raw_ids)
            first_row = row
            last_row = row + num_components - 1 if num_components > 1 else row

            # Prepare weight and total weight
            weight_per_unit = order.product_id.product_tmpl_id.weight
            total_weight = order.product_qty * weight_per_unit

            if num_components > 1:
                sheet.merge_range(first_row, 0, last_row, 0, index, normal_center)
                sheet.merge_range(first_row, 1, last_row, 1, order.name, normal_center)
                sheet.merge_range(first_row, 6, last_row, 6, order.product_id.display_name, normal_center)
                sheet.merge_range(first_row, 7, last_row, 7, order.lot_producing_id.name or "", normal_center)
                sheet.merge_range(first_row, 8, last_row, 8, order.product_qty, normal_center)
                sheet.merge_range(first_row, 9, last_row, 9, order.product_uom_id.name, normal_center)
                sheet.merge_range(first_row, 10, last_row, 10, weight_per_unit, normal_center)
                sheet.merge_range(first_row, 11, last_row, 11, total_weight, normal_center)
            else:
                sheet.write(first_row, 0, index, normal_center)
                sheet.write(first_row, 1, order.name, border)
                sheet.write(first_row, 6, order.product_id.display_name, normal_center)
                sheet.write(first_row, 7, order.lot_producing_id.name or "", normal_center)
                sheet.write(first_row, 8, order.product_qty, normal_center)
                sheet.write(first_row, 9, order.product_uom_id.name, normal_center)
                sheet.write(first_row, 10, weight_per_unit, normal_center)
                sheet.write(first_row, 11, total_weight, normal_center)

            column_widths[0] = max(column_widths[0], len(str(index)))
            column_widths[1] = max(column_widths[1], len(order.name))
            column_widths[6] = max(column_widths[6], len(order.product_id.display_name))
            column_widths[7] = max(column_widths[7], len(order.lot_producing_id.name or ""))
            column_widths[8] = max(column_widths[8], len(str(order.product_qty)))
            column_widths[9] = max(column_widths[9], len(str(order.product_uom_id.name)))
            column_widths[10] = max(column_widths[10], len(str(weight_per_unit)))
            column_widths[11] = max(column_widths[11], len(str(total_weight)))

            for component in order.move_raw_ids:
                sheet.write(row, 2, component.product_id.display_name, border)
                lot_numbers = ", ".join([lot.name for lot in component.lot_ids])
                sheet.write(row, 3, lot_numbers, border)
                sheet.write(row, 4, component.quantity_done, normal_center)
                sheet.write(row, 5, component.product_uom.name, normal_center)

                column_widths[2] = max(column_widths[2], len(component.product_id.display_name))
                column_widths[3] = max(column_widths[3], len(lot_numbers))
                column_widths[4] = max(column_widths[4], len(str(component.quantity_done)))
                column_widths[5] = max(column_widths[5], len(str(component.product_uom.name)))


                row += 1

            index += 1

        sheet.write(row + 4, 0, 'Authorized Signature', bold)

        # Adjust column widths
        for col_num, width in column_widths.items():
            sheet.set_column(col_num, col_num, width + 5)  # Adding some padding for better visibility

