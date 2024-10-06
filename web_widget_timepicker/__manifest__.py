# -*- coding: utf-8 -*-
#2023 sandesh paudel
{
    "name": "Web Timepicker Widget",
    "version": "GAP-1.0.1",
    "author": "Sandesh Paudel",
    "category": "Web",
    "depends": [ "web" ],
    "css": [
        "static/src/lib/jquery.timerpicker/jquery.timepicker.css",
        "static/src/css/web_widget_timepicker.css",
    ],
    "js": [
        "static/src/lib/jquery.timerpicker/jquery.timepicker.js",
        "static/src/js/web_widget_timepicker.js",
    ],
    "data": [
        "views/web_widget_timepicker_assets.xml",
    ],
    "qweb": [
        "static/src/xml/web_widget_timepicker.xml",
    ],
     'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,

}
