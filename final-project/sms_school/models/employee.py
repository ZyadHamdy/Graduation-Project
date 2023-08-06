# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.modules import get_module_resource
from odoo.exceptions import ValidationError
import base64


class SchoolEmployee(models.Model):
    """Defining a employee information."""

    _name = "school.employee"
    _description = "employee Employee"
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
            vals['ref'] = self.env['ir.sequence'].next_by_code('employee.seq') or _('New')
        return super().create(vals)

    ref = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))


    name = fields.Char(required=True)
    email = fields.Char("E-Mail", help="Enter student email")
    middle = fields.Char(
        "Middle Name",
        required=True,
        help="Enter student middle name",
    )
    last = fields.Char(
        "Surname",
        required=True,
        help="Enter student last name",
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        "Gender",
        help="Select student gender",
    )
    photo = fields.Binary(
        "Photo", default=_default_image, help="Attach student photo"
    )
    date_of_birth = fields.Date(
        "BirthDate",
        help="Enter student date of birth",
        default=fields.Date.today
    )
    color = fields.Integer("Color Index", help="Index of color")
    age = fields.Integer(
        string="Age",
        help="Enter student age",
    )
    contact_phone = fields.Char("Phone no.", help="Enter student phone no.")
    contact_mobile = fields.Char("Mobile no", help="Enter student mobile no.")
    employee_ssn = fields.Char(
        string='Employee SNN',
    )
    school_employee_line_ids = fields.One2many('school.employee.line', 'school_employee_id')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    company_id = fields.Many2one(comodel_name='res.company', string='Company',default=lambda self:self.env.company)
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id',string='Currency')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('paid', 'Paid'),
                   ('confirm', 'Confirm'),
                   ('done', 'done'),
                   ('cancel', 'Cancelled'),
                   ],
        required=False, default='draft')
    paid = fields.Boolean(
        string='Paid',
        required=False)

    def action_pay(self):
        self.state = 'paid'

    def action_confirm(self):
        self.state = 'confirm'
        self.paid = True
    def action_done(self):
        self.state = 'done'
        return self.env.ref("sms_school.action_bank_wizard_action").sudo().read()[0]

    def action_cancel(self):
        self.state = 'cancel'


    @api.depends('school_employee_line_ids.salary', 'school_employee_line_ids.taxes_in_percentage',
                 'school_employee_line_ids.reward')
    def _amount_all(self):
        total = 0.0
        for line in self.school_employee_line_ids:
            total += line.subtotal
        self.amount_total = total


class SchoolEmployeeLines(models.Model):
    _name = "school.employee.line"
    _description = "Employee Information Lines"

    salary = fields.Integer("Salary", help="employee's salary'")
    taxes_in_percentage = fields.Float("Taxes Percentage %", default=0, help="employee's' Taxes",readonly=True)
    taxes = fields.Integer("Taxes", help="employee's' Taxes")
    taxes_ids = fields.One2many('account.tax', 'school_employee_line_id')
    reward = fields.Integer("Reward")
    date = fields.Date("Date",default=fields.Date.today)
    subtotal = fields.Integer("Subtotal", compute='_calc_subtotal')
    school_employee_id = fields.Many2one('school.employee')
    currency_id = fields.Many2one('res.currency', related='school_employee_id.currency_id', string='Currency')

    @api.depends('salary', 'taxes_in_percentage', 'reward')
    def _calc_subtotal(self):
        for line in self:
            if line.taxes_in_percentage != 0:
                subtotal = (line.salary * (line.taxes_in_percentage / 100)) + line.reward
                line.subtotal = line.salary - subtotal
            elif line.taxes_in_percentage == 0:
                subtotal = line.salary * 1 + line.reward
                line.subtotal = subtotal
            else:
                pass
        if self.subtotal < 0:
            raise ValidationError('Subtotal must be greater than zero')

    @api.onchange('taxes_ids')
    def get_taxes_in_percentage(self):
        taxes = 0.0
        for tax in self.taxes_ids:
            taxes += tax.amount
        self.taxes_in_percentage = taxes
        print(taxes)


class TaxesInherit(models.Model):
    _inherit = "account.tax"

    school_employee_line_id = fields.Many2one('school.employee.line')
