# -*- coding: utf-8 -*-

{
    'name': " Sales Person Area Route ",
    'version': '15.0.0.0',
    'author': "ByteLegions",
    'website': "http://www.bytelegions.com",
    'depends': ['base', 'contacts'],
    'license': 'LGPL-3',
    'category': 'contact',
    'company': 'Bytelegion',
    'summary': """ This Module use for Salesperson on base of Area and User
     will be able to lot area and customer ill be only show of given lot area""",
    'description': """ This module allows to set are route day wise to salesperson. 
    Hence, the customers in the specific route can be viewed for each day.""",
    'sequence': 1,

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'views/sales_person_view.xml',
        'views/inherit_res_partner_view.xml',
        'views/sales_person_areas_view.xml',

        'data/sequence.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'],

}
