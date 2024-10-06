# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2019-Present Lekhnath Rijal <mail@lekhnathrijal.com.np>
#
##########################################################################


{
    'name': 'Nepali Date System',
    'summary': 'Nepali datepicker and date conversion tool for Odoo',
    'version': '13.0.6.0',
    'author': 'Lekhnath Rijal<mail@lekhnathrijal.com.np>',
    'category': 'Web',
    'description': '''
Nepali Datepicker
Nepali Date System
Bikram Sambat
Bikram Samvat
Odoo Nepali Date
Odoo datepicker
Nepali Calendar
Nepali Date
BS Calendar
BS Date
Nepali date converter
BS date converter
backend
    ''',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'data/config.xml',

        'views/res_config.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/datepicker.xml',
        'static/src/xml/filter.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'nepali_date/static/src/xml/datepicker.xml',
            # 'nepali_date/static/src/xml/filter.xml',
        ],
        'web.assets_backend': [
            'nepali_date/static/lib/jquery.calendars.package-2.1.0',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/css/jquery.calendars.picker.css',
            'nepali_date/static/src/scss/_variables.scss',
            # 'nepali_date/static/lib/jquery.calendars.package-2.1.0',
            'nepali_date/static/src/scss/style.scss',
            'nepali_date/static/src/js/calendar.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.calendars.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.calendars.plus.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.calendars.nepali.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.calendars.nepali-ne.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.plugin.js',
            'nepali_date/static/lib/jquery.calendars.package-2.1.0/js/jquery.calendars.picker.js',
            'nepali_date/static/src/js/main.js',
            # 'nepali_date/views/assets.xml',
        ],
    },
    'images': [
        'static/description/main_screenshot.png',
    ],
    'price': 199,
    'currency': 'EUR',
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
    'application': False,
}
