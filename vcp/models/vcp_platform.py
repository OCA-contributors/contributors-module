# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class VCPPlatform(models.Model):
    """
    This model should define how to interact with a Version Control Platform
    (VCP) such as GitHub, GitLab, etc.
    1 platform should correspond to 1 organization/account on the VCP.
    """

    _name = "vcp.platform"
    _description = "VCP Platform"

    name = fields.Char(required=True)
    description = fields.Char(readonly=True)
    short_description = fields.Char(readonly=True)
    last_update = fields.Datetime(readonly=True)
    active = fields.Boolean(default=True)
    update_interval_days = fields.Integer(default=3)
    image_1920 = fields.Image()
    branch_ids = fields.One2many(
        "vcp.branch",
        inverse_name="platform_id",
    )
    image_128 = fields.Image(
        max_width=128,
        max_height=128,
        store=True,
        related="image_1920",
        string="Image 128",
    )
    image_64 = fields.Image(
        max_width=64, max_height=64, store=True, related="image_1920", string="Image 64"
    )
    kind = fields.Selection([], required=True)
    key_ids = fields.One2many(
        comodel_name="vcp.platform.key",
        inverse_name="platform_id",
        string="API Keys",
    )
    repository_ids = fields.One2many(
        "vcp.repository",
        inverse_name="platform_id",
    )

    def update_information(self):
        self.ensure_one()
        getattr(self, f"_update_information_{self.kind}")()
        self.last_update = fields.Datetime.now()

    def _cron_update_platforms(self):
        for organization in self.search([]):
            try:
                organization.update_information()
            except Exception as e:
                _logger.error(
                    "Error updating organization %s: %s", organization.name, str(e)
                )

    @tools.ormcache("self.id", "name")
    def _get_branch(self, name):
        self.ensure_one()
        branch = self.env["vcp.branch"].search(
            [("platform_id", "=", self.id), ("name", "=", name)],
            limit=1,
        )
        if not branch:
            branch = (
                self.env["vcp.branch"]
                .sudo()
                .create(
                    {
                        "platform_id": self.id,
                        "name": name,
                    }
                )
            )
        return branch.id

    def _get_merged_domain(self, start, end, **values):
        return [
            ("repository_id.platform_id", "in", self.ids),
            ("is_merged", "=", True),
            ("closed_at", ">=", start),
            ("closed_at", "<", end),
        ]

    def _get_created_domain(self, start, end, **values):
        return [
            ("repository_id.platform_id", "in", self.ids),
            ("created_at", ">=", start),
            ("created_at", "<", end),
        ]

    def _get_comments_domain(self, start, end, **values):
        return [
            ("request_id.repository_id.platform_id", "in", self.ids),
            ("created_at", ">=", start),
            ("created_at", "<", end),
        ]

    def _get_reviews_domain(self, start, end, **values):
        return [
            ("request_id.repository_id.platform_id", "in", self.ids),
            ("submitted_at", ">=", start),
            ("submitted_at", "<", end),
        ]

    def _get_default_data(self, start, end, field, kind, **values):
        return {
            "name": "",
            "github_name": "",
            "created_requests": 0,
            "merged_requests": 0,
            "comments": 0,
            "reviews": 0,
            "developers": 0,
        }

    def _generate_data(self, start, end, field, kind, extra_domain=None, **values):
        if extra_domain is None:
            extra_domain = []
        default_dict = self._get_default_data(start, end, field, kind, **values)
        data = defaultdict(lambda: default_dict.copy())
        if not field:
            return data
        for merged in (
            self.env["vcp.request"]
            .sudo()
            .read_group(
                self._get_merged_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[merged[field][0]]["merged_requests"] = merged[f"{field}_count"]
        for pr in (
            self.env["vcp.request"]
            .sudo()
            .read_group(
                self._get_created_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field, "partner_id:count_distinct"]
                if field != "partner_id"
                else [field],
                [field],
            )
        ):
            data[pr[field][0]]["created_requests"] = pr[f"{field}_count"]
            if field != "partner_id":
                data[pr[field][0]]["developers"] = pr["partner_id"]
        for comment in (
            self.env["vcp.comment"]
            .sudo()
            .read_group(
                self._get_comments_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[comment[field][0]]["comments"] = comment[f"{field}_count"]
        for review in (
            self.env["vcp.review"]
            .sudo()
            .read_group(
                self._get_reviews_domain(start, end, **values)
                + extra_domain
                + [(field, "!=", False)],
                [field],
                [field],
            )
        ):
            data[review[field][0]]["reviews"] = review[f"{field}_count"]
        return data

    def _get_dates(self, year, month, period, **values):
        if month == 12:
            end = datetime(year + 1, 1, 1, 0, 0, 0)
        else:
            end = datetime(year, month + 1, 1, 0, 0, 0)
        if period == "YTD":
            start = datetime(year, 1, 1, 0, 0, 0)
        elif period == "MAT":
            start = end - relativedelta(years=1)
        else:
            start = datetime(year, month, 1, 0, 0, 0)
        return start, end


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

    _sql_constraints = [
        ("name_uniq", "unique(name, platform_id)", "API Key must be unique.")
    ]
