# -*- coding: utf-8 -*-
from multiprocessing.sharedctypes import Value
import xlwt
import base64
import calendar
import os
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class IrdSalesPurchaseReport(models.TransientModel):
    _name = "ird.sales.purchase.report.ext"
    
    start_date = fields.Date(string='Start Date', required=True, default=datetime.today().replace(day=1))
    end_date = fields.Date(string="End Date", required=True, default=datetime.now().replace(day = calendar.monthrange(datetime.now().year, datetime.now().month)[1]))
    # invoice_state = fields.Selection([
    #         ('open', 'Open'),
    #         ('paid', 'Paid'),
    #     ], string='Status', default='open', required=True)
    invoice_type = fields.Selection([
            ('out_invoice', 'Sales'),
            ('out_refund', 'Sales Return'),
            ('in_invoice', 'Purchase'),
            ('in_refund', 'Purchase Return'),
        ], string='Type', default='out_invoice', required=True)

    invoice_data = fields.Char('Name',)
    file_name = fields.Binary('IRD Sales/Purchase Excel Report Ext', readonly=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')

    _sql_constraints = [('check', 'CHECK((start_date <= end_date))', "End date must be greater then start date")]

    def action_ird_sales_purchase_report_ext(self):
        workbook = xlwt.Workbook()

        if self.invoice_type == 'out_invoice':
            invoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date), 
                                                    ('state', '=', 'posted'), ('move_type', '=', 'out_invoice')])
            sheet = workbook.add_sheet('Sale001 Ext', cell_overwrite_ok=True)
            sheet.col(0).width = int(20*260)
            sheet.col(1).width = int(20*260)
            sheet.col(2).width = int(30*260)
            sheet.col(3).width = int(18*260)
            sheet.col(4).width = int(33*260)
            sheet.col(5).width = int(12*260)
            sheet.col(6).width = int(15*260)
            sheet.col(7).width = int(20*260)
            sheet.col(8).width = int(18*260)
            sheet.col(9).width = int(15*260)
            sheet.col(10).width = int(15*260)
            sheet.col(11).width = int(15*260)
            sheet.col(12).width = int(15*260)
            sheet.col(13).width = int(15*260)
            sheet.col(14).width = int(15*260)

            format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
            format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
            format2 = xlwt.easyxf('font:bold True;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format5 = xlwt.easyxf('font:bold True;align: horiz right')
            format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
            format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

            sheet.write_merge(0, 2, 0, 14, 'IRD Sales Book', format0)
        elif self.invoice_type == 'out_refund':
            invoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date), 
                                                    ('state', '=', 'posted'), ('move_type', '=', 'out_refund')])
            sheet = workbook.add_sheet('Sale001 Return Ext', cell_overwrite_ok=True)
            sheet.col(0).width = int(20*260)
            sheet.col(1).width = int(20*260)
            sheet.col(2).width = int(30*260)
            sheet.col(3).width = int(18*260)
            sheet.col(4).width = int(33*260)
            sheet.col(5).width = int(12*260)
            sheet.col(6).width = int(15*260)
            sheet.col(7).width = int(20*260)
            sheet.col(8).width = int(18*260)
            sheet.col(9).width = int(15*260)
            sheet.col(10).width = int(15*260)
            sheet.col(11).width = int(15*260)
            sheet.col(12).width = int(15*260)
            sheet.col(13).width = int(15*260)
            sheet.col(14).width = int(15*260)
            

            format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
            format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
            format2 = xlwt.easyxf('font:bold True;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format5 = xlwt.easyxf('font:bold True;align: horiz right')
            format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
            format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

            sheet.write_merge(0, 2, 0, 14, 'IRD Sales Return Book', format0)

        elif self.invoice_type == 'in_invoice':
            invoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date), 
                                                    ('state', '=', 'posted'), ('move_type', '=', 'in_invoice')])
            sheet = workbook.add_sheet('Purchase001 Ext', cell_overwrite_ok=True)
            sheet.col(0).width = int(20*260)
            sheet.col(1).width = int(20*260)
            sheet.col(2).width = int(30*260)
            sheet.col(3).width = int(18*260)
            sheet.col(4).width = int(33*260)
            sheet.col(5).width = int(12*260)
            sheet.col(6).width = int(12*260)
            sheet.col(7).width = int(20*260)
            sheet.col(8).width = int(25*260)
            sheet.col(9).width = int(25*260)
            sheet.col(10).width = int(15*260)
            sheet.col(11).width = int(15*260)
            sheet.col(12).width = int(15*260)
            sheet.col(13).width = int(15*260)
            sheet.col(14).width = int(15*260)


            format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
            format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
            format2 = xlwt.easyxf('font:bold True;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format5 = xlwt.easyxf('font:bold True;align: horiz right')
            format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
            format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

            sheet.write_merge(0, 2, 0, 14, 'IRD Purchase Book', format0)
        else:
            invoice = self.env['account.move'].search([('invoice_date', '>=', self.start_date), ('invoice_date', '<=', self.end_date), 
                                                    ('state', '=', 'posted'), ('move_type', '=', 'in_refund')])
            sheet = workbook.add_sheet('Purchase001 Return Ext', cell_overwrite_ok=True)
            sheet.col(0).width = int(20*260)
            sheet.col(1).width = int(20*260)
            sheet.col(2).width = int(30*260)
            sheet.col(3).width = int(18*260)
            sheet.col(4).width = int(33*260)
            sheet.col(5).width = int(12*260)
            sheet.col(6).width = int(15*260)
            sheet.col(7).width = int(20*260)
            sheet.col(8).width = int(18*260)
            sheet.col(9).width = int(15*260)
            sheet.col(10).width = int(15*260)
            sheet.col(11).width = int(15*260)
            sheet.col(12).width = int(15*260)
            sheet.col(13).width = int(15*260)
            sheet.col(14).width = int(15*260)


            format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
            format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
            format2 = xlwt.easyxf('font:bold True;align: horiz left')
            format3 = xlwt.easyxf('align: horiz left')
            format4 = xlwt.easyxf('align: horiz right')
            format5 = xlwt.easyxf('font:bold True;align: horiz right')
            format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
            format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
            format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

            sheet.write_merge(0, 2, 0, 14, 'IRD Purchase Return Book', format0)
        record = []
        if invoice:
            for rec in invoice:
                record.append(rec)
                # if self.partner_select == "customer" and rec.partner_id.customer == True and rec.partner_id.supplier == False:
                #     record.append(rec)
                # elif self.partner_select == "vendor" and rec.partner_id.supplier == True and rec.partner_id.customer == False:
                #     record.append(rec)
                # elif self.partner_select == "both" and rec.partner_id.customer == True and rec.partner_id.supplier == True:
                    # record.append(rec)
            file = StringIO()        
            record.sort(key=lambda p: (p.invoice_date, p.name))
            final_value = {}
            # products = []
            # data1 = {}
            # data1['start'] = str(self.start_date)
            # data1['end'] = str(self.end_date)
            
            timestamp = str(datetime.today())
            row = 11
            if self.invoice_type == 'out_invoice':
                sheet.write(4, 0, "Seller Name:", format1)
                sheet.write(4, 1, str(self.env.company.name), format2)
                # _logger.info("====%s==========rec=====%s===",self,self.env.company.name)
                sheet.write(5, 0, "Seller PAN:", format1)
                sheet.write(5, 1, str(rec.company_id.vat), format2)
                sheet.write(6, 0, "Seller Address:", format1)
                sheet.write(6, 1, str(rec.company_id.street), format2)
                sheet.write(7, 0, "Duration of Sales", format1)
                sheet.write(7, 1, str(self.start_date), format2)
                sheet.write(7, 2, 'TO', format2)
                sheet.write(7, 3, str(self.end_date), format2)
                sheet.write(8, 0, 'Report generated at:', format1)
                sheet.write(8, 1, timestamp, format2)
                sheet.write(10, 0, 'Date', format1)
                sheet.write(10, 1, 'Bill No', format1)
                sheet.write(10, 2, 'Buyer Name', format1)
                sheet.write(10, 3, 'Buyer PAN No.', format1)
                sheet.write(10, 4, 'Product Name', format1)
                sheet.write(10, 5, 'Quantity', format6)


                # Additional Field for UoM(Unit of Measurements)
                sheet.write(10, 6, 'UoM', format6)





                sheet.write(10, 7, 'Total Sales', format6)
                sheet.write(10, 8, 'Non-Taxable Sales', format6)
                sheet.write(10, 9, 'Taxable Sales', format6)
                sheet.write(10, 10, 'Tax(Rs)', format6)
                sheet.write(10, 11, 'Export Sales', format6)
                sheet.write(10, 12, 'Export Country', format6)
                sheet.write(10, 13, 'Export Ref No.', format6)
                sheet.write(10, 14, 'Export Ref Date', format6)
               
                row1 = 11
                if record:
                    grand_price_total = 0.0
                    grand_price_subtotal = 0.0
                    grand_tax = 0.0
                    untax_total = 0.0
                    for rec in record:

                        for lines in rec.invoice_line_ids:
                            # products.append(lines.product_id.name)

                            sheet.write(row, 0, str(rec.invoice_date.strftime('%Y.%m.%d')), format3)

                            sheet.write(row, 1, str(rec.name), format3)
                            # if rec.partner_id.parent_id:
                            #     sheet.write(row, 2, str(rec.partner_id.parent_id.name), format3)
                            #     if rec.partner_id.parent_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)


                            # else:
                            #     sheet.write(row, 2, str(rec.partner_id.name), format3)
                            #     if rec.partner_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)

                            sheet.write(row, 2, str(rec.partner_id.name), format3)
                            if rec.partner_id.vat:
                                sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            else:
                                sheet.write(row, 3, "", format3)

                            sheet.write(row, 4, str(lines.product_id.name), format3)
                            sheet.write(row, 5, str(lines.quantity), format4)

                            

                            #For UOM Values
                            sheet.write(row, 6, str(lines.product_uom_id.name), format4)




                            sheet.write(row, 7, lines.price_total, format4)
                            grand_price_total += lines.price_total
                            # sheet.write(row, 8, '0.0', format4)
                            # sheet.write(row, 9, lines.price_subtotal, format4)
                            grand_price_subtotal += lines.price_subtotal
                            taxx = round(lines.price_total-lines.price_subtotal,3)

                            if not lines.tax_ids:
                                sheet.write(row, 8, lines.price_subtotal, format4)
                                sheet.write(row, 9, '0.0', format4)
                                untax_total += lines.price_subtotal
                            else:
                                sheet.write(row, 8, '0.0', format4)
                                sheet.write(row, 9, lines.price_subtotal, format4)
                                sheet.write(row, 10, taxx, format4)
                                grand_tax += taxx

                            sheet.write(row, 11, '0.0', format4)
                            sheet.write(row, 12, "", format4)
                            sheet.write(row, 13, "", format4)
                            sheet.write(row, 14, "", format4)
                            

                            # sheet.write(row, 6, str(lines.product_uom_id.name), format4)


                            row = row + 1
                        # row=row+1
                    #     invoice_lines = []
                    #     for lines in rec.invoice_line_ids:
                    #         product = {
                                
                    #             'description'    : lines.product_id.name,
                    #             'quantity'       : lines.quantity,
                    #             'price_unit'     : lines.price_unit,
                    #             'price_subtotal' : lines.price_each_subtotal 
                    #         }
                    #         if lines.invoice_line_tax_ids:
                    #             taxes = []
                    #             for tax_id in lines.invoice_line_tax_ids:
                    #                 taxes.append(tax_id.name)
                    #             product['invoice_line_tax_ids'] = taxes
                    #         invoice_lines.append(product)
                        final_value['partner_id'] = rec.partner_id.name
                        final_value['pan_number'] = rec.partner_id.vat
                        final_value['address_buyer'] = rec.partner_id.street
                        final_value['company_id'] = rec.company_id.name
                        final_value['pan_number_seller'] = rec.company_id.vat
                        final_value['address_seller'] = rec.company_id.street
                        final_value['date_invoice'] = rec.invoice_date
                        # final_value['date_due'] = rec.date_due
                        final_value['number'] = rec.name
                        final_value['currency_id'] = rec.currency_id
                        # final_value['state'] = dict(self.env['account.invoice'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                        # final_value['payment_term_id'] = rec.payment_term_id.name
                        # final_value['origin'] = rec.origin
                        final_value['amount_untaxed'] = rec.amount_untaxed
                        # final_value['amount_subtotal_1'] = rec.amount_actual
                        # final_value['amount_discount'] = "0.00"
                        final_value['amount_tax'] = rec.amount_tax
                        final_value['amount_total'] = rec.amount_total

                        # sheet.write(row, 7, '0.0', format4)
                        # sheet.write(row, 8, str(final_value['amount_untaxed']), format4)
                        # sheet.write(row, 9, str(final_value['amount_tax']), format4)
                        # row=row+2
                    row1 = row + 1
                    sheet.write(row1, 6, "Grand Total", format5)
                    sheet.write(row1, 7, grand_price_total, format5)
                    sheet.write(row1, 8, untax_total, format5)
                    sheet.write(row1, 9, grand_price_subtotal, format5)
                    # sheet.write(row1, 9,"Grand Tax", format1)
                    sheet.write(row1, 10, round(grand_tax, 2), format5)

            elif self.invoice_type == 'out_refund':
                sheet.write(4, 0, "Seller Name:", format1)
                # sheet.write(4, 1, str(rec.company_id.name), format2)
                sheet.write(4, 1, str(self.env.company.name), format2)
                # _logger.info("====%s==========rec=====%s===",self,self.env.company.name)
                sheet.write(5, 0, "Seller PAN:", format1)
                sheet.write(5, 1, str(rec.company_id.vat), format2)
                sheet.write(6, 0, "Seller Address:", format1)
                sheet.write(6, 1, str(rec.company_id.street), format2)
                sheet.write(7, 0, "Duration of Sales", format1)
                sheet.write(7, 1, str(self.start_date), format2)
                sheet.write(7, 2, 'TO', format2)
                sheet.write(7, 3, str(self.end_date), format2)
                sheet.write(8, 0, 'Report generated at:', format1)
                sheet.write(8, 1, timestamp, format2)

                sheet.write(10, 0, 'Date', format1)
                sheet.write(10, 1, 'Bill No', format1)
                sheet.write(10, 2, 'Buyer Name', format1)
                sheet.write(10, 3, 'Buyer PAN No.', format1)
                sheet.write(10, 4, 'Product Name', format1)
                sheet.write(10, 5, 'Quantity', format6)


                # Additional Field for UoM(Unit of Measurements)
                sheet.write(10, 6, 'UoM', format6)

                sheet.write(10, 7, 'Total Sales', format6)
                sheet.write(10, 8, 'Non-Taxable Sales', format6)
                sheet.write(10, 9, 'Taxable Sales', format6)
                sheet.write(10, 10, 'Tax(Rs)', format6)
                sheet.write(10, 11, 'Export Sales', format6)
                sheet.write(10, 12, 'Export Country', format6)
                sheet.write(10, 13, 'Export Ref No.', format6)
                sheet.write(10, 14, 'Export Ref Date', format6)
                row1 = 11
                if record:
                    grand_price_total = 0
                    grand_price_subtotal = 0
                    grand_tax = 0
                    untax_total = 0

                    for rec in record:
                        for lines in rec.invoice_line_ids:
                            # products.append(lines.product_id.name)
                            sheet.write(row, 0, str(rec.invoice_date.strftime('%Y.%m.%d')), format3)
                            sheet.write(row, 1, str(rec.name), format3)
                            # if rec.partner_id.parent_id:
                            #     sheet.write(row, 2, str(rec.partner_id.parent_id.name), format3)
                            #     if rec.partner_id.parent_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)


                            # else:
                            #     sheet.write(row, 2, str(rec.partner_id.name), format3)
                            #     if rec.partner_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)

                            sheet.write(row, 2, str(rec.partner_id.name), format3)
                            if rec.partner_id.vat:
                                sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            else:
                                sheet.write(row, 3, "", format3)
                            sheet.write(row, 4, str(lines.product_id.name), format3)
                            sheet.write(row, 5, lines.quantity, format4)

                            # For UOM Value
                            sheet.write(row, 6, str(lines.product_uom_id.name), format4)
                            sheet.write(row, 7, lines.price_total, format4)
                            grand_price_total += lines.price_total
                            # sheet.write(row, 8, '0.0', format4)
                            # sheet.write(row, 9, lines.price_subtotal, format4)
                            grand_price_subtotal += lines.price_subtotal
                            taxx = round(lines.price_total-lines.price_subtotal,3)

                            if not lines.tax_ids:
                                sheet.write(row, 8, lines.price_subtotal, format4)
                                sheet.write(row, 9, '0.0', format4)
                                untax_total += lines.price_subtotal
                            else:
                                sheet.write(row, 8, '0.0', format4)
                                sheet.write(row, 9, lines.price_subtotal, format4)
                                sheet.write(row, 10, taxx, format4)
                                grand_tax += taxx

                            sheet.write(row, 11, '0.0', format4)
                            sheet.write(row, 12, "", format4)
                            sheet.write(row, 13, "", format4)
                            sheet.write(row, 14, "", format4)
                            row = row+1
                        # row=row+1
                    #     invoice_lines = []
                    #     for lines in rec.invoice_line_ids:
                    #         product = {
                                
                    #             'description'    : lines.product_id.name,
                    #             'quantity'       : lines.quantity,
                    #             'price_unit'     : lines.price_unit,
                    #             'price_subtotal' : lines.price_each_subtotal 
                    #         }
                    #         if lines.invoice_line_tax_ids:
                    #             taxes = []
                    #             for tax_id in lines.invoice_line_tax_ids:
                    #                 taxes.append(tax_id.name)
                    #             product['invoice_line_tax_ids'] = taxes
                    #         invoice_lines.append(product)
                        final_value['partner_id'] = rec.partner_id.name
                        final_value['pan_number'] = rec.partner_id.vat
                        final_value['address_buyer'] = rec.partner_id.street
                        final_value['company_id'] = rec.company_id.name
                        final_value['pan_number_seller'] = rec.company_id.vat
                        final_value['address_seller'] = rec.company_id.street
                        final_value['date_invoice'] = rec.invoice_date
                        # final_value['date_due'] = rec.date_due
                        final_value['number'] = rec.name
                        final_value['currency_id'] = rec.currency_id
                        # final_value['state'] = dict(self.env['account.invoice'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                        # final_value['payment_term_id'] = rec.payment_term_id.name
                        # final_value['origin'] = rec.origin
                        final_value['amount_untaxed'] = rec.amount_untaxed
                        # final_value['amount_subtotal_1'] = rec.amount_actual
                        # final_value['amount_discount'] = "0.00"
                        final_value['amount_tax'] = rec.amount_tax
                        final_value['amount_total'] = rec.amount_total

                        # sheet.write(row, 6, str(final_value['amount_total']), format4)
                        # sheet.write(row, 7, '0.0', format4)
                        # sheet.write(row, 8, str(final_value['amount_untaxed']), format4)
                        # sheet.write(row, 9, str(final_value['amount_tax']), format4)

                        # row=row+2
                    row1 = row + 1
                    sheet.write(row1, 6, "Grand Total", format5)
                    sheet.write(row1, 7, grand_price_total, format5)
                    sheet.write(row1, 8, untax_total, format5)
                    sheet.write(row1, 9, grand_price_subtotal, format5)
                    # sheet.write(row1, 9,"Grand Tax", format1)
                    sheet.write(row1, 10, grand_tax, format5)

            elif self.invoice_type == 'in_invoice':
                sheet.write(4, 0, "Buyer Name:", format1)
                # sheet.write(4, 1, str(rec.company_id.name), format2)
                sheet.write(4, 1, str(self.env.company.name), format2)
                # _logger.info("====%s==========rec=====%s===",self,self.env.company.name)
                sheet.write(5, 0, "Buyer PAN:", format1)
                sheet.write(5, 1, str(rec.company_id.vat), format2)
                sheet.write(6, 0, "Buyer Address:", format1)
                sheet.write(6, 1, str(rec.company_id.street), format2)
                sheet.write(7, 0, "Duration of Purchase", format1)
                sheet.write(7, 1, str(self.start_date), format2)
                sheet.write(7, 2, 'TO', format2)
                sheet.write(7, 3, str(self.end_date), format2)
                sheet.write(8, 0, 'Report generated at:', format1)
                sheet.write(8, 1, timestamp, format2)

                sheet.write(10, 0, 'Date', format1)
                sheet.write(10, 1, 'Bill No', format1)
                sheet.write(10, 2, 'Seller Name', format1)
                sheet.write(10, 3, 'Seller PAN No.', format1)
                sheet.write(10, 4, 'Product Name', format1)
                sheet.write(10, 5, 'Quantity', format6)

                # Additional Field for UoM(Unit of Measurements)
                sheet.write(10, 6, 'UoM', format6)

                sheet.write(10, 7, 'Total Purchase', format6)
                sheet.write(10, 8, 'Non-Taxable Purchase', format6)
                sheet.write(10, 9, 'Taxable Purchase', format6)
                sheet.write(10, 10, 'Tax(Rs)', format6)
                sheet.write(10, 11, 'Import Purchase', format6)
                sheet.write(10, 12, 'Import VAT', format6)
                sheet.write(10, 13, 'Fixed Assets/Total', format6)
                sheet.write(10, 14, 'Fixed Assets/Vat', format6)
                # sheet.write(11, 12, 'Export Ref No.', format6)
                # sheet.write(11, 13, 'Export Ref Date', format6)
                
                row1 = 11
                if record:
                    purchase_total = 0.0
                    non_taxable_total = 0.0
                    taxable_total = 0.0
                    tax_total = 0.0

                    for rec in record:
                        for lines in rec.invoice_line_ids:
                            # products.append(lines.product_id.name)
                            sheet.write(row1, 0, str(rec.invoice_date.strftime('%Y.%m.%d')), format3)
                            sheet.write(row1, 1, str(rec.name), format3)
                            # if rec.partner_id.parent_id:
                            #     sheet.write(row, 2, str(rec.partner_id.parent_id.name), format3)
                            #     if rec.partner_id.parent_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)


                            # else:
                            #     sheet.write(row, 2, str(rec.partner_id.name), format3)
                            #     if rec.partner_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)

                            sheet.write(row1, 2, str(rec.partner_id.name), format3)
                            if rec.partner_id.vat:
                                sheet.write(row1, 3, str(rec.partner_id.vat), format3)
                            else:
                                sheet.write(row1, 3, "", format3)
                            sheet.write(row1, 4, str(lines.product_id.name), format3)
                            sheet.write(row1, 5, lines.quantity, format4)


                            # For UoM value
                            sheet.write(row1, 6, str(lines.product_uom_id.name), format4)


                            sheet.write(row1, 7, lines.price_total, format4)

                            # sheet.write(row1, 7, '0.0', format4)
                            if not lines.tax_ids:
                                sheet.write(row1, 8, lines.price_subtotal, format4)
                                sheet.write(row1, 9, '0.0', format4)
                            else:
                                sheet.write(row1, 8, '0.0', format4)
                                sheet.write(row1, 9, lines.price_subtotal, format4)
                            # sheet.write(row1, 8, str(lines.price_subtotal), format4)
                            
                            if lines.tax_ids:
                                sheet.write(row1, 10, str(round(lines.price_total-lines.price_subtotal,3)), format4)
                            sheet.write(row1, 11, '0.0', format4)
                            sheet.write(row1, 12, "", format4)
                            # sheet.write(row, 12,"N/A", format4)
                            # sheet.write(row, 13,"N/A", format4)
                            # sheet.write(row1, 12, "N/A", format4)
                            # sheet.write(row1, 13,"N/A", format4)
                            row1 = row1+1
                    #     invoice_lines = []
                    #     for lines in rec.invoice_line_ids:
                    #         product = {
                                
                    #             'description'    : lines.product_id.name,
                    #             'quantity'       : lines.quantity,
                    #             'price_unit'     : lines.price_unit,
                    #             'price_subtotal' : lines.price_each_subtotal 
                    #         }
                    #         if lines.invoice_line_tax_ids:
                    #             taxes = []
                    #             for tax_id in lines.invoice_line_tax_ids:
                    #                 taxes.append(tax_id.name)
                    #             product['invoice_line_tax_ids'] = taxes
                    #         invoice_lines.append(product)
                        final_value['partner_id'] = rec.partner_id.name
                        final_value['pan_number'] = rec.partner_id.vat
                        final_value['address_buyer'] = rec.partner_id.street
                        final_value['company_id'] = rec.company_id.name
                        final_value['pan_number_seller'] = rec.company_id.vat
                        final_value['address_seller'] = rec.company_id.street
                        final_value['date_invoice'] = rec.invoice_date
                        # final_value['date_due'] = rec.date_due
                        final_value['number'] = rec.name
                        final_value['currency_id'] = rec.currency_id
                        # final_value['state'] = dict(self.env['account.invoice'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                        # final_value['payment_term_id'] = rec.payment_term_id.name
                        # final_value['origin'] = rec.origin
                        final_value['amount_untaxed'] = rec.amount_untaxed
                        # final_value['amount_subtotal_1'] = rec.amount_actual
                        final_value['amount_discount'] = "0.00"
                        final_value['amount_tax'] = rec.amount_tax
                        final_value['amount_total'] = rec.amount_total
                        # final_value['amnt_in_words'] = rec.get_amount_in_words()
                        # sheet.write(row1, 4,  str(final_value['amount_total']), format4)
                        # sheet.write(row1, 5, '0.0', format4)
                        # sheet.write(row1, 6, '0.0', format4)
                        # sheet.write(row1, 7,   str(final_value['amount_discount']), format4)
                        # sheet.write(row1, 8, str(final_value['amount_untaxed']), format4)
                        # sheet.write(row1, 9,  str(final_value['amount_tax']), format4)
                        # row1=row1+1
                        # sheet.write(row1, 7, str(final_value['amount_total']), format5)
                        purchase_total += rec.amount_total
                        if not lines.tax_ids:
                            non_taxable_total += rec.amount_untaxed
                            # sheet.write(row1, 8, str(final_value['amount_untaxed']), format5)
                            # sheet.write(row1, 9, '0.0', format5)
                        else:
                            taxable_total += rec.amount_untaxed
                            # sheet.write(row1, 8, '0.0', format5)
                            # sheet.write(row1, 9, str(final_value['amount_untaxed']), format5)
                        tax_total += rec.amount_tax
                        # sheet.write(row1, 10, str(final_value['amount_tax']), format5)
                        # row1 = row1 + 1

                    sheet.write(row1, 6, "Grand Total", format5)
                    sheet.write(row1, 7, purchase_total, format5)
                    sheet.write(row1, 8, non_taxable_total, format5)
                    sheet.write(row1, 9, taxable_total, format5)
                    sheet.write(row1, 10, tax_total, format5)
            else:
                sheet.write(4, 0, "Buyer Name:", format1)
                # sheet.write(4, 1, str(rec.company_id.name), format2)
                sheet.write(4, 1, str(self.env.company.name), format2)
                # _logger.info("====%s==========rec=====%s===",self,self.env.company.name)
                sheet.write(5, 0, "Buyer PAN:", format1)
                sheet.write(5, 1, str(rec.company_id.vat), format2)
                sheet.write(6, 0, "Buyer Address:", format1)
                sheet.write(6, 1, str(rec.company_id.street), format2)
                sheet.write(7, 0, "Duration of Purchase", format1)
                sheet.write(7, 1, str(self.start_date), format2)
                sheet.write(7, 2, 'TO', format2)
                sheet.write(7, 3, str(self.end_date), format2)
                sheet.write(8, 0, 'Report generated at:', format1)
                sheet.write(8, 1, timestamp, format2)

                sheet.write(10, 0, 'Date', format1)
                sheet.write(10, 1, 'Bill No', format1)
                sheet.write(10, 2, 'Seller Name', format1)
                sheet.write(10, 3, 'Seller PAN No.', format1)
                sheet.write(10, 4, 'Product Name', format1)
                sheet.write(10, 5, 'Quantity', format6)


                
                # Additional Field for UoM(Unit of Measurements)
                sheet.write(10, 6, 'UoM', format6)


                sheet.write(10, 7, 'Total Purchase', format6)
                sheet.write(10, 8, 'Non-Taxable Purchase', format6)
                sheet.write(10, 9, 'Taxable Purchase', format6)
                sheet.write(10, 10, 'Tax(Rs)', format6)
                sheet.write(10, 11, 'Import Purchase', format6)
                sheet.write(10, 12, 'Import VAT', format6)
                sheet.write(10, 13, 'Fixed Assets/Total', format6)
                sheet.write(10, 14, 'Fixed Assets/Vat', format6)
                # sheet.write(11, 12, 'Export Ref No.', format6)
                # sheet.write(11, 13, 'Export Ref Date', format6)
                
                row1 = 11
                if record:
                    purchase_total = 0.0
                    non_taxable_total = 0.0
                    taxable_total = 0.0
                    tax_total = 0.0
                    for rec in record:
                        for lines in rec.invoice_line_ids:
                            # products.append(lines.product_id.name)

                            sheet.write(row1, 0, str(rec.invoice_date.strftime('%Y.%m.%d')), format3)
                            sheet.write(row1, 1, str(rec.name), format3)
                            # if rec.partner_id.parent_id:
                            #     sheet.write(row, 2, str(rec.partner_id.parent_id.name), format3)
                            #     if rec.partner_id.parent_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)


                            # else:
                            #     sheet.write(row, 2, str(rec.partner_id.name), format3)
                            #     if rec.partner_id.vat:
                            #         sheet.write(row, 3, str(rec.partner_id.vat), format3)
                            #     else:
                            #         sheet.write(row, 3, "", format3)

                            sheet.write(row1, 2, str(rec.partner_id.name), format3)
                            if rec.partner_id.vat:
                                sheet.write(row1, 3, str(rec.partner_id.vat), format3)
                            else:
                                sheet.write(row1, 3, "", format3)

                            sheet.write(row1, 4, str(lines.product_id.name), format3)
                            sheet.write(row1, 5, str(lines.quantity), format4)



                            # For UoM Value
                            sheet.write(row1, 6, str(lines.product_uom_id.name), format4)


                            sheet.write(row1, 7, str(lines.price_total), format4)

                            # sheet.write(row1, 7, '0.0', format4)
                            if not lines.tax_ids:
                                sheet.write(row1, 8, lines.price_subtotal, format4)
                                sheet.write(row1, 9, '0.0', format4)
                            else:
                                sheet.write(row1, 8, '0.0', format4)
                                sheet.write(row1, 9, lines.price_subtotal, format4)
                            # sheet.write(row1, 8, str(lines.price_subtotal), format4)
                            
                            if lines.tax_ids:
                                sheet.write(row1, 10, str(round(lines.price_total-lines.price_subtotal, 3)), format4)
                            sheet.write(row1, 11, '0.0', format4)
                            sheet.write(row1, 12, "", format4)
                            # sheet.write(row, 12,"N/A", format4)
                            # sheet.write(row, 13,"N/A", format4)
                            # sheet.write(row1, 12, "N/A", format4)
                            # sheet.write(row1, 13,"N/A", format4)
                            row1 = row1+1
                    #     invoice_lines = []
                    #     for lines in rec.invoice_line_ids:
                    #         product = {
                                
                    #             'description'    : lines.product_id.name,
                    #             'quantity'       : lines.quantity,
                    #             'price_unit'     : lines.price_unit,
                    #             'price_subtotal' : lines.price_each_subtotal 
                    #         }
                    #         if lines.invoice_line_tax_ids:
                    #             taxes = []
                    #             for tax_id in lines.invoice_line_tax_ids:
                    #                 taxes.append(tax_id.name)
                    #             product['invoice_line_tax_ids'] = taxes
                    #         invoice_lines.append(product)
                        final_value['partner_id'] = rec.partner_id.name
                        final_value['pan_number'] = rec.partner_id.vat
                        final_value['address_buyer'] = rec.partner_id.street
                        final_value['company_id'] = rec.company_id.name
                        final_value['pan_number_seller'] = rec.company_id.vat
                        final_value['address_seller'] = rec.company_id.street
                        final_value['date_invoice'] = rec.invoice_date
                        # final_value['date_due'] = rec.date_due
                        final_value['number'] = rec.name
                        final_value['currency_id'] = rec.currency_id
                        # final_value['state'] = dict(self.env['account.invoice'].fields_get(allfields=['state'])['state']['selection'])[rec.state]
                        # final_value['payment_term_id'] = rec.payment_term_id.name
                        # final_value['origin'] = rec.origin
                        final_value['amount_untaxed'] = rec.amount_untaxed
                        # final_value['amount_subtotal_1'] = rec.amount_actual
                        final_value['amount_discount'] = "0.00"
                        final_value['amount_tax'] = rec.amount_tax
                        final_value['amount_total'] = rec.amount_total
                        # final_value['amnt_in_words'] = rec.get_amount_in_words()
                        # sheet.write(row1, 4,  str(final_value['amount_total']), format4)
                        # sheet.write(row1, 5, '0.0', format4)
                        # sheet.write(row1, 6, '0.0', format4)
                        # sheet.write(row1, 7,   str(final_value['amount_discount']), format4)
                        # sheet.write(row1, 8, str(final_value['amount_untaxed']), format4)
                        # sheet.write(row1, 9,  str(final_value['amount_tax']), format4)
                        # row1=row1+1
                        # sheet.write(row1, 7, str(final_value['amount_total']), format5)
                        purchase_total += rec.amount_total
                        if not lines.tax_ids:
                            non_taxable_total += rec.amount_untaxed
                            # sheet.write(row1, 8, str(final_value['amount_untaxed']), format5)
                            # sheet.write(row1, 9, '0.0', format5)
                        else:
                            taxable_total += rec.amount_untaxed
                            # sheet.write(row1, 8, '0.0', format5)
                            # sheet.write(row1, 9, str(final_value['amount_untaxed']), format5)
                        tax_total += rec.amount_tax
                        # sheet.write(row1, 10, str(final_value['amount_tax']), format5)

                    sheet.write(row1, 6, "Grand Total", format5)
                    sheet.write(row1, 7, purchase_total, format5)
                    sheet.write(row1, 8, non_taxable_total, format5)
                    sheet.write(row1, 9, taxable_total, format5)
                    sheet.write(row1, 10, tax_total, format5)
                    
            path = ("/home/odoo/Reports/IRD_Sales_Purchase_Book_Ext.xls")

            # directory = os.path.dirname(path)
            # if not os.path.exists(directory):
            #     os.makedirs(directory)

            # os.chmod(directory, 0o777)    
            # path = ("/mnt/extra-addons/ird_sales_purchase_report_ext/Reports/Partner_detailed_report.xls")
            workbook.save(path)
            file = open(path, "rb")
            file_data = file.read()
            out = base64.encodebytes(file_data)
            self.write({'state': 'get', 'file_name': out, 'invoice_data': 'IRD_Sales/Purchase_Book_Ext.xls'})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ird.sales.purchase.report.ext',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'target': 'new',
                }                
        else:
            raise UserError(_("Currently No Invoice/Bills For This Data!!"))
