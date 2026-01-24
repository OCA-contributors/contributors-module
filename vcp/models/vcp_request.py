# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpRequest(models.Model):
    _name = "vcp.request"
    _description = "Code Request"

    external_id = fields.Char(string="Externa ID", readonly=True, index=True)
    name = fields.Char(readonly=True)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contributor",
        readonly=True,
    )
    repository_id = fields.Many2one(
        comodel_name="vcp.repository",
        readonly=True,
        ondelete="cascade",
    )
    branch_id = fields.Many2one(
        comodel_name="vcp.branch",
        readonly=True,
        ondelete="restrict",
    )
    organization_id = fields.Many2one(
        comodel_name="res.partner",
        readonly=True,
    )
    url = fields.Char(readonly=True)
    state = fields.Char(readonly=True)
    is_merged = fields.Boolean(readonly=True)
    created_at = fields.Datetime(readonly=True)
    updated_at = fields.Datetime(readonly=True)
    closed_at = fields.Datetime(readonly=True)
    number = fields.Integer(readonly=True)
    label_ids = fields.Many2many(
        comodel_name="vcp.request.label",
        string="Labels",
        readonly=True,
    )
    commits = fields.Integer(readonly=True)
    additions = fields.Integer(readonly=True)
    deletions = fields.Integer(readonly=True)
    total_comments = fields.Integer(readonly=True)
    review_comments = fields.Integer(readonly=True)

    _sql_constraints = [
        ("external_id_uniq", "unique(external_id)", "External ID must be unique.")
    ]


class VcpRequestLabel(models.Model):
    _name = "vcp.request.label"
    _description = "Vcp Request Label"

    name = fields.Char(required=True)

    _sql_constraints = [("name_uniq", "unique(name)", "Label name must be unique.")]

    @tools.ormcache("name")
    def _get_label(self, name):
        label = self.search([("name", "=", name)], limit=1)
        if not label:
            label = self.sudo().create({"name": name})
        return label.id
