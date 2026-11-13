import random
import re

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

    def click_add_rule(self):
        add_rule = self.page.locator(
            ClaimEligibilityLocators.ADD_RULE_BUTTON
        ).last

        expect(add_rule).to_be_visible(timeout=10000)

        add_rule.click()

        self.page.wait_for_timeout(1000)

        return True

    def verify_role_designation_dropdown(self):
        role_dropdown = self.page.get_by_role(
            "combobox"
        ).nth(0)

        expect(role_dropdown).to_be_visible(timeout=10000)
        expect(role_dropdown).to_be_enabled(timeout=10000)

        role_dropdown.click()

        self.page.wait_for_timeout(500)

        options = self.page.get_by_role("option")

        expect(options.first).to_be_visible(timeout=10000)

        # Get all available Role / Designation options
        option_count = options.count()

        assert option_count > 0, (
            "No Role / Designation options are available"
        )

        # Select a random Role / Designation
        random_index = random.randrange(option_count)

        selected_option = options.nth(random_index)

        expect(selected_option).to_be_visible(timeout=10000)

        selected_role = selected_option.inner_text()

        selected_option.click()

        print(
            f"Selected random Role / Designation: {selected_role}"
        )

        return True

    def select_claim_type(self):
        claim_type_dropdown = self.page.get_by_role(
            "combobox"
        ).nth(1)

        expect(claim_type_dropdown).to_be_visible(timeout=10000)
        expect(claim_type_dropdown).to_be_enabled(timeout=10000)

        claim_type_dropdown.click()

        self.page.wait_for_timeout(500)

        options = self.page.get_by_role("option")

        expect(options.first).to_be_visible(timeout=10000)

        options.first.click()

        return True

    def enter_minimum_visits(self):
        field = self.page.get_by_label(
            "Min visits per day",
            exact=True
        )

        expect(field).to_be_visible(timeout=10000)
        expect(field).to_be_enabled(timeout=10000)

        field.fill("3")

        expect(field).to_have_value("3")

        return True

    def enter_submission_deadline(self):
        field = self.page.get_by_label(
            "Day of next month (deadline)",
            exact=True
        )

        expect(field).to_be_visible(timeout=10000)
        expect(field).to_be_enabled(timeout=10000)

        field.fill("3")

        expect(field).to_have_value("3")

        return True

    def select_status(self):
        status_dropdown = self.page.get_by_role(
            "combobox"
        ).nth(2)

        expect(status_dropdown).to_be_visible(timeout=10000)
        expect(status_dropdown).to_be_enabled(timeout=10000)

        status_dropdown.click()

        self.page.wait_for_timeout(500)

        options = self.page.get_by_role("option")

        expect(options.first).to_be_visible(timeout=10000)

        options.first.click()

        return True

    def save_claim_rule(self):
        save_button = self.page.get_by_role(
            "button",
            name="Save",
            exact=True
        )

        expect(save_button).to_be_visible(timeout=10000)
        expect(save_button).to_be_enabled(timeout=10000)

        save_button.click()

        self.page.wait_for_timeout(1500)

        return True

    def verify_claim_rule_saved(self):
        modal = self.page.locator(
            ClaimEligibilityLocators.ADD_CLAIM_RULE_MODAL
        )

        expect(modal).to_be_hidden(timeout=10000)

        return True

    def verify_role_designation_configuration(self):

        # Open Claim Eligibility
        self.verify_claim_eligibility_card()

        # Open Add Rule form
        self.click_add_rule()

        # Verify and randomly select Role / Designation
        self.verify_role_designation_dropdown()

        # Select Claim Type
        self.select_claim_type()

        # Enter Minimum Visits Per Day = 3
        self.enter_minimum_visits()

        # Enter valid deadline between 1 and 5
        self.enter_submission_deadline()

        # Select Status
        self.select_status()

        # Save
        self.save_claim_rule()

        # Verify save
        self.verify_claim_rule_saved()

        return True

    def click_add_rule_for_existing_role(self):
        # Find the existing role card
        role_card = self.page.locator(
            ClaimEligibilityLocators.EXISTING_ROLE_CARD
        ).filter(
            has=self.page.get_by_text(
                re.compile(r"^\d+ rules?$")
            )
        ).first

        expect(
            role_card
        ).to_be_visible(timeout=10000)

        # Click Add Rule inside the existing role card
        add_rule_button = role_card.get_by_role(
            "button",
            name="Add Rule",
            exact=True
        )

        expect(
            add_rule_button
        ).to_be_visible(timeout=10000)

        expect(
            add_rule_button
        ).to_be_enabled(timeout=10000)

        add_rule_button.click()

        # Verify dialog opened
        dialog = self.page.get_by_role(
            "dialog"
        )

        expect(
            dialog
        ).to_be_visible(timeout=10000)

        return True

    def verify_existing_role_is_locked(self):
        dialog = self.page.get_by_role("dialog")

        # Role / Designation field
        role_input = dialog.locator(
            "input"
        ).first

        expect(
            role_input
        ).to_be_visible(timeout=10000)

        # Verify the field is disabled / locked
        expect(
            role_input
        ).to_be_disabled(timeout=10000)

        # Verify an existing role is populated
        role_value = role_input.get_attribute("value")

        assert role_value, (
            "Existing Role/Designation is not populated."
        )

        print(
            f"Existing Role/Designation: {role_value}"
        )

        return True

    def select_claim_type_for_existing_role(self):
        dialog = self.page.get_by_role(
            "dialog"
        )

        claim_type = dialog.get_by_role(
            "combobox"
        ).nth(1)

        expect(
            claim_type
        ).to_be_visible(timeout=10000)

        expect(
            claim_type
        ).to_be_enabled(timeout=10000)

        claim_type.click()

        options = self.page.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=10000)

        options.first.click()

        return True

    def enter_minimum_visits_for_existing_role(self):
        dialog = self.page.get_by_role("dialog")

        field = dialog.get_by_label(
            "Min visits per day",
            exact=True
        )

        expect(
            field
        ).to_be_visible(timeout=10000)

        expect(
            field
        ).to_be_enabled(timeout=10000)

        field.fill("3")

        expect(
            field
        ).to_have_value("3")

        return True

    def enter_deadline_for_existing_role(self):
        dialog = self.page.get_by_role("dialog")

        field = dialog.get_by_label(
            "Day of next month (deadline)",
            exact=True
        )

        expect(
            field
        ).to_be_visible(timeout=10000)

        expect(
            field
        ).to_be_enabled(timeout=10000)

        field.fill("3")

        expect(
            field
        ).to_have_value("3")

        return True

    def select_status_for_existing_role(self):
        dialog = self.page.get_by_role(
            "dialog"
        )

        status = dialog.get_by_role(
            "combobox"
        ).nth(2)

        expect(
            status
        ).to_be_visible(timeout=10000)

        expect(
            status
        ).to_be_enabled(timeout=10000)

        status.click()

        options = self.page.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=10000)

        options.first.click()

        return True

    def save_existing_role_claim_rule(self):
        dialog = self.page.get_by_role(
            "dialog"
        )

        save_button = dialog.get_by_role(
            "button",
            name="Save",
            exact=True
        )

        expect(
            save_button
        ).to_be_visible(timeout=10000)

        expect(
            save_button
        ).to_be_enabled(timeout=10000)

        save_button.click()

        self.page.wait_for_timeout(1500)

        return True

    def add_claim_rule_for_existing_role(self):
        # Existing role → Add Rule
        self.click_add_rule_for_existing_role()

        # Verify existing role is populated and locked
        self.verify_existing_role_is_locked()

        # Select Claim Type first
        self.select_claim_type_for_existing_role()

        # Automatically fill values after Claim Type
        self.enter_minimum_visits_for_existing_role()
        self.enter_deadline_for_existing_role()

        # Select Status
        self.select_status_for_existing_role()

        # Save
        self.save_existing_role_claim_rule()

        return True
