# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class VcpPlatformKey(models.Model):
    _name = "vcp.platform.key"
    _description = "VCP Platform API Key"  # TODO

    platform_id = fields.Many2one(
        comodel_name="vcp.platform",
        string="Platform",
        required=True,
        ondelete="cascade",
    )
    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "unique(name, platform_id)", "API Key must be unique."
    )
