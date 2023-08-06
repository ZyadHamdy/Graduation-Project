# Created by zyadhamdy at 8:08 PM 5/11/23 using PyCharm
# See LICENSE file for full copyright and licensing details.

# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _

EM = r"[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"


def emailvalidation(email):
    """Check valid email."""
    if email:
        email_regex = re.compile(EM)
        if not email_regex.match(email):
            raise ValidationError(
                _(
                    """This seems not to be valid email.
Please enter email in correct format!"""
                )
            )


class AcademicYear(models.Model):
    """Defines an academic year."""

    _name = "academic.year"
    _description = "Academic Year"
    _order = "sequence"

    sequence = fields.Integer(
        "Sequence",
        required=True,
        help="Sequence order you want to see this year.",
    )
    name = fields.Char("Name", required=True, help="Name of academic year")
    code = fields.Char("Code", required=True, help="Code of academic year")
    date_start = fields.Date(
        "Start Date", required=True, help="Starting date of academic year"
    )
    date_stop = fields.Date(
        "End Date", required=True, help="Ending of academic year"
    )

    current = fields.Boolean("Current", help="Set Active Current Year")
    description = fields.Text("Description", help="Description")

    @api.model
    def next_year(self, sequence):
        """This method assign sequence to years"""
        year_rec = self.search(
            [("sequence", ">", sequence)], order="id", limit=1
        )
        if year_rec:
            return year_rec.id or False

    def name_get(self):
        """Method to display name and code"""
        return [(rec.id, " [" + rec.code + "]" + rec.name) for rec in self]