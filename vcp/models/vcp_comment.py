# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpComment(models.Model):
    _name = "vcp.comment"
    _description = "Comment"

    external_id = fields.Char(readonly=True, required=True, index=True)
    body = fields.Html(readonly=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        readonly=True,
    )
    organization_id = fields.Many2one(
        related="request_id.organization_id",
        readonly=True,
        store=True,
    )
    repository_id = fields.Many2one(
        related="request_id.repository_id",
        readonly=True,
        store=True,
    )
    created_at = fields.Datetime(readonly=True)
    updated_at = fields.Datetime(readonly=True)
    request_id = fields.Many2one(
        comodel_name="vcp.request",
        string="Request",
        readonly=True,
    )
    _sql_constraints = [
        ("external_id_uniq", "unique(external_id)", "External ID must be unique.")
    ]
