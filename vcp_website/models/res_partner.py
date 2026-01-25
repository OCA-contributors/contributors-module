# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_contributor_url(self):
        if self.is_published and self.website_url:
            return self.website_url
        return super()._get_contributor_url()
