
{
    'name': 'Real time Stock Inventory Valuation Report (PDF/EXCEL) in odoo',
    'version': '15.0.0.7',
    'category': 'Warehouse',
    'price': 89,
    'currency': "EUR",
    'summary': 'print product inventory Valuation Report real time stock inventory report for particular date Stock Inventory Real Time Report stock card stockcard inventory cost reports real time inventory valuation report Periodically Stock valuation Report stock report',
    'description': """
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['stock','sale','account','purchase','sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_daybook_report_product_category_wizard.xml',
        'views/report_pdf.xml',
        'views/inventory_valuation_detail_template.xml',
    ],
    'live_test_url':'https://youtu.be/Lpr2cqdzs_I',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images":["static/description/Banner.png"],
}


