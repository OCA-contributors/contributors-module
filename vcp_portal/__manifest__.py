# Copyright 2026 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp - Portal",
    "summary": "Glue module between Virtual Control Platform and Portal",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,GRAP,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["vcp", "portal"],
    "data": [
        "templates/templates.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "vcp_portal/static/src/components/**/*.esm.js",
            "vcp_portal/static/src/components/**/*.xml",
            "vcp_portal/static/src/components/**/*.scss",
        ],
        "web.assets_tests": [
            "vcp_portal/static/tests/**/*",
        ],
    },
    "auto_install": True,
}
