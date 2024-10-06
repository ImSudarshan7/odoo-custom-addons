# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Excel Report",

    'summary': """
        A detailed excel report for manufacturing processes in Odoo.
    """,

    'description': """
        This module provides a detailed report for manufacturing processes, allowing users to generate and print excel reports based on various criteria.
    """,

    'author': "Devendra Shrestha",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['mrp', 'CRMIC_PROD', 'serial_no_from_mo','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/mrp_report_template.xml',
        'wizards/mrp_detail_report_views.xml',
    ],
}
