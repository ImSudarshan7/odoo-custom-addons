{
    'name': "Advanced Dynamic Dashboard",
    'version': '15.0.1.0.0',
    'category': 'Productivity',
    'summary': """Helps to create configurable dashboards easily.""",
    'description': """This module helps to create configurable advanced dynamic 
     dashboard to get the information that are relevant to your business, 
     department or a specific process or need.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['web', 'hr', 'point_of_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data_view.xml',
        'views/dynamic_block_views.xml',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'advanced_dynamic_dashboard/static/lib/css/gridstack.min.css',
            'advanced_dynamic_dashboard/static/src/css/dynamic_dashboard.css',
       
            'advanced_dynamic_dashboard/static/src/scss/dynamic_dashboard.scss',
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css",
            'https://cdnjs.cloudflare.com/ajax/libs/gridstack.js/0.2.6/gridstack.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js',
            "https://cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.3/jquery.ui.touch-punch.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/bootbox.js/4.4.0/bootbox.min.js",
            'https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.5.3/jspdf.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js',
            'advanced_dynamic_dashboard/static/src/js/dynamic_dashboard.js',
            'https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700'
        ],
        'web.assets_qweb': [
            'advanced_dynamic_dashboard/static/src/xml/dynamic_dashboard_template.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': True,
}
