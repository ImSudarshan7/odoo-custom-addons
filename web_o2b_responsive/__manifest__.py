##########################################################################
# Author      : O2b Technologies Pvt. Ltd.(<www.o2btechnologies.com>)
# Copyright(c): 2016-Present O2b Technologies Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
##########################################################################

{
    "name": "Web Responsive",
    "summary": "Responsive web client, community-supported",
    "version": "15.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/web",
    "author": "LasLabs, Tecnativa, ITerra, " "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["web", "mail"],
    "development_status": "Production/Stable",
    "maintainers": ["Yajo", "Tardo", "SplashS"],
    "excludes": ["web_enterprise"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users.xml",
        "views/res_config_settings_view.xml",
        "views/web.xml",
        "views/database_schedule.xml"
    ],
    "assets": {
        'web._assets_primary_variables': [
            '/web_o2b_responsive/static/src/colors.scss',
            '/web_o2b_responsive/static/src/legacy/scss/colors.scss'
        ],
        'web._assets_backend_helpers': [
            '/web_o2b_responsive/static/src/variables.scss',
        ],
        "web.assets_frontend": [
            "/web_o2b_responsive/static/src/legacy/js/website_apps_menu.js",
            "/web_o2b_responsive/static/src/legacy/scss/website_apps_menu.scss",
        ],
        "web.assets_backend": [
            "/web_o2b_responsive/static/src/legacy/scss/web_responsive.scss",
            # "/web_responsive/static/src/legacy/scss/colors.scss",
            "/web_o2b_responsive/static/src/legacy/scss/style.scss",
            "web_o2b_responsive/static/src/legacy/js/web_responsive.js",
            "/web_o2b_responsive/static/src/legacy/scss/kanban_view_mobile.scss",
            "/web_o2b_responsive/static/src/legacy/js/kanban_renderer_mobile.js",
            "/web_o2b_responsive/static/src/components/ui_context.esm.js",
            "/web_o2b_responsive/static/src/components/apps_menu/apps_menu.scss",
            "/web_o2b_responsive/static/src/components/apps_menu/apps_menu.esm.js",
            "/web_o2b_responsive/static/src/components/navbar/main_navbar.scss",
            "/web_o2b_responsive/static/src/components/navbar/navbar.js",
            "/web_o2b_responsive/static/src/components/control_panel/control_panel.scss",
            "/web_o2b_responsive/static/src/components/control_panel/control_panel.esm.js",
            "/web_o2b_responsive/static/src/components/search_panel/search_panel.scss",
            "/web_o2b_responsive/static/src/components/search_panel/search_panel.esm.js",
            "/web_o2b_responsive/static/src/components/attachment_viewer/attachment_viewer.scss",
            "/web_o2b_responsive/static/src/components/attachment_viewer/attachment_viewer.esm.js",
            "/web_o2b_responsive/static/src/components/hotkey/hotkey.scss",
        ],
        "web.assets_qweb": [
            "/web_o2b_responsive/static/src/legacy/xml/form_buttons.xml",
            "/web_o2b_responsive/static/src/components/apps_menu/apps_menu.xml",
            "/web_o2b_responsive/static/src/components/control_panel/control_panel.xml",
            "/web_o2b_responsive/static/src/components/navbar/main_navbar.xml",
            "/web_o2b_responsive/static/src/components/search_panel/search_panel.xml",
            "/web_o2b_responsive/static/src/components/attachment_viewer/attachment_viewer.xml",
            "/web_o2b_responsive/static/src/components/hotkey/hotkey.xml",
        ],
        "web.assets_tests": [
            "/web_o2b_responsive/static/tests/test_patch.js",
        ],
    },
    "sequence": 1,
}
