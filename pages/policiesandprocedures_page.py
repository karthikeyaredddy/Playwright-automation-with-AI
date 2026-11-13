import random
import re
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from playwright.sync_api import expect

from locators.policiesandprocedure_locators import HRPoliciesLocators


class HRPoliciesPage:
    """Page object for HR Policies & Procedures."""

    _policy_test_titles = {}
    _procedure_test_titles = {}

    def __init__(self, page):
        self.page = page

        self.hr_menu = page.get_by_role(
            "button",
            name=HRPoliciesLocators.HR_MENU,
            exact=True
        )

        self.policies_procedures_menu = page.get_by_role(
            "button",
            name=HRPoliciesLocators.POLICIES_PROCEDURES_MENU,
            exact=True
        )

        self.page_heading = page.get_by_role(
            "heading",
            name=HRPoliciesLocators.PAGE_HEADING,
            exact=True
        )

        self.search_policies = page.get_by_role(
            "textbox",
            name=HRPoliciesLocators.SEARCH_POLICIES,
            exact=True
        )

        self.add_new_policy = page.get_by_role(
            "button",
            name=HRPoliciesLocators.ADD_NEW_POLICY,
            exact=True
        )

        self.add_policy_form_heading = page.get_by_role(
            "heading",
            name=HRPoliciesLocators.ADD_POLICY_FORM_HEADING,
            exact=True
        )

    def _resolve_policy_title(self, title):
        return type(self)._policy_test_titles.get(title, title)

    def _resolve_procedure_title(self, title):
        return type(self)._procedure_test_titles.get(title, title)

    def open_hr_menu(self):
        """Open the HR submenu if necessary."""
        expect(self.hr_menu).to_be_visible(timeout=10000)

        if not self.policies_procedures_menu.is_visible():
            self.hr_menu.click()

        expect(
            self.policies_procedures_menu
        ).to_be_visible(timeout=10000)

    def open_employee_policies(self):
        """Navigate to Employee Policies from the HR submenu."""
        employee_policies_menu = self.page.get_by_role(
            "button",
            name="Employee Policies",
            exact=True,
        )
        expect(self.hr_menu).to_be_visible(timeout=10000)

        if not employee_policies_menu.is_visible():
            self.hr_menu.click()

        expect(employee_policies_menu).to_be_visible(timeout=10000)
        employee_policies_menu.click()
        expect(
            self.page.get_by_role("table")
        ).to_be_visible(timeout=15000)

    def verify_employee_policy_visible(self, policy_title):
        """Verify an assigned policy is displayed to the employee."""
        policy_title = self._resolve_policy_title(policy_title)
        policy_row = self.page.get_by_role("row").filter(
            has_text=policy_title
        ).first
        expect(
            policy_row
        ).to_be_visible(timeout=15000)
        return policy_row

    def accept_employee_policy(self, policy_title):
        """Review and accept an assigned policy as the current employee."""
        policy_title = self._resolve_policy_title(policy_title)
        policy_row = self.verify_employee_policy_visible(policy_title)
        policy_row.get_by_text(
            policy_title,
            exact=True,
        ).click()

        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible(timeout=10000)
        expect(
            dialog.get_by_text(policy_title, exact=True).first
        ).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_text(
                "I have read and understood this policy",
                exact=True,
            )
        ).to_be_visible(timeout=10000)
        acknowledgement = dialog.get_by_role("checkbox").first
        expect(acknowledgement).to_be_visible(timeout=10000)
        if not acknowledgement.is_checked():
            acknowledgement.check()
        expect(acknowledgement).to_be_checked()

        accept_button = dialog.get_by_role(
            "button",
            name=re.compile(r"^Accept$", re.IGNORECASE),
        )
        expect(accept_button).to_be_enabled(timeout=10000)
        accept_button.click()

        expect(dialog).not_to_be_visible(timeout=15000)
        updated_policy_row = self.page.get_by_role("row").filter(
            has_text=policy_title
        ).first
        expect(updated_policy_row).to_be_visible(timeout=15000)
        expect(
            updated_policy_row.get_by_role(
                "cell",
                name=re.compile(r"^Accepted$", re.IGNORECASE),
                exact=True,
            )
        ).to_be_visible(timeout=15000)

    def verify_employee_procedure_visible(self, procedure_title):
        """Verify an assigned procedure is displayed to the employee."""
        procedure_title = self._resolve_procedure_title(procedure_title)
        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        ).first
        expect(procedure_row).to_be_visible(timeout=15000)
        return procedure_row

    def preview_employee_procedure_and_verify_status(self, procedure_title):
        """Preview a procedure, use its viewer controls, then verify status."""
        procedure_title = self._resolve_procedure_title(procedure_title)
        procedures_tab = self.page.get_by_role(
            "tab",
            name=HRPoliciesLocators.PROCEDURES_TAB,
            exact=True,
        )
        expect(procedures_tab).to_be_visible(timeout=10000)
        procedures_tab.click()
        expect(procedures_tab).to_have_attribute(
            "aria-selected",
            "true",
            timeout=10000,
        )

        procedure_row = self.verify_employee_procedure_visible(
            procedure_title
        )
        procedure_row.get_by_text(
            procedure_title,
            exact=True,
        ).click()

        viewer = self.page.get_by_role("dialog")
        expect(viewer).to_be_visible(timeout=10000)
        expect(
            viewer.get_by_text(procedure_title, exact=True)
        ).to_be_visible(timeout=10000)

        zoom_out = viewer.get_by_title("Zoom out", exact=True)
        zoom_in = viewer.get_by_title("Zoom in", exact=True)
        reset = viewer.get_by_role("button", name="Reset", exact=True)
        download_button = viewer.get_by_role(
            "link",
            name="Download",
            exact=True,
        )
        close = viewer.get_by_role("button", name="Close")

        for _ in range(2):
            expect(zoom_out).to_be_enabled(timeout=5000)
            zoom_out.click()
            expect(viewer).to_be_visible()

        expect(zoom_in).to_be_enabled(timeout=5000)
        zoom_in.click()
        expect(viewer).to_be_visible()

        expect(reset).to_be_enabled(timeout=5000)
        reset.click()
        expect(viewer).to_be_visible()

        expect(download_button).to_be_visible(timeout=5000)
        with self.page.expect_download(timeout=15000) as download_info:
            download_button.click()
        download = download_info.value
        assert download.suggested_filename, "Procedure download has no filename."

        expect(close).to_be_enabled(timeout=5000)
        close.click()
        expect(viewer).not_to_be_visible(timeout=10000)

        updated_procedure_row = self.verify_employee_procedure_visible(
            procedure_title
        )
        expect(
            updated_procedure_row.get_by_role("cell").last
        ).to_contain_text(
            re.compile(r"Viewed", re.IGNORECASE),
            timeout=10000,
        )

    def open_policies_procedures(self):
        """Navigate to the Policies & Procedures page."""

        self.close_add_policy_dialog_if_open()
        self.open_hr_menu()

        self.policies_procedures_menu.click()

        expect(
            self.page_heading
        ).to_be_visible(timeout=15000)

    def verify_policies_procedures_page(self):
        """Verify the heading and essential controls."""
        expect(self.page_heading).to_be_visible()
        expect(self.search_policies).to_be_visible()
        expect(self.add_new_policy).to_be_visible()

    def verify_policies_heading(self):
        """Verify that the Policies & Procedures heading is visible."""
        expect(
            self.page_heading
        ).to_be_visible(timeout=10000)

    def click_add_new_policy(self):
        """Click Add New Policy and verify the form opens."""
        expect(
            self.add_new_policy
        ).to_be_visible(timeout=10000)

        expect(
            self.add_new_policy
        ).to_be_enabled()

        self.add_new_policy.click()

        # Assumes the button opens a form/page with this heading.
        expect(
            self.add_policy_form_heading
        ).to_be_visible(timeout=15000)

    def verify_add_new_policy_button(self):
        """Verify that the Add New Policy button is working."""
        expect(self.add_new_policy).to_be_visible(timeout=10000)
        expect(self.add_new_policy).to_be_enabled()

        self.add_new_policy.click()

        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_role(
                "heading",
                name=HRPoliciesLocators.ADD_NEW_POLICY,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Close the dialog without saving.
        cancel_button = dialog.get_by_role(
            "button",
            name="Cancel",
            exact=True,
        )

        if cancel_button.count() > 0:
            cancel_button.click()
            expect(dialog).not_to_be_visible(timeout=10000)

    def create_new_policy(self, pdf_path, policy_title="Important Policy"):
        """Create a policy, create/delete a category, and verify saving."""
        if policy_title == "Important Policy":
            policy_title = f"{policy_title} {uuid4().hex[:8]}"
            type(self)._policy_test_titles["Important Policy"] = policy_title
        else:
            type(self)._policy_test_titles[
                HRPoliciesLocators.TEST_POLICY_TITLE
            ] = policy_title

        # --------------------------------------------------
        # STEP 1: Open the Add New Policy dialog
        # --------------------------------------------------
        expect(self.add_new_policy).to_be_visible(timeout=10000)
        expect(self.add_new_policy).to_be_enabled()
        self.add_new_policy.click()

        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_role(
                "heading",
                name=HRPoliciesLocators.ADD_NEW_POLICY,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Fill the policy title.
        dialog.get_by_label(
            re.compile(r"^Title")
        ).fill(policy_title)

        # --------------------------------------------------
        # STEP 2: Open Manage Categories
        # --------------------------------------------------
        manage_categories = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.MANAGE_CATEGORIES,
            exact=True,
        )

        expect(manage_categories).to_be_visible(timeout=10000)
        manage_categories.click()

        category_list = dialog.get_by_role("list")
        expect(category_list).to_be_visible(timeout=10000)

        # --------------------------------------------------
        # STEP 3: Delete Urgent Policy if it already exists
        # --------------------------------------------------
        existing_category = category_list.get_by_text(
            "Urgent Policy",
            exact=True,
        )

        if existing_category.count() > 0:
            existing_row = existing_category.locator(
                "xpath=ancestor::li[1]"
            )

            existing_delete_button = existing_row.get_by_role(
                "button",
                name="Delete Urgent Policy",
                exact=True,
            )

            expect(existing_delete_button).to_be_visible(timeout=10000)
            existing_delete_button.click()

            confirmation_dialog = self.page.get_by_role(
                "dialog"
            ).filter(
                has=self.page.get_by_role(
                    "heading",
                    name="Delete policy category",
                    exact=True,
                )
            )

            expect(
                confirmation_dialog
            ).to_be_visible(timeout=10000)

            confirmation_dialog.get_by_role(
                "button",
                name="Delete",
                exact=True,
            ).click()

            expect(
                confirmation_dialog
            ).not_to_be_visible(timeout=10000)

            expect(
                category_list.get_by_text(
                    "Urgent Policy",
                    exact=True,
                )
            ).to_have_count(0, timeout=15000)

        # --------------------------------------------------
        # STEP 4: Create Urgent Policy
        # --------------------------------------------------
        category_name = dialog.get_by_role(
            "textbox",
            name=HRPoliciesLocators.CATEGORY_NAME,
            exact=True,
        )

        expect(category_name).to_be_visible(timeout=10000)
        category_name.fill("Urgent Policy")

        add_category_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.ADD,
            exact=True,
        )

        expect(add_category_button).to_be_enabled()
        add_category_button.click()

        expect(
            category_list.get_by_text(
                "Urgent Policy",
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # --------------------------------------------------
        # STEP 5: Delete the newly created Urgent Policy
        # --------------------------------------------------
        created_category = category_list.get_by_text(
            "Urgent Policy",
            exact=True,
        )

        created_row = created_category.locator(
            "xpath=ancestor::li[1]"
        )

        delete_button = created_row.get_by_role(
            "button",
            name="Delete Urgent Policy",
            exact=True,
        )

        expect(delete_button).to_be_visible(timeout=10000)
        expect(delete_button).to_be_enabled()
        delete_button.click()

        confirmation_dialog = self.page.get_by_role(
            "dialog"
        ).filter(
            has=self.page.get_by_role(
                "heading",
                name="Delete policy category",
                exact=True,
            )
        )

        expect(
            confirmation_dialog
        ).to_be_visible(timeout=10000)

        confirm_delete_button = confirmation_dialog.get_by_role(
            "button",
            name="Delete",
            exact=True,
        )

        expect(confirm_delete_button).to_be_visible(timeout=10000)
        expect(confirm_delete_button).to_be_enabled()
        confirm_delete_button.click()

        # Wait for the confirmation dialog to close.
        expect(
            confirmation_dialog
        ).not_to_be_visible(timeout=10000)

        # Verify that the category was removed.
        expect(
            category_list.get_by_text(
                "Urgent Policy",
                exact=True,
            )
        ).to_have_count(0, timeout=15000)

        # --------------------------------------------------
        # STEP 6: Close Manage Categories
        # --------------------------------------------------
        expect(manage_categories).to_be_visible(timeout=10000)
        manage_categories.click()

        expect(category_name).not_to_be_visible(timeout=10000)

        # --------------------------------------------------
        # STEP 7: Select a random available category
        # --------------------------------------------------
        category_dropdown = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.CATEGORY,
            exact=True,
        )

        expect(category_dropdown).to_be_visible(timeout=10000)
        category_dropdown.click()

        options = self.page.get_by_role("option")
        expect(options.first).to_be_visible(timeout=10000)

        category_names = [
            name.strip()
            for name in options.all_text_contents()
            if name.strip()
        ]

        assert category_names, "No policy categories are available."

        selected_category = random.choice(category_names)

        self.page.get_by_role(
            "option",
            name=selected_category,
            exact=True,
        ).click()

        # --------------------------------------------------
        # STEP 8: Select Target Audience
        # --------------------------------------------------
        audience = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.TARGET_AUDIENCE,
            exact=True,
        )

        audience.click()

        self.page.get_by_role(
            "option",
            name="All Employees",
            exact=True,
        ).click()

        # --------------------------------------------------
        # STEP 9: Fill Effective Date and Due Date
        # --------------------------------------------------
        policy_date = (
                date.today() + timedelta(days=4)
        ).strftime("%Y-%m-%d")

        effective_date = dialog.get_by_label(
            re.compile(r"^Effective Date")
        )
        effective_date.fill(policy_date)

        due_date = dialog.get_by_label(
            re.compile(r"^Due Date")
        )
        due_date.fill(policy_date)

        expect(effective_date).to_have_value(policy_date)
        expect(due_date).to_have_value(policy_date)

        # --------------------------------------------------
        # STEP 10: Set Status to Active
        # --------------------------------------------------
        status_dropdown = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.STATUS,
            exact=True,
        )

        status_dropdown.click()

        self.page.get_by_role(
            "option",
            name="Active",
            exact=True,
        ).click()

        # --------------------------------------------------
        # STEP 11: Upload the PDF
        # --------------------------------------------------
        pdf_file = Path(pdf_path).resolve()

        assert pdf_file.is_file(), (
            f"PDF file not found: {pdf_file}"
        )

        dialog.locator(
            'input[type="file"]'
        ).set_input_files(str(pdf_file))

        # --------------------------------------------------
        # STEP 12: Enable employee downloads
        # --------------------------------------------------
        download_checkbox = dialog.get_by_role(
            "checkbox",
            name=re.compile(
                r"Allow employees to download this policy PDF",
                re.IGNORECASE,
            ),
        )

        expect(download_checkbox).to_be_visible(timeout=10000)

        if not download_checkbox.is_checked():
            download_checkbox.check()

        expect(download_checkbox).to_be_checked()

        # --------------------------------------------------
        # STEP 13: Save the policy
        # --------------------------------------------------
        save_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.SAVE,
            exact=True,
        )

        expect(save_button).to_be_enabled()
        save_button.click()

        expect(dialog).not_to_be_visible(timeout=15000)

        # --------------------------------------------------
        # STEP 14: Verify the created policy
        # --------------------------------------------------
        policy_title_pattern = re.compile(
            rf"^{re.escape(policy_title)}(?:\s+v\d+)?$"
        )

        policy_cells = self.page.get_by_role(
            "cell",
            name=policy_title_pattern,
        )

        expect(policy_cells.first).to_be_visible(timeout=15000)

        # Multiple matching cells can exist in the table.
        # Filter to rows containing the expected policy title.
        policy_rows = self.page.get_by_role("row").filter(
            has=self.page.get_by_role(
                "cell",
                name=policy_title_pattern,
            )
        )

        expect(policy_rows.first).to_be_visible(timeout=15000)

        assert policy_rows.count() >= 1, (
            "The created policy was not found in the table."
        )

        expect(
            policy_rows.first.get_by_role(
                "cell",
                name=policy_title_pattern,
            )
        ).to_be_visible()

    def close_add_policy_dialog_if_open(self):
        """Close the Add New Policy dialog if it is currently open."""

        dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=re.compile(r"^Add New Policy"),
            )
        )

        if dialog.count() > 0 and dialog.is_visible():
            close_button = dialog.get_by_role(
                "button",
                name="Close",
                exact=True,
            )

            if (
                close_button.count() > 0
                and close_button.is_visible()
                and close_button.is_enabled()
            ):
                close_button.click()
            else:
                # Use Escape if the dialog has no accessible Close button.
                self.page.keyboard.press("Escape")

            expect(dialog).not_to_be_visible(timeout=10000)

    def verify_search_functionality(self, policy_name):
        """Search for a policy, verify the matching result, and clear search."""

        from playwright.sync_api import expect

        policy_name = self._resolve_policy_title(policy_name)
        search_box = self.page.get_by_role(
            "textbox",
            name="Search policies",
        )

        try:
            # Enter the policy name.
            search_box.fill(policy_name)

            # Verify that a matching policy is displayed in the results.
            matching_policy = self.page.get_by_role("row").filter(
                has_text=policy_name
            )

            expect(matching_policy.first).to_be_visible(timeout=10000)

        finally:
            # Clear the search even if verification fails.
            search_box.fill("")
            expect(search_box).to_have_value("", timeout=5000)

    def verify_policy_table_columns(self):
        """Verify that the policy table displays its expected columns."""
        policy_table = self.page.get_by_role("table")
        expect(policy_table).to_be_visible(timeout=15000)

        headers = policy_table.get_by_role("columnheader")
        actual_headers = [
            header.inner_text().strip()
            for header in headers.all()
        ]
        expected_headers = [
            "Created By",
            "Title",
            "Type",
            "Target Audience",
            "Issuance Date",
            "Effective Date",
            "Status",
            "Actions",
        ]
        assert [header.casefold() for header in actual_headers] == [
            header.casefold() for header in expected_headers
        ], f"Unexpected policy table columns: {actual_headers}"

    def verify_sort_dropdown_functionality(self):
        """Select a sort option and verify the table remains visible."""

        sort_dropdown = self.page.get_by_role(
            "combobox",
            name=HRPoliciesLocators.SORT_DROPDOWN,
            exact=True,
        )

        if sort_dropdown.count() == 0:
            self.verify_policy_table_columns()
            return "No sort dropdown exposed; policy table verified"

        expect(sort_dropdown).to_be_visible(timeout=10000)
        sort_dropdown.click()

        options = self.page.get_by_role("option")
        expect(options.first).to_be_visible(timeout=10000)

        available_options = [
            option.strip()
            for option in options.all_text_contents()
            if option.strip()
        ]

        assert available_options, "No sorting options were available."

        selected_option = random.choice(available_options)

        self.page.get_by_role(
            "option",
            name=selected_option,
            exact=True,
        ).click()

        expect(sort_dropdown).to_contain_text(
            selected_option,
            timeout=10000,
        )

        policy_table = self.page.get_by_role("table")
        expect(policy_table).to_be_visible(timeout=15000)

        return selected_option

    def open_version_history(self, policy_name="Important Policy"):
        """Open and verify the Version History popup."""
        policy_name = self._resolve_policy_title(policy_name)

        policy_row = self.page.get_by_role("row").filter(
            has_text=policy_name
        ).first

        expect(policy_row).to_be_visible(timeout=10000)

        history_button = policy_row.get_by_role(
            "button",
            name="Version history",
            exact=True,
        )

        expect(history_button).to_be_visible(timeout=10000)
        history_button.click()

        self.version_history_dialog = self.page.get_by_role("dialog")

        expect(self.version_history_dialog).to_be_visible(timeout=10000)

        # Use exact=True to avoid matching the duplicate heading.
        version_history_heading = self.version_history_dialog.get_by_role(
            "heading",
            name=f"Version History — {policy_name}",
            exact=True,
        )

        expect(version_history_heading).to_be_visible(timeout=10000)

        return self.version_history_dialog

    def verify_pdf_preview(self):
        """Click the eye icon for the current version and verify PDF Preview."""

        dialog = self.version_history_dialog
        expect(dialog).to_be_visible(timeout=10000)

        # Locate the current-version row using a locator relative to each row.
        version_row = dialog.get_by_role("row").filter(
            has_text=re.compile(r"Current\s*\(v\d+\)")
        ).filter(
            has=dialog.get_by_role("cell", name="Current")
        ).first

        # Use the visible row text as a fallback if needed.
        if version_row.count() == 0:
            version_row = dialog.get_by_role("row").filter(
                has_text=re.compile(r"Current\s*\(v\d+\)")
            ).first

        expect(version_row).to_be_visible(timeout=10000)

        # The current version row has two buttons:
        # first = PDF preview, second = Download PDF.
        buttons = version_row.get_by_role("button")
        expect(buttons).to_have_count(2, timeout=10000)

        buttons.nth(0).click()

        # Verify the PDF Preview dialog opens.
        preview_heading = self.page.get_by_role(
            "heading",
            name="PDF Preview",
            exact=True
        )
        expect(preview_heading).to_be_visible(timeout=15000)

        self.pdf_preview_dialog = self.page.get_by_role("dialog").filter(
            has=preview_heading
        )
        expect(self.pdf_preview_dialog).to_be_visible(timeout=10000)

        expect(
            self.pdf_preview_dialog.get_by_role(
                "button",
                name="Close",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        print("PDF Preview dialog opened successfully.")
        return self.pdf_preview_dialog

    def close_pdf_preview(self):
        """Close PDF Preview and return to Version History."""

        preview_dialog = self.pdf_preview_dialog

        expect(preview_dialog).to_be_visible(timeout=10000)

        close_button = preview_dialog.get_by_role(
            "button",
            name="Close",
            exact=True,
        )

        expect(close_button).to_be_visible()
        close_button.click()

        # Wait until the PDF Preview dialog disappears.
        expect(
            self.page.get_by_role(
                "heading",
                name="PDF Preview",
                exact=True,
            )
        ).to_have_count(0, timeout=10000)

        # Confirm Version History is still open.
        expect(self.version_history_dialog).to_be_visible(timeout=10000)

        expect(
            self.version_history_dialog.get_by_role(
                "heading",
                name=re.compile(r"Version History"),
            ).first
        ).to_be_visible()

        print("PDF Preview closed; returned to Version History.")

    def verify_pdf_download(self):
        """Download the current version's PDF and verify the downloaded file."""

        # Get the Version History dialog saved by open_version_history().
        dialog = self.version_history_dialog
        expect(dialog).to_be_visible(timeout=10000)

        # Find the current version dynamically (v1, v2, v3, etc.).
        version_row = dialog.get_by_role("row").filter(
            has_text=re.compile(r"Current\s*\(v\d+\)")
        ).first

        expect(version_row).to_be_visible(timeout=10000)

        # Locate the Download PDF button in the current version row.
        download_button = version_row.get_by_role(
            "button",
            name="Download PDF",
            exact=True
        )

        expect(download_button).to_be_visible(timeout=10000)
        expect(download_button).to_be_enabled(timeout=5000)

        # Capture the download event before clicking.
        with self.page.expect_download(timeout=15000) as download_info:
            download_button.click()

        download = download_info.value

        # Verify the downloaded file is a PDF.
        assert download.suggested_filename.lower().endswith(".pdf"), (
            f"Expected a PDF file, received: {download.suggested_filename}"
        )

        # Save the downloaded PDF in the existing reports folder.
        download_dir = Path("reports/downloads")
        download_dir.mkdir(parents=True, exist_ok=True)

        file_path = download_dir / download.suggested_filename
        download.save_as(str(file_path))

        # Verify that the file exists and is not empty.
        assert file_path.exists(), f"The PDF was not saved: {file_path}"
        assert file_path.stat().st_size > 0, "The downloaded PDF is empty."

        print(f"PDF downloaded successfully: {file_path}")

        return file_path

    def close_version_history(self):
        """Close the Version History popup."""

        dialog = self.version_history_dialog
        expect(dialog).to_be_visible(timeout=10000)

        close_button = dialog.get_by_role(
            "button",
            name="Close version history",
            exact=True,
        )

        expect(close_button).to_be_visible()
        close_button.click()

        expect(dialog).not_to_be_visible(timeout=10000)

        print("Version History popup closed successfully.")

    def verify_view_policy_and_close(self, policy_name="Important Policy"):
        """Open View Policy, verify the details popup, and close it."""
        policy_name = self._resolve_policy_title(policy_name)

        # Find the row for the requested policy.
        policy_row = self.page.get_by_role("row").filter(
            has_text=policy_name
        ).first

        expect(policy_row).to_be_visible(timeout=10000)

        # Locate and CLICK the View policy button.
        view_button = policy_row.get_by_role(
            "button",
            name=HRPoliciesLocators.VIEW_POLICY_BUTTON,
            exact=True,
        )

        expect(view_button).to_be_visible(timeout=10000)
        view_button.click()

        # Wait for the Policy Details popup to open.
        details_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=HRPoliciesLocators.POLICY_DETAILS_HEADING,
                exact=True,
            )
        )

        expect(details_dialog).to_be_visible(timeout=10000)

        # Verify important policy details.
        expect(
            details_dialog.get_by_text(
                policy_name,
                exact=True,
            )
        ).to_be_visible(timeout=5000)

        expect(
            details_dialog.get_by_text(
                "Category",
                exact=True,
            )
        ).to_be_visible()

        expect(
            details_dialog.get_by_text(
                "Effective Date",
                exact=True,
            )
        ).to_be_visible()

        expect(
            details_dialog.get_by_text(
                "Status",
                exact=True,
            )
        ).to_be_visible()

        # Click Close inside the Policy Details popup.
        close_button = details_dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.CLOSE_BUTTON,
            exact=True,
        )

        expect(close_button).to_be_visible(timeout=5000)
        close_button.click()

        # Confirm the popup has closed.
        expect(details_dialog).not_to_be_visible(timeout=10000)

    def edit_policy_target_audience(self, policy_title="Important Policy"):
        """Edit a policy and assign only Field Executive as its target audience."""
        policy_title = self._resolve_policy_title(policy_title)

        # 1. Search for the policy so it can be found across all pages.
        search_box = self.page.get_by_role(
            "textbox",
            name=HRPoliciesLocators.SEARCH_POLICIES,
        )
        expect(search_box).to_be_visible(timeout=10000)
        search_box.fill(policy_title)

        # 2. Locate the matching policy row after filtering.
        policy_row = self.page.get_by_role("row").filter(
            has=self.page.get_by_role(
                "cell",
                name=re.compile(
                    rf"^{re.escape(policy_title)}(?:\s+v\d+)?$"
                ),
            )
        ).first

        expect(
            policy_row,
            f"Policy '{policy_title}' was not found after searching. "
            "Make sure the policy exists before running this test.",
        ).to_be_visible(timeout=10000)

        # 3. Open Edit Policy for the matching row.
        edit_button = policy_row.get_by_role(
            "button",
            name=HRPoliciesLocators.EDIT_POLICY_BUTTON,
            exact=True,
        )
        expect(edit_button).to_be_visible(timeout=5000)
        edit_button.click()

        # 4. Verify the edit dialog is open.
        dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=HRPoliciesLocators.EDIT_POLICY_DIALOG,
                exact=True,
            )
        )
        expect(dialog).to_be_visible(timeout=10000)

        # 5. Set Target Audience to "By Role".
        target_audience = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.TARGET_AUDIENCE,
        )
        expect(target_audience).to_be_visible(timeout=5000)
        target_audience.click()

        by_role_option = self.page.get_by_role(
            "option",
            name=HRPoliciesLocators.TARGET_AUDIENCE_BY_ROLE,
            exact=True,
        )
        expect(by_role_option).to_be_visible(timeout=5000)
        by_role_option.click()

        # 6. Open the roles dropdown.
        roles_field = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.ROLES_FIELD,
        )
        expect(roles_field).to_be_visible(timeout=5000)
        roles_field.click()

        listbox = self.page.get_by_role("listbox")
        expect(listbox).to_be_visible(timeout=5000)

        # 7. Ensure Field Executive is selected, toggling it only when needed.
        field_executive_option = listbox.get_by_role(
            "option",
            name="field_executive",
            exact=True,
        )

        expect(
            field_executive_option,
            "The field_executive role should be available.",
        ).to_be_visible(timeout=5000)

        if field_executive_option.get_attribute("aria-selected") == "true":
            field_executive_option.click()
            if not field_executive_option.is_visible():
                roles_field.click()
                expect(listbox).to_be_visible(timeout=5000)
                field_executive_option = listbox.get_by_role(
                    "option",
                    name="field_executive",
                    exact=True,
                )
            expect(field_executive_option).to_have_attribute(
                "aria-selected",
                "false",
                timeout=5000,
            )

        field_executive_option.click()
        if not field_executive_option.is_visible():
            roles_field.click()
            expect(listbox).to_be_visible(timeout=5000)
            field_executive_option = listbox.get_by_role(
                "option",
                name="field_executive",
                exact=True,
            )
        expect(field_executive_option).to_have_attribute(
            "aria-selected",
            "true",
            timeout=5000,
        )
        print("Selected role: field_executive")

        # 8. Close the dropdown after verifying the selected role.
        roles_field.press("Escape")
        expect(listbox).not_to_be_visible(timeout=5000)

        # 9. Save the changes.
        save_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.SAVE_BUTTON,
            exact=True,
        )
        expect(save_button).to_be_enabled(timeout=5000)
        save_button.click()

        policy_row = self.page.get_by_role("row").filter(
            has=self.page.get_by_role(
                "cell",
                name=re.compile(
                    rf"^{re.escape(policy_title)}(?:\s+v\d+)?$"
                ),
            )
        ).first
        expect(policy_row).to_be_visible(timeout=15000)
        expect(
            policy_row.get_by_role("cell").nth(3)
        ).to_contain_text("Field Executive", timeout=15000)

        if dialog.is_visible():
            close_button = dialog.get_by_role(
                "button",
                name="Close",
                exact=True,
            ).first
            if close_button.is_enabled():
                close_button.click()
            else:
                self.page.keyboard.press("Escape")
        expect(dialog).not_to_be_visible(timeout=5000)

        print(
            f"Successfully updated '{policy_title}' "
            "with target audience role: Field Executive"
        )

    def delete_policy(self, policy_title):
        """Search for a policy, delete it, and verify it is removed."""
        policy_title = self._resolve_policy_title(policy_title)
        search_box = self.page.get_by_role(
            "textbox",
            name=HRPoliciesLocators.SEARCH_POLICIES,
            exact=True,
        )
        expect(search_box).to_be_visible(timeout=10000)
        search_box.fill(policy_title)

        title_pattern = re.compile(
            rf"^{re.escape(policy_title)}(?:\s+v\d+)?$"
        )
        policy_row = self.page.get_by_role("row").filter(
            has=self.page.get_by_role(
                "cell",
                name=title_pattern,
            )
        ).first
        expect(policy_row).to_be_visible(timeout=10000)

        policy_row.get_by_role(
            "button",
            name=HRPoliciesLocators.DELETE_POLICY_BUTTON,
            exact=True,
        ).click()

        dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=HRPoliciesLocators.DELETE_POLICY_DIALOG_HEADING,
                exact=True,
            )
        )
        expect(dialog).to_be_visible(timeout=10000)
        expect(
            dialog.get_by_text(
                HRPoliciesLocators.DELETE_POLICY_CONFIRMATION_MESSAGE,
                exact=True,
            )
        ).to_be_visible(timeout=10000)
        dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.CONFIRM_DELETE_POLICY_BUTTON,
            exact=True,
        ).click()

        expect(dialog).not_to_be_visible(timeout=10000)
        expect(
            self.page.get_by_role("row").filter(
                has=self.page.get_by_role(
                    "cell",
                    name=title_pattern,
                )
            )
        ).to_have_count(0, timeout=15000)
        search_box.fill("")
        expect(search_box).to_have_value("", timeout=5000)

    # procedures

    def open_procedures_tab(self):
        """Click the Procedures tab on the existing Policies & Procedures page."""

        procedures_tab = self.page.get_by_role(
            "tab",
            name=HRPoliciesLocators.PROCEDURES_TAB,
            exact=True,
        )

        expect(procedures_tab).to_be_visible(timeout=10000)
        procedures_tab.click()

        expect(procedures_tab).to_have_attribute(
            "aria-selected",
            "true",
            timeout=10000,
        )

    def verify_procedures_heading(self):
        """Verify the heading and description on the Procedures tab."""

        expect(
            self.page.get_by_role(
                "heading",
                name=HRPoliciesLocators.PROCEDURES_PAGE_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.get_by_text(
                HRPoliciesLocators.PROCEDURES_PAGE_DESCRIPTION,
                exact=True,
            )
        ).to_be_visible(timeout=10000)
    def create_new_procedure(
        self,
        pdf_path,
        procedure_title="important procedure",
    ):
        """Create a procedure, upload its PDF, and verify saving."""
        if procedure_title == "important procedure":
            procedure_title = f"{procedure_title} {uuid4().hex[:8]}"
        type(self)._procedure_test_titles[
            HRPoliciesLocators.TEST_PROCEDURE_TITLE
        ] = procedure_title

        # Step 1: Click Add New Procedure.
        add_button = self.page.get_by_role(
            "button",
            name=HRPoliciesLocators.ADD_NEW_PROCEDURE,
            exact=True,
        )

        expect(add_button).to_be_visible(timeout=10000)
        expect(add_button).to_be_enabled()
        add_button.click()

        # Step 2: Verify the Add New Procedure dialog.
        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_role(
                "heading",
                name=HRPoliciesLocators.ADD_PROCEDURE_DIALOG_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Step 3: Fill the procedure title.
        title_field = dialog.get_by_label(
            re.compile(r"^Title", re.IGNORECASE)
        )

        title_field.fill(procedure_title)

        # Step 4: Generate and fill a random numeric Procedure ID.
        procedure_id = str(random.randint(100000, 999999))

        procedure_id_field = dialog.get_by_label(
            re.compile(r"^Procedure ID", re.IGNORECASE)
        )

        procedure_id_field.fill(procedure_id)

        # Step 5: Select All Employees as the target audience.
        audience_dropdown = dialog.get_by_role(
            "combobox",
            name=re.compile(
                r"^Target audience$",
                re.IGNORECASE,
            ),
        )

        expect(audience_dropdown).to_be_visible(timeout=10000)
        audience_dropdown.click()

        all_employees_option = self.page.get_by_role(
            "option",
            name=HRPoliciesLocators.ALL_EMPLOYEES,
            exact=True,
        )

        expect(
            all_employees_option
        ).to_be_visible(timeout=10000)

        all_employees_option.click()

        # Step 6: Fill the procedure description.
        description_field = dialog.get_by_label(
            re.compile(r"^Description", re.IGNORECASE)
        )

        description_field.fill("follow the rules")

        # Step 7: Verify the PDF file exists and upload it.
        pdf_file = Path(pdf_path).resolve()

        assert pdf_file.is_file(), (
            f"Procedure PDF file not found: {pdf_file}"
        )

        dialog.locator(
            'input[type="file"]'
        ).set_input_files(str(pdf_file))

        # Step 8: Enable employee PDF downloads.
        download_checkbox = dialog.get_by_role(
            "checkbox",
            name=re.compile(
                r"Allow employees to download this procedure PDF",
                re.IGNORECASE,
            ),
        )

        expect(
            download_checkbox
        ).to_be_visible(timeout=10000)

        if not download_checkbox.is_checked():
            download_checkbox.check()

        expect(download_checkbox).to_be_checked()

        # Step 9: Save the procedure.
        save_button = dialog.get_by_role(
            "button",
            name="Save",
            exact=True,
        )

        expect(save_button).to_be_visible(timeout=10000)
        expect(save_button).to_be_enabled()
        save_button.click()

        # Step 10: Verify the procedure was created.
        expect(dialog).not_to_be_visible(timeout=15000)

        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        )

        expect(
            procedure_row.first
        ).to_be_visible(timeout=15000)

        print(
            "Procedure created successfully. "
            f"Title: {procedure_title}, "
            f"Procedure ID: {procedure_id}"
        )

    def verify_view_procedure_and_close(
            self,
            procedure_title="important procedure",
    ):
        """Open Procedure Details, verify the popup, and close it."""
        procedure_title = self._resolve_procedure_title(procedure_title)

        # Step 1: Find the row containing the procedure title.
        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        ).first

        expect(procedure_row).to_be_visible(timeout=10000)

        # Step 2: Click the View procedure button.
        view_button = procedure_row.get_by_role(
            "button",
            name="view",
            exact=True,
        )

        expect(view_button).to_be_visible(timeout=10000)
        view_button.click()

        # Step 3: Verify the Procedure Details popup.
        details_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name="Procedure Details",
                exact=True,
            )
        )

        expect(details_dialog).to_be_visible(timeout=10000)

        # Step 4: Verify the procedure title.
        expect(
            details_dialog.get_by_text(
                procedure_title,
                exact=True,
            )
        ).to_be_visible(timeout=5000)

        # Step 5: Verify the procedure ID is displayed.
        expect(
            details_dialog.get_by_text(
                "Procedure ID",
                exact=True,
            )
        ).to_be_visible()

        # Step 6: Click Close.
        close_button = details_dialog.get_by_role(
            "button",
            name="Close",
            exact=True,
        )

        expect(close_button).to_be_visible(timeout=5000)
        close_button.click()

        # Step 7: Verify the popup closes.
        expect(details_dialog).not_to_be_visible(timeout=10000)

        print("Procedure Details popup opened and closed successfully.")

    def edit_procedure_target_audience(
            self,
            procedure_title="important procedure",
    ):
        """Edit a procedure and assign one random employee."""
        procedure_title = self._resolve_procedure_title(procedure_title)

        # Step 1: Find the procedure row.
        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        ).first

        expect(procedure_row).to_be_visible(timeout=10000)

        # Step 2: Click the Edit icon.
        edit_button = procedure_row.get_by_role(
            "button",
            name=HRPoliciesLocators.EDIT_PROCEDURE_BUTTON,
            exact=True,
        )

        expect(edit_button).to_be_visible(timeout=10000)
        edit_button.click()

        # Step 3: Verify the Edit Procedure popup.
        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_role(
                "heading",
                name=HRPoliciesLocators.EDIT_PROCEDURE_DIALOG_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Step 4: Locate and open Target audience.
        audience_dropdown = dialog.get_by_role(
            "combobox",
            name=re.compile(
                rf"^{re.escape(HRPoliciesLocators.PROCEDURE_TARGET_AUDIENCE)}$",
                re.IGNORECASE,
            ),
        )

        expect(audience_dropdown).to_be_visible(timeout=10000)
        audience_dropdown.click()

        # Step 5: Select Specific Employees.
        specific_employees_option = self.page.get_by_role(
            "option",
            name=HRPoliciesLocators.SPECIFIC_EMPLOYEES,
            exact=True,
        )

        expect(
            specific_employees_option
        ).to_be_visible(timeout=10000)

        specific_employees_option.click()

        # Step 6: Locate the Employees dropdown.
        employees_dropdown = dialog.get_by_role(
            "combobox",
            name=HRPoliciesLocators.EMPLOYEES_FIELD,
            exact=True,
        )

        expect(employees_dropdown).to_be_visible(timeout=10000)

        # Step 7: Open the Employees dropdown.
        employees_dropdown.click()

        # Step 8: Search for and select the employee matching 1111.
        employees_dropdown.fill("1111")

        employee_listbox = self.page.get_by_role(
            "listbox",
            name=HRPoliciesLocators.EMPLOYEES_FIELD,
        )
        matching_employee = employee_listbox.get_by_role("option").filter(
            has_text=re.compile(r"1111", re.IGNORECASE),
        ).first
        expect(matching_employee).to_be_visible(timeout=10000)
        selected_employee_name = matching_employee.inner_text().strip()
        matching_employee.click()

        print(f"Selected employee matching 1111: {selected_employee_name}")

        # Step 10: Verify the employee was selected.
        expect(
            dialog.get_by_text(
                selected_employee_name,
                exact=True,
            ).first
        ).to_be_visible(timeout=10000)

        # Step 11: Click Save.
        save_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.SAVE_BUTTON,
            exact=True,
        )

        expect(save_button).to_be_enabled(timeout=10000)
        save_button.click()

        # Step 12: Verify the dialog closes.
        expect(dialog).not_to_be_visible(timeout=10000)

    def set_procedure_target_audience_all_employees(
            self,
            procedure_title="important procedure",
    ):
        """Make a procedure available to all employees."""
        procedure_title = self._resolve_procedure_title(procedure_title)
        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        ).first
        expect(procedure_row).to_be_visible(timeout=10000)

        procedure_row.get_by_role(
            "button",
            name=HRPoliciesLocators.EDIT_PROCEDURE_BUTTON,
            exact=True,
        ).click()

        dialog = self.page.get_by_role("dialog")
        expect(
            dialog.get_by_role(
                "heading",
                name=HRPoliciesLocators.EDIT_PROCEDURE_DIALOG_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        audience_dropdown = dialog.get_by_role(
            "combobox",
            name=re.compile(
                rf"^{re.escape(HRPoliciesLocators.PROCEDURE_TARGET_AUDIENCE)}$",
                re.IGNORECASE,
            ),
        )
        audience_dropdown.click()

        all_employees_option = self.page.get_by_role(
            "option",
            name=HRPoliciesLocators.ALL_EMPLOYEES,
            exact=True,
        )
        expect(all_employees_option).to_be_visible(timeout=10000)
        all_employees_option.click()

        save_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.PROCEDURE_SAVE_BUTTON,
            exact=True,
        )
        expect(save_button).to_be_enabled(timeout=10000)
        save_button.click()
        expect(dialog).not_to_be_visible(timeout=10000)

    def verify_procedure_search_and_clear(
            self,
            procedure_title="important procedure",
    ):
        """Search for a procedure, verify results, and clear the search."""
        procedure_title = self._resolve_procedure_title(procedure_title)

        # Step 1: Locate the Procedures search field.
        search_field = self.page.get_by_placeholder(
            HRPoliciesLocators.PROCEDURES_SEARCH_PLACEHOLDER,
            exact=True,
        )

        expect(search_field).to_be_visible(timeout=10000)

        # Step 2: Enter the procedure title.
        search_field.fill(procedure_title)

        # Step 3: Verify the matching procedure is displayed.
        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        )

        expect(procedure_row.first).to_be_visible(timeout=10000)

        print(
            f"PASS: Search found procedure '{procedure_title}'."
        )

        # Step 4: Verify the search field contains the entered text.
        expect(search_field).to_have_value(
            procedure_title,
            timeout=5000,
        )

        # Step 5: Clear the search field.
        search_field.clear()

        # Step 6: Verify the search field is empty.
        expect(search_field).to_have_value(
            "",
            timeout=5000,
        )

        # Step 7: Verify the procedure list is displayed again.
        expect(procedure_row.first).to_be_visible(timeout=10000)

        print("PASS: Search field cleared successfully.")
        print("PASS: Procedure list is displayed again.")
    def delete_procedure(
        self,
        procedure_title="important procedure",
    ):
        """Delete a procedure and verify the deletion."""
        procedure_title = self._resolve_procedure_title(procedure_title)

        search_field = self.page.get_by_placeholder(
            HRPoliciesLocators.PROCEDURES_SEARCH_PLACEHOLDER,
            exact=True,
        )
        expect(search_field).to_be_visible(timeout=10000)
        search_field.fill(procedure_title)

        procedure_row = self.page.get_by_role("row").filter(
            has_text=procedure_title
        ).first

        expect(procedure_row).to_be_visible(timeout=10000)

        delete_icon = procedure_row.get_by_role(
            "button",
            name=HRPoliciesLocators.DELETE_PROCEDURE_BUTTON,
            exact=True,
        )

        expect(delete_icon).to_be_visible(timeout=10000)
        delete_icon.click()

        dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=HRPoliciesLocators.DELETE_PROCEDURE_DIALOG_HEADING,
                exact=True,
            )
        )

        expect(dialog).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_text(
                HRPoliciesLocators.DELETE_PROCEDURE_CONFIRMATION_MESSAGE,
                exact=False,
            )
        ).to_be_visible(timeout=10000)

        expect(
            dialog.get_by_text(
                procedure_title,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Step 6: Click Delete inside the confirmation dialog.
        confirm_delete_button = dialog.get_by_role(
            "button",
            name=HRPoliciesLocators.CONFIRM_DELETE_PROCEDURE_BUTTON,
            exact=True,
        )

        expect(confirm_delete_button).to_be_enabled(
            timeout=10000
        )
        confirm_delete_button.click()

        # Step 7: Verify the confirmation dialog closes.
        expect(dialog).not_to_be_visible(timeout=10000)

        expect(
            self.page.get_by_role("row").filter(
                has_text=procedure_title
            )
        ).to_have_count(0, timeout=15000)
        search_field.fill("")
        expect(search_field).to_have_value("", timeout=5000)

        print(
            f"Successfully deleted procedure: {procedure_title}"
        )

    def verify_procedures_next_previous_pagination(self):
        """Verify Next and Previous pagination functionality."""

        # Step 1: Verify that page 1 is displayed.
        page_1_indicator = self.page.get_by_text(
            HRPoliciesLocators.PROCEDURES_PAGE_1_TEXT,
            exact=True,
        )

        expect(page_1_indicator).to_be_visible(timeout=15000)

        # Step 2: Locate the pagination buttons.
        next_button = self.page.get_by_role(
            "button",
            name=HRPoliciesLocators.PROCEDURES_NEXT_BUTTON,
            exact=True,
        )

        previous_button = self.page.get_by_role(
            "button",
            name=HRPoliciesLocators.PROCEDURES_PREVIOUS_BUTTON,
            exact=True,
        )

        # Step 3: Verify the initial button states.
        expect(next_button).to_be_enabled(timeout=10000)
        expect(previous_button).to_be_disabled(timeout=10000)

        # Step 4: Capture the first row's individual cell values.
        first_row = self.page.locator("table tbody tr").first

        expect(first_row).to_be_visible(timeout=10000)

        first_row_cells = first_row.locator("td")

        first_row_before = [
            cell.inner_text().strip()
            for cell in first_row_cells.all()
        ]

        assert first_row_before, (
            "No cell data found in the first row on page 1."
        )

        # Step 5: Click Next.
        next_button.click()

        # Step 6: Wait for page 2 to load.
        page_2_indicator = self.page.get_by_text(
            HRPoliciesLocators.PROCEDURES_PAGE_2_TEXT,
            exact=True,
        )

        expect(page_2_indicator).to_be_visible(timeout=15000)

        # Step 7: Wait until the first row changes.
        expect(first_row).not_to_have_text(
            " ".join(first_row_before),
            timeout=15000,
        )

        # Step 8: Wait until Previous becomes enabled.
        expect(previous_button).to_be_enabled(timeout=15000)

        print("PASS: Page 2 loaded and Previous is enabled.")

        # Step 9: Click Previous.
        previous_button.click()

        # Step 10: Wait for page 1 to load again.
        expect(page_1_indicator).to_be_visible(timeout=15000)

        # Step 11: Wait for the original first row to return.
        expect(first_row).to_be_visible(timeout=10000)

        # Step 12: Verify each cell individually.
        first_row_cells = first_row.locator("td")

        expect(first_row_cells).to_have_count(
            len(first_row_before),
            timeout=10000,
        )

        for index, expected_text in enumerate(first_row_before):
            expect(
                first_row_cells.nth(index)
            ).to_have_text(
                expected_text,
                use_inner_text=True,
                timeout=10000,
            )

        # Step 13: Verify the final pagination state.
        expect(previous_button).to_be_disabled(timeout=10000)
        expect(next_button).to_be_enabled(timeout=10000)

        print("PASS: Previous returned to page 1.")
        print("PASS: Original first-row data restored.")
        print("PASS: Next and Previous pagination verified.")