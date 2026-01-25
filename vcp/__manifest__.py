# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Vcp",
    "summary": """Virtual Control Platform core module""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/version-control-platform",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/menu.xml",
        "views/vcp_comment.xml",
        "views/vcp_review.xml",
        "views/vcp_request.xml",
        "views/vcp_repository.xml",
        "views/vcp_branch.xml",
        "views/vcp_platform.xml",
    ],
    "demo": [],
}
