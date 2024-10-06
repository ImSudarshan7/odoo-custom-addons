# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'VAT INVOICE IRD',
    'version': '15.0.1',
    'summary': 'Nepali VAT Bill/ IRD Integration',
    'description': "Nepali VAT System",
    'category': 'Accounting',
    'author': 'SLM',
    'license': 'AGPL-3',
    'data': [

        'report/vat_invoice_pdf.xml',
        'report/vat_sales_invoice_pdf.xml',
        'view/res_cmpny.xml',
        'view/account_move_inherited.xml',
        'view/ir_actions_report_xml.xml',
        'view/res_config_view.xml',
        'data/data.xml',
    ],
    'depends': ['base', 'sale_management', 'account'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
