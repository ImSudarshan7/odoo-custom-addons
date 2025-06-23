# -*- coding: utf-8 -*-
{
    'name': "Matrialized Report IRD",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SLM",
    'category': 'Uncategorized',
    'version': '15.0.0.1',
    'depends': ['base', 'account', 'web','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'reports/paper_format.xml',
        'reports/ird_report.xml',
    ],
 
}