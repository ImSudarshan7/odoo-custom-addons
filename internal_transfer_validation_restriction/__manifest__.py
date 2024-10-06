# __manifest__.py
{
    'name': 'Internal Transfer Validation Restriction',
    'version': '1.0',
    'depends': ['stock'],
    'category': 'Warehouse',
    'summary': 'Restrict validation of internal transfers to allowed users in the destination location',
    'data': [
        'views/stock_location_views.xml',
    ],
    'application': False,
}
