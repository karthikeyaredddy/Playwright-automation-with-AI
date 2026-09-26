import random
import re
from playwright.sync_api import expect
from locators.partnerverification_locators import PartnerVerificationLocators


class PartnerVerificationPage:

    def __init__(self, page):
        self.page = page

    # ==========================================================
    # Common Helper Methods
    # ==========================================================

    def _click_and_verify_tab(self, locator):
        tab = self.page.locator(locator)
        expect(tab).to_be_visible(timeout=10000)
        tab.click()
        expect(tab).to_be_visible()
        return True

    def _wait_for_cards(self):
        cards = self.page.locator(
            PartnerVerificationLocators.PARTNER_CARD
        )
        expect(cards.first).to_be_visible(timeout=30000)
        return cards

    def _select_first_dropdown_option(self, index):

        dropdown = self.page.locator(
            PartnerVerificationLocators.COMBOBOX
        ).nth(index)

        expect(dropdown).to_be_visible(timeout=10000)

        dropdown.click()

        options = self.page.locator(
            PartnerVerificationLocators.DROPDOWN_OPTIONS
        )

        expect(options.first).to_be_visible(timeout=10000)

        options.first.click()
        print("Combobox Count :", self.page.locator("[role='combobox']").count())

        return True

    def open_basic_details(self):
        self.page.locator(
            PartnerVerificationLocators.BASIC_DETAILS
        ).click()

        expect(
            self.page.locator(
                PartnerVerificationLocators.BASIC_DETAILS
            )
        ).to_be_visible()

        return True

    # ==========================================================
    # Module Verification
    # ==========================================================

    def verify_partner_verification_module(self):

        heading = self.page.locator(
            PartnerVerificationLocators.PARTNER_VERIFICATION_HEADING
        )

        expect(heading).to_have_text(
            "Partner Verification",
            timeout=15000
        )

        description = self.page.locator(
            PartnerVerificationLocators.PARTNER_VERIFICATION_DESCRIPTION
        )

        expect(description).to_be_visible(timeout=10000)

        elements = [

            PartnerVerificationLocators.SEARCH_BOX,

            PartnerVerificationLocators.BASIC_DETAILS,

            PartnerVerificationLocators.BUSINESS_GST,

            PartnerVerificationLocators.DOCUMENTS,

            PartnerVerificationLocators.INVALID_PARTNERS

        ]

        for locator in elements:
            expect(
                self.page.locator(locator)
            ).to_be_visible(timeout=10000)

        return True
    # ==========================================================
    # Tabs
    # ==========================================================

    def verify_basic_details_tab(self):
        return self._click_and_verify_tab(
            PartnerVerificationLocators.BASIC_DETAILS
        )

    def verify_business_gst_tab(self):
        return self._click_and_verify_tab(
            PartnerVerificationLocators.BUSINESS_GST
        )

    def verify_documents_tab(self):
        return self._click_and_verify_tab(
            PartnerVerificationLocators.DOCUMENTS
        )

    def verify_invalid_partners_tab(self):
        return self._click_and_verify_tab(
            PartnerVerificationLocators.INVALID_PARTNERS
        )

    # ==========================================================
    # Pending Count
    # ==========================================================

    def verify_pending_count(self):

        pending = self.page.locator(
            PartnerVerificationLocators.PENDING_CHIP
        )

        expect(pending).to_be_visible(timeout=10000)

        text = pending.text_content().strip()

        print("Pending :", text)

        match = re.search(r"\d+", text)

        assert match is not None, "Pending count not found"

        return True

    # ==========================================================
    # Verified Today
    # ==========================================================

    def verify_verified_today_count(self):

        verified = self.page.locator(
            PartnerVerificationLocators.VERIFIED_TODAY_CHIP
        )

        expect(verified).to_be_visible(timeout=10000)

        text = verified.text_content().strip()

        print("Verified Today :", text)

        match = re.search(r"\d+", text)

        assert match is not None, "Verified Today count not found"

        return True

    # ==========================================================
    # Search
    # ==========================================================

    def verify_search_working(self):

        self.open_basic_details()

        search = self.page.locator(
            PartnerVerificationLocators.SEARCH_BOX
        )

        expect(search).to_be_visible(timeout=10000)

        search.fill("9838472195")

        expect(search).to_have_value("9838472195")

        search.clear()

        expect(search).to_have_value("")

        return True

    # ==========================================================
    # State Filter
    # ==========================================================

    def verify_state_filter(self):

        clear = self.page.get_by_role("button", name="Clear Filters")

        if clear.count() > 0 and clear.first.is_visible():
            clear.first.click()

        self.open_basic_details()

        close_btn = self.page.get_by_role(
            "button",
            name="Close basic verification modal"
        )

        if close_btn.count() > 0:

            if close_btn.first.is_visible():

                close_btn.first.click()

        state = self.page.get_by_role("combobox", name="State")

        expect(state).to_be_visible(timeout=10000)

        state.click()

        options = self.page.locator(
            PartnerVerificationLocators.DROPDOWN_OPTIONS
        )

        expect(options.first).to_be_visible(timeout=10000)

        options.first.click()

        return True

    # ==========================================================
    # Information Message
    # ==========================================================

    def verify_bulk_action_message(self):

        tab_messages = [

            (
                PartnerVerificationLocators.BASIC_DETAILS,
                "Select one or more partners"
            ),

            (
                PartnerVerificationLocators.BUSINESS_GST,
                "If the GST name mismatch"
            ),

            (
                PartnerVerificationLocators.DOCUMENTS,
                "Click a thumbnail"
            ),

            (
                PartnerVerificationLocators.INVALID_PARTNERS,
                "Select one or more partners"
            )

        ]

        message = self.page.locator(
            PartnerVerificationLocators.INFO_MESSAGE
        )

        for tab, expected in tab_messages:

            self.page.locator(tab).click()

            expect(message).to_be_visible(timeout=10000)

            expect(message).to_contain_text(expected)

        return True
    # ==========================================================
    # Business + GST Filters
    # ==========================================================

    def verify_business_gst_filters(self):

        self.page.locator(
            PartnerVerificationLocators.BUSINESS_GST
        ).click()

        search = self.page.locator(
            PartnerVerificationLocators.SEARCH_BOX
        )

        expect(search).to_be_visible(timeout=10000)

        search.fill("9838472195")
        expect(search).to_have_value("9838472195")
        search.clear()

        # State
        state = self.page.get_by_role("combobox", name="State")
        expect(state).to_be_visible(timeout=10000)
        state.click()

        options = self.page.locator(
            PartnerVerificationLocators.DROPDOWN_OPTIONS
        )
        expect(options.first).to_be_visible(timeout=10000)
        options.first.click()

        # GST Status (only if available)
        dropdowns = self.page.locator(
            PartnerVerificationLocators.COMBOBOX
        )

        if dropdowns.count() > 2:
            self._select_first_dropdown_option(2)

        # Name Match (only if available)
        try:
            name_match = self.page.get_by_role(
                "combobox",
                name="Name match"
            )

            if name_match.is_visible():
                name_match.click()

                options = self.page.locator(
                    PartnerVerificationLocators.DROPDOWN_OPTIONS
                )

                expect(options.first).to_be_visible(timeout=5000)
                options.first.click()

        except Exception:
            print("Name Match filter not available.")

        return True

    # ==========================================================
    # Documents Filters
    # ==========================================================

    def verify_documents_filters(self):

        self.page.locator(
            PartnerVerificationLocators.DOCUMENTS
        ).click()

        expect(
            self.page.locator(
                PartnerVerificationLocators.SEARCH_BOX
            )
        ).to_be_visible(timeout=10000)

        state = self.page.get_by_role(
            "combobox",
            name="State"
        )

        expect(state).to_be_visible(timeout=10000)

        return True
    # ==========================================================
    # Invalid Partners Filters
    # ==========================================================

    def verify_invalid_partners_filters(self):

        self.page.locator(
            PartnerVerificationLocators.INVALID_PARTNERS
        ).click()

        search = self.page.locator(
            PartnerVerificationLocators.SEARCH_BOX
        )

        expect(search).to_be_visible(timeout=10000)

        search.fill("md1")

        expect(search).to_have_value("md1")

        search.clear()

        expect(search).to_have_value("")

        # State
        state = self.page.get_by_role("combobox", name="State")
        expect(state).to_be_visible(timeout=10000)
        state.click()

        options = self.page.locator(
            PartnerVerificationLocators.DROPDOWN_OPTIONS
        )
        expect(options.first).to_be_visible(timeout=10000)
        options.first.click()

        return True

    # ==========================================================
    # Invalid Partners Actions
    # ==========================================================

    def verify_invalid_partners_actions(self):

        # Click Invalid Partners tab
        invalid_tab = self.page.locator(
            PartnerVerificationLocators.INVALID_PARTNERS
        )

        expect(invalid_tab).to_be_visible(
            timeout=10000
        )

        invalid_tab.click()

        # Click All
        all_button = self.page.get_by_role(
            "button",
            name="All",
            exact=True
        )

        expect(all_button).to_be_visible(
            timeout=10000
        )

        all_button.click()

        # Verify Select All button
        select_all = self.page.get_by_role(
            "button",
            name="Select All",
            exact=True
        )

        expect(select_all).to_be_visible(
            timeout=10000
        )

        print(
            "Select All Enabled:",
            select_all.is_enabled()
        )

        # Verify Deactivate Selected button
        deactivate_selected = self.page.get_by_role(
            "button",
            name="Deactivate Selected",
            exact=True
        )

        expect(deactivate_selected).to_be_visible(
            timeout=10000
        )

        print(
            "Deactivate Selected Enabled:",
            deactivate_selected.is_enabled()
        )

        # Verify Deactivate All button
        deactivate_all = self.page.get_by_role(
            "button",
            name="Deactivate All",
            exact=True
        )

        expect(deactivate_all).to_be_visible(
            timeout=10000
        )

        print(
            "Deactivate All Enabled:",
            deactivate_all.is_enabled()
        )

        # Do not click destructive buttons
        return True
