from playwright.sync_api import expect

from locators.partnerusermanagement_locators import partnerusermanagement_locators


class partnerusermanagementPage:

    def __init__(self, page):
        self.page = page

    # Partner User Management

    def verify_partner_user_management(self):

        # Wait for Partner User Management menu
        partner_user = self.page.get_by_role(
            "button",
            name="Partner User Management"
        )

        expect(partner_user).to_be_visible(timeout=10000)

        # Click Partner User Management
        partner_user.click()

        # Verify navigation
        self.page.wait_for_url(
            "**/partner-user-management**",
            timeout=15000
        )

        assert "partner-user-management" in self.page.url

        return True