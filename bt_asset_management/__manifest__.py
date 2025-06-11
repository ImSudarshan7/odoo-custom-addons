{
    'name': 'Asset Management',
    'version': '15.0.1',
    'category': 'custom',
    'summary': 'Asset Management',
    'license': 'LGPL-3',
    'description': """
     Asset management is a simple system to manage assets owned by an organization.
""",
    'author' : 'BroadTech IT Solutions Pvt Ltd',
    'website' : 'http://www.broadtech-innovations.com',
    'depends': ['base','mail'],
    'images': ['static/description/banner.jpg'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/asset_sequence.xml',
        'views/asset_view.xml',
        'views/asset_move_view.xml'
             
             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}


