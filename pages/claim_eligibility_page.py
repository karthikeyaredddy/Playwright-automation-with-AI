from playwright.sync_api import expect
from locators.claim_eligibility_locators import ClaimEligibilityLocators


class ClaimEligibilityPage:

    def __init__(self, page):
        self.page = page

    def open_account_settings(self):

        self.page.locator(
            ClaimEligibilityLocators.ADMIN_BUTTON
        ).click()

        self.page.locator(
            ClaimEligibilityLocators.ACCOUNT_SETTINGS
        ).click()

        self.page.wait_for_load_state("networkidle")

    def verify_claim_eligibility_card(self):

        self.open_account_settings()

        financial = self.page.locator(
            ClaimEligibilityLocators.FINANCIAL_CONFIGURATION
        )

        financial.scroll_into_view_if_needed()

        expect(financial).to_be_visible(timeout=10000)

        card = self.page.locator(
            ClaimEligibilityLocators.CLAIM_ELIGIBILITY_CARD
        )

        expect(card).to_be_visible(timeout=10000)

        card.click()

        self.page.wait_for_timeout(2000)

        return True