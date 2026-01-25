# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo_test_helper import FakeModelLoader

from odoo.fields import Date
from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo, HttpCaseWithUserPortal


@tagged("post_install", "-at_install")
class TestBase(HttpCaseWithUserDemo, HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake order model
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models.vcp_platform import VCPPlatform

        cls.loader.update_registry((VCPPlatform,))

        # be sure some expected values are set otherwise homepage may fail
        date = Date.today()
        date = date - timedelta(days=date.day)
        cls.partner_portal.write(
            {
                "city": "Bayonne",
                "company_name": "YourCompany",
                "country_id": cls.env.ref("base.us").id,
                "phone": "(683)-556-5104",
                "street": "858 Lynn Street",
                "zip": "07002",
            }
        )
        platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "short_description": "OCA",
                "description": "OCA",
                "kind": "dummy",
            }
        )
        repository = cls.env["vcp.repository"].create(
            {
                "name": "contributors-module",
                "description": "OCA/contributors-module",
                "platform_id": platform.id,
                "from_date": date,
            }
        )
        user_01 = cls.env["res.partner"].create(
            {
                "name": "Enric Tobella",
            }
        )
        user_02 = cls.env["res.partner"].create(
            {
                "name": "Luis Rodriguez",
            }
        )
        user_03 = cls.env["res.partner"].create(
            {
                "name": "Jordi Ballester",
            }
        )
        org_01 = cls.env["res.partner"].create(
            {
                "name": "Dixmit",
            }
        )
        org_02 = cls.env["res.partner"].create(
            {
                "name": "ForgeFlow",
            }
        )
        pull_request_01 = cls.env["vcp.request"].create(
            {
                "external_id": 1,
                "name": "Test PR",
                "repository_id": repository.id,
                "partner_id": user_01.id,
                "organization_id": org_01.id,
                "created_at": date,
                "closed_at": date,
                "is_merged": True,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 2,
                "name": "Test PR",
                "repository_id": repository.id,
                "partner_id": user_02.id,
                "organization_id": org_01.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 3,
                "name": "Test PR",
                "repository_id": repository.id,
                "partner_id": user_03.id,
                "organization_id": org_02.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.review"].create(
            {
                "external_id": 1,
                "body": "Test Review",
                "state": "APPROVED",
                "request_id": pull_request_01.id,
                "partner_id": user_01.id,
                "submitted_at": date,
            }
        )
        cls.env["vcp.comment"].create(
            {
                "external_id": 1,
                "body": "Test Comment",
                "request_id": pull_request_01.id,
                "partner_id": user_01.id,
                "created_at": date,
            }
        )
