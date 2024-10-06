# -*- coding: utf-8 -*-
import xlwt
import base64
import calendar
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
import tempfile


class JobOrderSummaryReport(models.TransientModel):
    _name = "joborder.summary"
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)
    make_id = fields.Many2one('vehicle.make', string="Make")
    report_data = fields.Char('Name',)
    file_name = fields.Binary('Job Order Summary Excel Report', readonly=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
    _sql_constraints = [
            ('check','CHECK((start_date <= end_date))',"End date must be greater then start date")
    ]

    # @api.model
    def action_joborder_summary_report(self):
        if self.make_id:
            domain = [('date_in', '>=', self.start_date), ('date_in', '<=', self.end_date), ('vehicle_id.make_id', '=', self.make_id.id)]
        else:
            domain = [('date_in', '>=', self.start_date), ('date_in', '<=', self.end_date)]

        job_order_summary = self.env['job.order'].search(domain)

        if not job_order_summary:
            raise UserError("Currently No Job Orders For This Data!!")

        record = [rec for rec in job_order_summary]
        record.sort(key=lambda p: p.date_in)  # Sort the records by date_in
        data1 = {
            'start': str(self.start_date),
            'end': str(self.end_date)
        }
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Job Order Summary Report')

        # Column Width
        sheet.col(0).width = int(30 * 45)
        sheet.col(1).width = int(30 * 270)
        sheet.col(2).width = int(18 * 260)
        sheet.col(3).width = int(18 * 250)
        sheet.col(4).width = int(33 * 200)
        sheet.col(5).width = int(23 * 230)
        sheet.col(6).width = int(18 * 230)
        sheet.col(7).width = int(30 * 180)
        sheet.col(8).width = int(30 * 300)
        sheet.col(9).width = int(30 * 300)
        sheet.col(10).width = int(30 * 240)

        #Defining Formats
        format0 = xlwt.easyxf('font:height 500,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        format1 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz left')
        format2 = xlwt.easyxf('font:bold True;align: horiz left')
        format3 = xlwt.easyxf('align: horiz left')
        format4 = xlwt.easyxf('align: horiz right')
        format5 = xlwt.easyxf('font:bold True;align: horiz right')
        format6 = xlwt.easyxf('font:bold True;pattern: pattern solid, fore_colour gray25;align: horiz right')
        format7 = xlwt.easyxf('font:bold True;borders:top thick;align: horiz right')
        format8 = xlwt.easyxf('font:bold True;borders:top thick;pattern: pattern solid, fore_colour gray25;align: horiz left')

        timestamp = str(datetime.today())
        row=13
        i=1
        # total=0.00

        #Writing in Sheets
        sheet.write_merge(0, 2, 0, 11, 'Monthly Vehicle Flow Report', format0)
        sheet.write(5, 1, "Organization Name", format1)
        sheet.write(5, 2, str("Global Auto Point"), format2)
        sheet.write(6, 1, "Location", format1)
        sheet.write(6, 2, str("Biratnagar"), format2)
        sheet.write(7, 1, "Reported By", format1)
        sheet.write(7, 2, str(self.env.user.name), format2)
        sheet.write(9, 1, "Duration of Report", format1)
        sheet.write(9, 2, data1['start'], format2)
        sheet.write(9, 3, 'To', format2)
        sheet.write(9, 4, data1['end'], format2)
        sheet.write(10, 1, 'Report generated at:', format1)
        sheet.write(10, 2, timestamp, format2)

        sheet.write(12, 0, 'S.No', format1)
        sheet.write(12, 1, "Customer's Name", format1)
        sheet.write(12, 2, "Job Card No.", format1)
        sheet.write(12, 3, 'Contact Number', format1)
        sheet.write(12, 4, 'Vehicle Reg. No.', format1)
        sheet.write(12, 5, 'Date of failure', format1)
        sheet.write(12, 6, 'Model Code', format1)
        sheet.write(12, 7, 'Model Name', format1)
        sheet.write(12, 8, 'KM In', format1)
        sheet.write(12, 9, 'Job Instruction', format1)
        sheet.write(12, 10, "Supervisor's Report", format1)
        sheet.write(12, 11, "Remarks by Supervisor", format1)
        sheet.write(12, 12, "Job Order Status", format1)

        for rec in record:
            sheet.write(row, 0, str(i), format3)
            sheet.write(row, 1, str(rec.customer_id.name), format3)
            sheet.write(row, 2, str(rec.name), format3)

            if rec.mobile:
                sheet.write(row, 3, str(rec.mobile), format3)
            else:
                sheet.write(row, 3, str(""), format3)
            sheet.write(row, 4, str(rec.vehicle_id.vehicle_no), format3)
            sheet.write(row, 5, str(rec.date_in), format3)
            sheet.write(row, 6, str(rec.vehicle_id.model_no), format3)
            sheet.write(row, 7, str(rec.vehicle_id.name), format3)
            sheet.write(row, 8, str(rec.odometer), format3)
            if rec.job_instruction:
                sheet.write(row, 9, str(rec.job_instruction), format3)
            else:
                sheet.write(row, 9, str(""), format3)
            if rec.technician_report:
                sheet.write(row, 10, str(rec.technician_report), format3)
            else:
                sheet.write(row, 10, str(""), format3)
            sheet.write(row, 11, str(""), format3)
            sheet.write(row, 12, str(rec.state), format3)
            row += 1
            i += 1

        # Saving File in a Temporary Directory
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xls') as temp_file:
            workbook.save(temp_file.name)
            temp_file.seek(0)
            file_data = temp_file.read()
            out = base64.b64encode(file_data)
            self.write({'state': 'get', 'file_name': out, 'report_data': 'Vehicle Flow Report.xls'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'joborder.summary',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }