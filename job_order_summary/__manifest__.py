{
    'name': 'Vehicle Flow Report',
    'version': '15.0.1',
    'summary': 'This app will generate Job Order Summary Report',
    'description': "This app will generate Job Order Summary Report'",
    'category': 'Extra Tools',
    'author': 'Sandesh Paudel',
    "license": "LGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'wizard/job_order_summary.xml'
    ],
    'depends': ['base','ab_global_autopoint'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
