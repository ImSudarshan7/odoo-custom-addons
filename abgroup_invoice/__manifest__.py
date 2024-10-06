# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Global Auto Point Tax Invoice',
    'version': '15.0.1',
    'summary': 'This app helps to generate Tax Invoice as per IRD clause For AB Group.',
    'description': "Tax Invoice",
    'category': 'Accounting',
    'author': 'Sandesh Paudel',
    'sequence':-100,
    'license': 'LGPL-3',
    'data': [
        'report/invoice_template.xml',
        'report/tax_invoice.xml',
        'views/account_invoice.xml',

    ],
    'depends': ['base', 'account', 'sale',],
    'installable': True,
    'application': True,
    'auto_install': False,

}
