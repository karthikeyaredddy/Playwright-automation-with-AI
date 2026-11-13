import pytest
from pages.partnerusermanagement_page import partnerusermanagementPage


@pytest.mark.order(6)
class TestPartnerUserManagement:

    def test_partner_user_management(self, logged_in_page):
        partner = partnerusermanagementPage(logged_in_page)

        partner.verify_partner_user_management()
