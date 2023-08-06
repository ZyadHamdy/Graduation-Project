# See LICENSE file for full copyright and licensing details.

import base64

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.modules import get_module_resource

# from lxml import etree
# added import statement in try-except because when server runs on
# windows operating system issue arise because this library is not in Windows.
try:
    from odoo.tools import image_colorize
except Exception:
    image_colorize = False


class StudentStudent(models.Model):
    """Defining a student information."""

    _name = "student.student"
    _table = "student_student"
    _description = "Student Information"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def _default_image(self):
        """Method to get default Image"""
        image_path = get_module_resource(
            "hr", "static/src/img", "default_image.png"
        )
        return base64.b64encode(open(image_path, "rb").read())

    @api.model
    def create(self, vals):
        if not vals.get('ref') or vals['ref'] == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('student.seq') or _('New')
        return super().create(vals)

    name = fields.Char(states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]})
    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))
    email = fields.Char("E-Mail", help="Enter student email")

    student_name = fields.Char(
        "Student Name",
        store=True,
        readonly=True,
        help="Student Name",
    )
    color = fields.Integer("Color Index", help="Index of color")
    pid = fields.Char(
        "Student ID",
        required=True,
        default=lambda self: _("New"),
        help="Personal IDentification Number",
    )
    reg_code = fields.Char(
        "Registration Code", help="Student Registration Code"
    )
    student_ssn = fields.Char("Student SSN", help="Enter student code")
    contact_phone = fields.Char("Phone no.", help="Enter student phone no.")
    contact_mobile = fields.Char("Mobile no", help="Enter student mobile no.")
    email = fields.Char(
        "E-Mail.", help="Enter student roll no."
    )
    photo = fields.Binary(
        "Photo", default=_default_image, help="Attach student photo"
    )

    admission_date = fields.Date(
        "Admission Date",
        default=fields.Date.today(),
        help="Enter student admission date",
    )
    middle = fields.Char(
        "Middle Name",
        required=True,
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Enter student middle name",
    )
    last = fields.Char(
        "Surname",
        required=True,
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Enter student last name",
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        "Gender",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Select student gender",
    )
    date_of_birth = fields.Date(
        "BirthDate",
        required=True,
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Enter student date of birth",
    )
    age = fields.Integer(
        compute="_compute_student_age",
        string="Age",
        readonly=True,
        help="Enter student age",
    )
    maritual_status = fields.Selection(
        [("unmarried", "Unmarried"), ("married", "Married")],
        "Marital Status",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Select student maritual status",
    )

    doctor = fields.Char(
        "Doctor Name",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Enter doctor name for student medical details",
    )
    designation = fields.Char("Designation", help="Enter doctor designation")
    doctor_phone = fields.Char("Contact No.", help="Enter doctor phone")
    blood_group = fields.Char("Blood Group", help="Enter student blood group")
    height = fields.Float("Height", help="Hieght in C.M")
    weight = fields.Float("Weight", help="Weight in K.G")
    eye = fields.Boolean("Eyes", help="Eye for medical info")
    ear = fields.Boolean("Ears", help="Eye for medical info")
    nose_throat = fields.Boolean(
        "Nose & Throat", help="Nose & Throat for medical info"
    )
    respiratory = fields.Boolean(
        "Respiratory", help="Respiratory for medical info"
    )
    cardiovascular = fields.Boolean(
        "Cardiovascular", help="Cardiovascular for medical info"
    )
    neurological = fields.Boolean(
        "Neurological", help="Neurological for medical info"
    )
    muskoskeletal = fields.Boolean(
        "Musculoskeletal", help="Musculoskeletal for medical info"
    )
    dermatological = fields.Boolean(
        "Dermatological", help="Dermatological for medical info"
    )
    blood_pressure = fields.Boolean(
        "Blood Pressure", help="Blood pressure for medical info"
    )
    remark = fields.Text(
        "Remark",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]},
        help="Remark can be entered if any",
    )

    stu_name = fields.Char(
        "First Name",
        readonly=True,
        help="Enter student first name",
        tracking=True,
    )
    Acadamic_year = fields.Char(
        "Year",
        help="Academic Year",
        readonly=True,
        tracking=True,
    )
    terminate_reason = fields.Text(
        "Reason", help="Enter student terminate reason",states={"done": [("readonly", True)], "cancel": [("readonly", True)], "graduated": [("readonly", True)]}
    )
    active = fields.Boolean(
        default=True, help="Activate/Deactivate student record", tracking=True
    )
    teachr_user_grp = fields.Boolean(
        "Teacher Group",
        compute="_compute_teacher_user",
        help="Activate/Deactivate teacher group",
    )
    student_line_ids = fields.One2many('student.student.line', 'student_id')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    archive = fields.Boolean(default=False,
                             help="Set archive to true to hide the student record without deleting it.")
    academic_id = fields.Many2one(
        comodel_name='academic.year',
        string='Academic Year',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('paid', 'Paid'),
                   ('confirm', 'Confirm'),
                   ('done', 'done'),
                   ('cancel', 'Cancelled'),
                   ('graduated', 'Graduated'),
                   ],
        required=False, default='draft')
    paid = fields.Boolean(
        string='Paid',
        required=False)

    def action_pay(self):
        self.state = 'paid'

    def action_graduated(self):
        self.state = 'graduated'

    def action_confirm(self):
        self.state = 'confirm'
        self.paid = True


    def action_done(self):
        self.state = 'done'
        return self.env.ref("sms_school.action_bank_wizard_action").sudo().read()[0]
    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('student_line_ids.expenses')
    def _amount_all(self):
        total = 0.0
        for line in self.student_line_ids:
            total += line.subtotal
        self.amount_total = total

    @api.depends("date_of_birth")
    def _compute_student_age(self):
        """Method to calculate student age"""
        current_dt = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.date_of_birth and rec.date_of_birth < current_dt:
                start = rec.date_of_birth
                age_calc = (current_dt - start).days / 365
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains("date_of_birth")
    def check_age(self):
        """Method to check age should be greater than 6"""
        if self.date_of_birth:
            start = self.date_of_birth
            age_calc = (fields.Date.today() - start).days / 365
            # Check if age less than required age
            if age_calc < 6:
                raise ValidationError(
                    _(
                        "Age of student should be greater than 6 years!"
                    )
                )


class StudentStudentLine(models.Model):
    """Defining a student information."""

    _name = "student.student.line"
    _table = "student_student_line"
    _description = "Student Information"

    expenses = fields.Float("Expenses")
    discount = fields.Float("Discount %", default=0, help="employee's' discount")
    date = fields.Date()
    year = fields.Char(string='Year')
    status_of_pay = fields.Selection(
        string='Status of pay',
        selection=[('paid', 'Paid'),
                   ('not_paid', 'Not Paid'),
                   ('free_year', 'Free Year'),
                   ],
        required=False, )
    student_id = fields.Many2one('student.student')
    subtotal = fields.Integer("Subtotal", compute='_calc_subtotal')
    school_employee_id = fields.Many2one('school.employee')
    currency_id = fields.Many2one('res.currency', related='school_employee_id.currency_id', string='Currency')

    @api.depends('expenses', 'discount')
    def _calc_subtotal(self):
        for line in self:
            if line.discount != 0:
                subtotal = (line.expenses * (line.discount / 100))
                line.subtotal = line.expenses - subtotal
            elif line.discount == 0:
                print("elif")
                subtotal = line.expenses * 1
                line.subtotal = subtotal
            else:
                pass
        if self.subtotal < 0:
            raise ValidationError('Subtotal must be greater than zero')

    @api.constrains('discount')
    def _calc_discount(self):
        for line in self:
            if line.discount > 50:
                raise ValidationError('Subtotal can not be greater than 50%')
