# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from math import sqrt

from odoo import _, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class ContributorsController(CustomerPortal):
    @http.route(
        [
            "/vcp",
            "/vcp/<string:vcp>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def contributors_vcp(self, vcp=None):
        values = self._prepare_portal_layout_values()
        values.update(self._prepare_home_portal_values([]))
        if vcp is None:
            vcps = request.env["vcp.platform"].search([])
            return request.render(
                "vcp_portal.vcp_platforms_template",
                {"vcps": vcps, **values},
            )
        vcp_id = (
            request.env["vcp.platform"]
            .sudo()
            .search([("name", "=ilike", vcp)], limit=1)
            .id
        )
        return request.render(
            "vcp_portal.vcp_platform_template",
            {"vcp": vcp_id, **values},
        )

    def _get_index(self, data):
        return round(
            sqrt(data["created_requests"])
            + data["merged_requests"]
            + sqrt(data["comments"])
            + data["reviews"],
            2,
        )

    def _get_field(self, kind):
        if kind == "contributors":
            return "partner_id"
        elif kind == "organizations":
            return "organization_id"
        elif kind == "repositories":
            return "repository_id"
        return False

    @http.route(["/vcp-fetch"], type="json", auth="user", readonly=True)
    def fetch_vcp_data(self, vcp_id, year, month, kind, period, **values):
        vcp = request.env["vcp.platform"].browse(vcp_id).exists()
        if not vcp:
            return []
        start, end = vcp._get_dates(year, month, period, **values)
        data = vcp._generate_data(start, end, self._get_field(kind), kind, **values)
        return {
            "columns": self._get_vcp_columns(kind),
            "data": self._improve_vcp_data(data, kind, **values),
        }

    def _get_vcp_columns(self, kind):
        if kind == "contributors":
            return [
                {"field": "name", "title": _("Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        elif kind == "organizations":
            return [
                {"field": "name", "title": _("Organization Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "developers",
                    "title": _("Developers"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        elif kind == "repositories":
            return [
                {"field": "name", "title": _("Repository Name"), "kind": "name"},
                {
                    "field": "created_requests",
                    "title": _("Created Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "merged_requests",
                    "title": _("Merged Requests"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "comments",
                    "title": _("Comments"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "reviews",
                    "title": _("Reviews"),
                    "kind": "float",
                    "decimals": 0,
                },
                {
                    "field": "developers",
                    "title": _("Developers"),
                    "kind": "float",
                    "decimals": 0,
                },
            ]
        return []

    def _improve_vcp_data(self, data, kind, **kwargs):
        for key, values in data.items():
            if kind == "contributors":
                partner = request.env["res.partner"].browse(key)
                values["name"] = partner._get_contributors_name(kind, **kwargs)
                values["url"] = partner._get_contributor_url()
            elif kind == "organizations":
                organization = request.env["res.partner"].browse(key)
                values["name"] = organization._get_contributors_name(kind, **kwargs)
                values["url"] = organization._get_contributor_url()
            elif kind == "repositories":
                repository = request.env["vcp.repository"].browse(key)
                values["name"] = repository.name
                values["url"] = repository._get_repository_url()
        return data
