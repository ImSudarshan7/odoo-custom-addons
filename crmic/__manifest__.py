{
    'name': 'CRMIC',
    'version': '1.0.0',
    'category': 'Customization for Kalashshop',
    'sequence': -1,
    'author': 'Sudarshan',
    'summary': 'Customization for Kalashshop in CRMIC production materials',
    'description': """
        This module provides customizations for the Kalashshop in CRMIC.

    """,
    'depends': ['base', 'contacts', 'mail', 'stock',],
    'data': [
        # # 'security/ir.model.access.csv',
        # 'views/res_partner_view.xml',
        # 'views/oder_view.xml',
        'views/stock_picking_view.xml',
        # 'views/purchase_view.xml',
        # 'reports/challan_report.xml',
        # 'reports/challan_template.xml',
        # 'reports/purchase_order_report.xml',
        # 'reports/purchase_order_template.xml',
        # 'reports/manufacture_order_report.xml',
        # 'reports/manufacture_order_template.xml',

    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3',
}
