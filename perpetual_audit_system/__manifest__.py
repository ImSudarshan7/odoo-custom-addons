{
    'name': 'Perpetual Audit System',
    'version': '1.0',
    'summary': 'A custom module for managing perpetual audits in Odoo 16',
    'description': """
        This module helps manage auditing processes, including item assignment,
        auditor management, audit log tracking, and API integration with external systems.
    """,
    'author': 'Bipin Shrestha',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/audit_location_views.xml',
        'views/audit_item_views.xml',
        'views/audit_session_views.xml',
        'views/menus.xml',
    ],
    'demo': ['data/demo_data.xml'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
