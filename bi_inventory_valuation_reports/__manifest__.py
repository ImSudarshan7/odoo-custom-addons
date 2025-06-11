{
    'name': 'Real-Time Stock Inventory Valuation Report (PDF/EXCEL) in Odoo',
    'version': '15.0.0.6',
    'category': 'Warehouse',
    'price': 89,
    'currency': "EUR",
    'summary': 'Generate real-time stock inventory valuation reports in PDF and Excel, covering stock quantities, costs, and valuation by specific date or period.',
    'description': """
    This module offers real-time inventory valuation reporting in PDF and Excel formats. Users can access accurate stock quantities, costs, and inventory movements by date. It supports customizable valuation, cost tracking, and warehouse reporting for quick insights into stock levels and values.
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['stock', 'sale', 'account', 'purchase', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_day_book_wizard_view.xml',
    ],
    'live_test_url': 'https://youtu.be/Lpr2cqdzs_I',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images": ["static/description/Banner.png"],
}
