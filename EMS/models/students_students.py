from odoo import models, fields, api, _

class Students(models.Model):
    _name = 'students.students'
    _description = 'Students Profile'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    roll_no = fields.Integer(string="Roll No.")
    class_id = fields.Many2one('school.class', string="Class", required=True)
    birth_date = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True)  # Added compute method for age
    image = fields.Binary(string="Image")
    address = fields.Char()
    school_id = fields.Many2one('school.name', string="School Name", required=True)
    medium_id = fields.Many2one('school.medium', string="Medium")

    @api.depends('birth_date')  # Dependency on birth_date field
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0
