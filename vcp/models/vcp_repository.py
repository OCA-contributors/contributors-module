# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class VcpRepository(models.Model):
    _name = "vcp.repository"
    _description = "Repository"

    name = fields.Char(required=True, index=True)
    description = fields.Char(readonly=True)
    platform_id = fields.Many2one(
        comodel_name="vcp.platform",
        required=True,
    )
    created_at = fields.Datetime(readonly=True)
    stargazers_count = fields.Integer(readonly=True)
    fork_count = fields.Integer(readonly=True)
    watchers_count = fields.Integer(readonly=True)
    from_date = fields.Datetime(readonly=True, required=True)
    request_ids = fields.One2many("vcp.request", inverse_name="repository_id")
    request_count = fields.Integer(compute="_compute_request_count")
    active = fields.Boolean(default=True)

    @api.depends("request_ids")
    def _compute_request_count(self):
        for record in self:
            record.request_count = len(record.request_ids)

    def force_update_information(self):
        self.update_information(update_interval_days=365)

    def update_information(self, update_interval_days=None):
        self.ensure_one()
        getattr(self, f"_update_information_{self.platform_id.kind}")(
            update_interval_days=update_interval_days
        )

    def _cron_update_repositories(self, limit=1):
        repositories = self.search([], limit=limit, order="from_date ASC")
        for repository in repositories:
            repository.update_information()

    def _get_repository_url(self):
        self.ensure_one()
        return False
