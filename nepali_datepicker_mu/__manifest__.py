# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#################################################################################

# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
    # Application Information
    'name' : 'Nepali Datepicker',
    'category' : 'Extra Tools',
    'version' : '10.0.1',
    #'license': 'OPL-1',
    
    'summary': """Odoo Web Nepali Datepicker. The Nepali calendar is the official calendar in Nepal.""",
    'description': """
        Odoo Nepali Datepicker. The Nepali calendar is a purely lunar calendar.
    """,
    
    # Author Information
    'author': 'Sagar',
    
    # Dependencies
    'depends': ['web'],
    'sequence': 1,

    # Views
    'data': [
        'views/assets.xml',
    ],

    'qweb' : [
        "static/src/xml/*.xml",
    ],
    
    # Technical
    'installable': True,
    'application' : True,
    'auto_install': False,
    'active': False,
}