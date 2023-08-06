from odoo import models, fields, api


class WizardBank(models.TransientModel):
    _name = 'wizard.bank'

    date = fields.Datetime('Date',required=True,default=fields.Date.today)
    bank_id = fields.Many2one('school.bank', string='BANK',required=True)
    account_number = fields.Char('Account Number',required=True)


    def confirm_paymeny(self):
        message = "The Payment Done Successfully"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': message,
                'type': 'rainbow_man',
            }
        }
