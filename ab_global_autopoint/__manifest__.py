# -*- coding: utf-8 -*-
#2023 sandesh Paudel
{
    'name': "Global Auto Point",
    'version': 'GAP-1.0.1',
    'summary': 'This app will handle all the enterprise activities of the AB Group of Company: Global Autopoint',
     'description': "This app will handle all the enterprise activities of the AB Group of Company: Global Autopoint",
    'author': "Bishwas Pudasaini",
    'sequence':'-100',
    'company': 'CRMIC',
    'category': 'Extra Tools',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/account_invoice.xml',
        'views/sale.xml',
        'views/vehicle.xml',
        'views/product_template.xml',
        'views/hr_employee.xml',
        'views/workorder.xml',
        'views/res_company_views.xml',
        'data/sequence.xml',
        'reports/report.xml',
        'reports/job_card.xml',
        'reports/sale_report.xml',
        'reports/sale_excel_xls.xml',
        'reports/quotation_template.xml'
    ],
    'depends': ['base', 'mail', 'sale', 'hr', 'web_widget_timepicker', 'stock'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
