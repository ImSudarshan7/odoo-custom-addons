{
    'name': 'CRMIC_PROD',
    'version': '1.0.0',
    'category': 'Customization for Kalashshop',
    'sequence': -100,
    'author': 'Devendra Stha',
    'summary': 'Customization for Kalashshop in CRMIC production materials',
    'description': """
        This module provides customizations for the Kalashshop in CRMIC_PROD.
        
    """,
    'depends': ['base', 'contacts', 'mail', 'sale', 'stock', 'purchase', 'mrp','account', 'sale_stock'],
    'data': [
        'security/security.xml',
        'views/res_partner_view.xml',
        'views/oder_view.xml',
        'views/sales_view.xml',
        'views/stock_picking_view.xml',
        'views/manufacturing_view.xml',
        'views/purchase_view.xml',
        'views/stock_move.xml',
        'reports/challan_report.xml',
        'reports/challan_template.xml',
        'reports/purchase_order_report.xml',
        'reports/purchase_order_template.xml',
        'reports/manufacturing_order_report.xml',
        'reports/manufacturing_order_template.xml',

    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3',
}
