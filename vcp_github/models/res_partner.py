# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import github3

from odoo import fields, models, tools


class ResPartner(models.Model):
    _inherit = "res.partner"

    github_name = fields.Char(
        string="GitHub Username",
        help="GitHub username of the contributor or organization",
        readonly=True,
    )
    github_organization = fields.Boolean(
        string="Is GitHub Organization",
        help="Check if this partner represents a GitHub organization",
        readonly=True,
    )
    github_user = fields.Boolean(
        string="Is GitHub User",
        help="Check if this partner represents a GitHub user",
        readonly=True,
    )

    _sql_constraints = [
        (
            "github_name_uniq",
            "unique(github_name)",
            "The GitHub username must be unique across partners.",
        ),
    ]

    @tools.ormcache("github_login")
    def _get_github_user_id(self, github_login):
        partner = self.with_context(active_test=False).search(
            [("github_name", "=ilike", github_login)], limit=1
        )
        if not partner:
            return False
        if not partner.github_user:
            partner.github_user = True
        return partner.id

    @tools.ormcache("github_login")
    def _get_github_organization_id(self, github_login):
        partner = self.with_context(active_test=False).search(
            [("github_name", "=ilike", github_login)], limit=1
        )
        if not partner:
            return False
        if not partner.github_organization:
            partner.github_organization = True
        return partner.id

    def _get_github_user(self, gh, client):
        if not gh:
            return False
        if isinstance(gh, github3.users.User):
            github_login = gh.login
        else:
            github_login = str(gh)
        partner = self._get_github_user_id(github_login)
        if partner:
            return partner
        if isinstance(gh, str):
            try:
                gh = client.user(github_login)
                name = gh.name or github_login
            except github3.exceptions.NotFoundError:
                name = gh
        else:
            if hasattr(gh, "name"):
                name = gh.name or github_login
            else:
                name = github_login
        self.env.registry.clear_cache()
        return self.create(
            {
                "name": name,
                "github_name": github_login,
                "github_user": True,
            }
        ).id

    def _get_github_organization(self, gh, client):
        if not gh:
            return False
        partner = self._get_github_organization_id(str(gh))
        if partner:
            return partner
        self.env.registry.clear_cache()
        try:
            org = client.organization(str(gh))

            return self.create(
                {
                    "name": org.name or str(gh),
                    "github_name": str(gh),
                    "github_organization": True,
                }
            ).id
        except github3.exceptions.NotFoundError:
            user = client.user(str(gh))
            name = user.name or str(gh)
        except github3.exceptions.ForbiddenError:
            name = str(gh)
        return self.create(
            {
                "name": name,
                "github_name": str(gh),
                "github_user": True,
                "github_organization": True,
            }
        ).id

    def _get_contributor_url(self):
        result = super()._get_contributor_url()
        if not result and self.github_name:
            return f"https://github.com/{self.github_name}"
        return result
