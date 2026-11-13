import random
import re

from playwright.sync_api import Page, expect

from locators.Leavemanagement_locators import LeaveManagementLocators


class LeaveManagementPage:
    """Page object for EMS > Leave Management navigation."""

    def __init__(self, page: Page):
        self.page = page


    def _dismiss_open_dialog(self):
        """Close a leftover dialog from a previous test, if one is open."""
        dialog = self.page.get_by_role("dialog").last
        if dialog.count() and dialog.is_visible():
            cancel = dialog.get_by_role("button", name=LeaveManagementLocators.CANCEL_BUTTON, exact=True)
            if cancel.count() and cancel.is_visible():
                cancel.click()
                expect(dialog).not_to_be_visible()

    def navigate_to_leave_management(self):
        """Return to the Leave Management overview reliably between tests."""
        self._dismiss_open_dialog()
        overview_heading = self.page.get_by_role(
            "heading", name=LeaveManagementLocators.PAGE_HEADING, exact=True
        )

        if re.search(r"/dashboard/leave(?:/policies)?/?$", self.page.url):
            if overview_heading.is_visible():
                return

        nav = self.page.get_by_label("mailbox folders")
        leave_menu = nav.get_by_role(
            "button", name=LeaveManagementLocators.LEAVE_MANAGEMENT_MENU, exact=True
        )

        back_to_overview = self.page.get_by_role(
            "button", name="Back to leave management overview", exact=True
        )
        if back_to_overview.is_visible():
            back_to_overview.click()
        else:
            expect(leave_menu).to_be_visible()
            leave_menu.click()

        expect(self.page).to_have_url(re.compile(r".*/dashboard/leave/?$"))
        expect(overview_heading).to_be_visible()

    def verify_leave_management_page(self):
        """Verify the Leave Management overview is visible."""
        expect(self.page).to_have_url(re.compile(r".*/dashboard/leave/?$"))
        expect(self.page.get_by_role(
            "heading", name=LeaveManagementLocators.PAGE_HEADING, exact=True
        )).to_be_visible()

    def click_leave_types(self):
        """Open Leave Types whether currently on overview or another section."""
        self._dismiss_open_dialog()
        types_heading = self.page.get_by_role(
            "heading", name=LeaveManagementLocators.LEAVE_TYPES_HEADING, exact=True
        )
        if types_heading.is_visible():
            return

        self.navigate_to_leave_management()
        self.page.get_by_role(
            "button", name=LeaveManagementLocators.LEAVE_TYPES_BUTTON, exact=True
        ).click()
        expect(types_heading).to_be_visible()
        expect(self.page.get_by_text(
            "Manage leave categories, eligibility, and leave policy structure.", exact=True
        )).to_be_visible()
        expect(self.page.get_by_role(
            "button", name=LeaveManagementLocators.ADD_LEAVE_TYPE_BUTTON, exact=True
        )).to_be_visible()

    def _urgent_leave_row(self):
        """Return the first matching Urgent Leave row (older test runs may leave duplicates)."""
        rows = self.page.get_by_role("row").filter(
            has=self.page.get_by_role(
                "cell", name=LeaveManagementLocators.CREATED_LEAVE_TYPE_NAME, exact=True
            )
        )
        expect(rows.first).to_be_visible()
        return rows.first

    def create_leave_type(self):
        """Create a leave type and verify same-day application toggle."""

        # Open Leave Types section
        self.navigate_to_leave_management()
        self.click_leave_types()

        # Click Add Leave Type
        self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.ADD_LEAVE_TYPE_BUTTON,
            exact=True
        ).first.click()

        # Verify the popup is open
        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()

        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.ADD_LEAVE_TYPE_DIALOG_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Generate a random alphanumeric type code
        type_code = f"UL{random.randint(1000, 9999)}"

        # Fill required fields
        dialog.get_by_role(
            "textbox",
            name=re.compile(r"Type Code", re.I)
        ).fill(type_code)

        dialog.get_by_role(
            "textbox",
            name=re.compile(r"Leave Type Name", re.I)
        ).fill("Urgent Leave")

        dialog.get_by_role(
            "textbox",
            name=re.compile(r"Description", re.I)
        ).fill("Urgent only")

        # Locate the same-day application checkbox/switch
        same_day_toggle = dialog.get_by_label(
            LeaveManagementLocators.SAME_DAY_APPLICATION
        )

        expect(same_day_toggle).to_be_visible()

        # Normalize to unchecked so both states can be tested
        if same_day_toggle.is_checked():
            same_day_toggle.click()

        expect(same_day_toggle).not_to_be_checked()

        # Enable and verify
        same_day_toggle.click()
        expect(same_day_toggle).to_be_checked()

        # Disable and verify
        same_day_toggle.click()
        expect(same_day_toggle).not_to_be_checked()

        # Enable again for final submission
        same_day_toggle.click()
        expect(same_day_toggle).to_be_checked()

        # Locate the dialog's submit button
        submit_button = dialog.get_by_role(
            "button",
            name=LeaveManagementLocators.ADD_LEAVE_TYPE_BUTTON,
            exact=True
        )

        # Verify required fields enable the submit button
        expect(submit_button).to_be_enabled()

        # Submit the form
        submit_button.click()

        # Verify the new leave type appears in the list
        urgent_leave_row = self._urgent_leave_row()
        expect(urgent_leave_row).to_be_visible()
        expect(urgent_leave_row).to_contain_text("Urgent only")

    def disable_same_day_application(self):
        """Edit Urgent Leave and disable same-day application."""

        # Navigate to Leave Management if not already there
        if not re.search(r"/dashboard/leave/?$", self.page.url):
            self.navigate_to_leave_management()

        # Open Leave Types if the section is not already displayed
        leave_types_heading = self.page.get_by_role(
            "heading",
            name=LeaveManagementLocators.LEAVE_TYPES_HEADING,
            exact=True
        )

        if not leave_types_heading.is_visible():
            self.click_leave_types()

        # Find the row for the newly created leave type
        urgent_leave_row = self._urgent_leave_row()
        expect(urgent_leave_row).to_be_visible()

        # The first action button is Edit; the second is Delete
        edit_button = urgent_leave_row.get_by_role("button").first
        expect(edit_button).to_be_visible()
        edit_button.click()

        # Verify Edit Leave Type dialog
        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible()
        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.EDIT_LEAVE_TYPE_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Locate the same-day application switch
        same_day_toggle = dialog.get_by_label(
            LeaveManagementLocators.SAME_DAY_APPLICATION
        )

        expect(same_day_toggle).to_be_visible()

        # Disable the toggle only if it is currently enabled
        if same_day_toggle.is_checked():
            same_day_toggle.click()

        # Verify that the toggle is disabled
        expect(same_day_toggle).not_to_be_checked()

        # Save changes
        update_button = dialog.get_by_role(
            "button",
            name=LeaveManagementLocators.UPDATE_LEAVE_TYPE_BUTTON,
            exact=True
        )

        expect(update_button).to_be_enabled()
        update_button.click()

        # Verify the dialog closes after saving
        expect(dialog).not_to_be_visible()

        # Verify the leave type still exists
        expect(urgent_leave_row).to_be_visible()

        # Reopen Edit to verify the saved state persists
        urgent_leave_row.get_by_role("button").first.click()

        edit_dialog = self.page.get_by_role("dialog")
        expect(edit_dialog).to_be_visible()

        saved_toggle = edit_dialog.get_by_label(
            LeaveManagementLocators.SAME_DAY_APPLICATION
        )

        expect(saved_toggle).not_to_be_checked()

        # Leave no modal open; the same page fixture is reused by later tests.
        cancel_button = edit_dialog.get_by_role(
            "button", name=LeaveManagementLocators.CANCEL_BUTTON, exact=True
        )
        if cancel_button.count() and cancel_button.is_visible():
            cancel_button.click()
        expect(edit_dialog).not_to_be_visible()

    def edit_leave_type_and_cancel(self):
        """Open Edit Leave Type for Urgent Leave and cancel."""

        # Locate the row for the newly created leave type
        leave_type_row = self._urgent_leave_row()
        expect(leave_type_row).to_be_visible()

        # Click the Edit button within the Urgent Leave row
        edit_button = leave_type_row.get_by_role("button").first
        expect(edit_button).to_be_visible()
        edit_button.click()

        # Verify the Edit Leave Type dialog opens
        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()

        expect(
            dialog.get_by_role(
                "heading",
                name="Edit Leave Type",
                exact=True
            )
        ).to_be_visible()

        # Click Cancel without saving any changes
        cancel_button = dialog.get_by_role(
            "button",
            name="Cancel",
            exact=True
        )

        expect(cancel_button).to_be_visible()
        cancel_button.click()

        # Verify the dialog closes
        expect(dialog).not_to_be_visible()

        # Verify the leave type remains in the list
        expect(leave_type_row).to_be_visible()

    def refresh_and_verify_created_leave_type(self):
        """Refresh Leave Types and verify Urgent Leave still appears."""

        # Ensure the Leave Types section is open, even if another test changed screens.
        self.click_leave_types()
        expect(
            self.page.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_TYPES_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Locate the newly created leave type before refreshing
        leave_type_row = self._urgent_leave_row()
        expect(leave_type_row, "Urgent Leave should exist before refreshing.").to_be_visible()

        # Click the Refresh data button
        refresh_button = self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.REFRESH_DATA_BUTTON,
            exact=True
        )

        expect(refresh_button).to_be_visible()
        refresh_button.click()

        # Verify the latest created leave type remains after refresh
        refreshed_row = self._urgent_leave_row()
        expect(
            refreshed_row,
            "Urgent Leave was not found after refreshing the Leave Types list."
        ).to_be_visible()

        # Verify the description as well
        expect(
            refreshed_row.get_by_role(
                "cell",
                name=LeaveManagementLocators.CREATED_LEAVE_TYPE_DESCRIPTION,
                exact=True
            )
        ).to_be_visible()

    def verify_leave_policies_and_open_entitlement(self):
        """Verify Leave Policies page and open the Add Entitlement popup."""

        # Navigate to Leave Management
        self.navigate_to_leave_management()
        self.verify_leave_management_page()

        # Click the Leave Policies card button on the landing page
        leave_policies_button = self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.OPEN_LEAVE_POLICIES_BUTTON,
            exact=True
        )

        expect(leave_policies_button).to_be_visible()
        leave_policies_button.click()

        # Verify the Leave Policies page has loaded
        expect(self.page).to_have_url(
            re.compile(r".*/dashboard/leave(?:/policies)?/?$")
        )

        expect(
            self.page.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_POLICIES_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Click Add Entitlement
        add_entitlement_button = self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.ADD_ENTITLEMENT_BUTTON,
            exact=True
        )

        expect(add_entitlement_button).to_be_visible()
        add_entitlement_button.click()

        # Verify the popup opens
        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()

        return dialog

    def create_leave_policy_entitlement(self):
        """Create an entitlement for field_executive for 2026."""

        # Navigate to Leave Policies and open Add Entitlement
        dialog = self.verify_leave_policies_and_open_entitlement()

        # Verify popup heading
        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.ADD_LEAVE_POLICY_HEADING,
                exact=True
            )
        ).to_be_visible()

        # 1. Select Role: field_executive
        role_dropdown = dialog.get_by_role("combobox").nth(0)
        role_dropdown.click()

        role_option = self.page.get_by_role(
            "option",
            name=LeaveManagementLocators.ROLE_FIELD_EXECUTIVE,
            exact=True
        )
        expect(role_option).to_be_visible()
        role_option.click()

        # 2. Select Year: 2026
        year_dropdown = dialog.get_by_role("combobox").nth(1)
        year_dropdown.click()

        year_option = self.page.get_by_role(
            "option",
            name=LeaveManagementLocators.ENTITLEMENT_YEAR,
            exact=True
        )
        expect(year_option).to_be_visible()
        year_option.click()

        # 3. Select Urgent Leave in the first entitlement row
        leave_type_dropdown = dialog.get_by_role("combobox").nth(2)
        leave_type_dropdown.click()

        leave_type_option = self.page.get_by_role(
            "option",
            name=LeaveManagementLocators.ENTITLEMENT_LEAVE_TYPE,
            exact=True
        )
        expect(leave_type_option).to_be_visible()
        leave_type_option.click()

        # 4. Enter Total Days = 1
        total_days_field = dialog.get_by_role("spinbutton").first
        total_days_field.fill(
            LeaveManagementLocators.ENTITLEMENT_TOTAL_DAYS
        )

        expect(total_days_field).to_have_value("1")

        # 5. Verify entitlement section and selected leave type
        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_ENTITLEMENTS_HEADING,
                exact=True
            )
        ).to_be_visible()

        expect(
            dialog.get_by_text(
                LeaveManagementLocators.ENTITLEMENT_LEAVE_TYPE,
                exact=True
            )
        ).to_be_visible()

        # Verify the Summary section is visible
        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.ENTITLEMENT_SUMMARY_HEADING,
                exact=True
            )
        ).to_be_visible()

        # 6. Add another entitlement row
        add_row_button = dialog.get_by_role(
            "button",
            name=LeaveManagementLocators.ADD_ENTITLEMENT_ROW_BUTTON,
            exact=True
        )

        expect(add_row_button).to_be_visible()
        add_row_button.click()

        # Verify an additional leave type dropdown is available
        expect(dialog.get_by_role("combobox")).to_have_count(4)

        # Delete the newly added, second entitlement row.
        # Supports the common Material UI Delete and DeleteOutline icons.
        delete_buttons = dialog.locator(
            'button:has(svg[data-testid="DeleteIcon"]), '
            'button:has(svg[data-testid="DeleteOutlineIcon"])'
        )

        expect(delete_buttons).to_have_count(2)
        delete_buttons.last.click()

        # Verify the extra row has been removed
        expect(dialog.get_by_role("combobox")).to_have_count(3)
        expect(delete_buttons).to_have_count(1)

        # 7. Save the entitlement
        save_button = dialog.get_by_role(
            "button",
            name=LeaveManagementLocators.SAVE_ENTITLEMENT_BUTTON,
            exact=True
        )

        expect(save_button).to_be_enabled()
        save_button.click()

        # Verify the popup closes after saving
        expect(dialog).not_to_be_visible()

        # Verify the Leave Policy Directory page
        expect(
            self.page.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_POLICIES_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Find the field_executive role accordion
        role_section = self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.FIELD_EXECUTIVE_ROLE,
            exact=True
        )

        expect(role_section).to_be_visible()

        # Expand the role if it is currently collapsed
        if role_section.get_attribute("aria-expanded") != "true":
            role_section.click()

        # The created entitlement can be rendered in a table that is not
        # always nested under the same region role. Match the row by the
        # leave type and day count text instead of relying on a fragile region
        # hierarchy that may differ across app renders.
        entitlement_row = self.page.locator("tr").filter(
            has_text=LeaveManagementLocators.CREATED_ENTITLEMENT_NAME
        ).filter(
            has_text=LeaveManagementLocators.CREATED_ENTITLEMENT_DAYS
        ).first

        expect(entitlement_row).to_be_visible()

        expect(entitlement_row).to_contain_text(LeaveManagementLocators.CREATED_ENTITLEMENT_NAME)
        expect(entitlement_row).to_contain_text(LeaveManagementLocators.CREATED_ENTITLEMENT_DAYS)

    def verify_add_entitlement_cancel(self):
        """Verify Add Entitlement popup closes when Cancel is clicked."""

        # Navigate to Leave Management landing page
        self.navigate_to_leave_management()

        # Open Leave Policies
        self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.LEAVE_POLICIES_BUTTON,
            exact=True
        ).click()

        # Verify Leave Policy Directory heading
        expect(
            self.page.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_POLICIES_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Click Add Entitlement
        self.page.get_by_role(
            "button",
            name=LeaveManagementLocators.ADD_ENTITLEMENT_BUTTON,
            exact=True
        ).click()

        # Verify the popup opens
        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()

        # Verify the actual popup heading
        expect(
            dialog.get_by_role(
                "heading",
                name=LeaveManagementLocators.ADD_ENTITLEMENT_DIALOG_HEADING,
                exact=True
            )
        ).to_be_visible()

        # Click Cancel
        dialog.get_by_role(
            "button",
            name=LeaveManagementLocators.CANCEL_BUTTON,
            exact=True
        ).click()

        # Verify the popup closes
        expect(dialog).not_to_be_visible()

        # Verify the Leave Policies page remains visible
        expect(
            self.page.get_by_role(
                "heading",
                name=LeaveManagementLocators.LEAVE_POLICIES_HEADING,
                exact=True
            )
        ).to_be_visible()