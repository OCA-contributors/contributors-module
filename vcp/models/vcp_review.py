# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VcpReview(models.Model):
    _name = "vcp.review"
    _description = "Review"  # TODO

    external_id = fields.Char(readonly=True, required=True, index=True)
    body = fields.Html(readonly=True)
    state = fields.Char(readonly=True)
    partner_id = fields.Many2one("res.partner", readonly=True)
    submitted_at = fields.Datetime(readonly=True)
    repository_id = fields.Many2one(
        related="request_id.repository_id",
        readonly=True,
        store=True,
    )
    request_id = fields.Many2one(
        "vcp.request",
        readonly=True,
    )
    organization_id = fields.Many2one(
        related="request_id.organization_id",
        readonly=True,
        store=True,
    )
    platform_id = fields.Many2one(
        related="request_id.repository_id.platform_id",
        readonly=True,
        store=True,
    )

    _sql_constraints = [
        ("external_id_uniq", "unique(external_id)", "External ID must be unique.")
    ]
