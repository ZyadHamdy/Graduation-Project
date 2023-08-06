# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolBank(models.Model):
    _name = 'school.bank'
    _description = 'school.bank'

    name = fields.Char('Bank Name', required=True)
    bank_code = fields.Char('Bank Identifier Code', required=True)
    country_id = fields.Many2one('res.country', 'Country', required=True)
