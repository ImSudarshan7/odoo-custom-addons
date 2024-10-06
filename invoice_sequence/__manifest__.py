# -*- coding: utf-8 -*-
{
    'name': 'Invoice Location and Sequence Customization',
    'version': '15.0.1.0.1',
    'summary': 'Adds functionality to update the invoice sequence based on the selected location.',
    'description': """
    This module extends the functionality of the Account Move model in Odoo 15 by adding:
    - A new field 'Invoice Location' to select between 'Kathmandu Office' and 'Simara Office'.
    - Automatic generation of an 'Invoice Sequence' based on the selected location.
    - Customization of the invoice form view to display and control the new fields.
    """,
    'category': 'Accounting',
    'author': 'Bipin Shrestha',
    'maintainer': 'Bipin Shrestha',
    'depends': ['account', 'invoice_stock_move'],
    'data': [
        'views/account_move_views.xml',
    ],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
