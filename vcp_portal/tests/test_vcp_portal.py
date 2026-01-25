# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import tagged

from odoo.addons.vcp.tests.test_base import TestBase


@tagged("post_install", "-at_install")
class TestVCPPortal(TestBase):
    def test_01_portal_load_tour(self):
        self.start_tour("/", "portal_load_contributors_github", login="portal")
