{
    'name': 'sale and purchase reports',
    'version': '15.0.0',
    'category': 'Reporting',
    'sequence': -100,
    'author': 'Devendra Stha',
    'summary': 'Generating reports for sales and purchase',
    'description': """
        This module provides sales and purchase report to the clients.
    """,
    'depends': ['ab_global_autopoint', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_template.xml',
        'wizards/report_view.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
