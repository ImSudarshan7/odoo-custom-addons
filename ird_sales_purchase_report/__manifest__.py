# -*- coding: utf-8 -*-
{
    'name': 'IRD Sales&Purchase Register',
    'version': '15.0',
    'category': 'Accounts',
    'summary': ' IRD compliance Sales/Purchase Report',
    'author': 'SLM',
    'license': "OPL-1",
    'depends': [
        'base',
        'account',
        'sale_management',
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/ird_sales_purchase_report_ext_view.xml',
    ],
    'demo': [],
    'auto_install': False,
    'installable': True,
    'application': True
}
