{
    'name': "sms_school",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/student_sequence.xml',
        'data/employee_sequence.xml',
        'data/teacher_sequence.xml',
        'views/views.xml',
        'views/student_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/employee_view.xml',
        'views/academic_year.xml',
        'views/school_bank.xml',
        'views/taxes.xml',
        'views/menus.xml',
        'wizard/bank.xml',
        'report/student_report.xml',
        'report/teacher_report.xml',
        'report/employee_report.xml',
        'report/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
