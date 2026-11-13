import pytest
from pathlib import Path
from uuid import uuid4

from playwright.sync_api import expect

from locators.policiesandprocedure_locators import HRPoliciesLocators
from pages.dashboard_page import DashboardPage
from pages.fieldexecutivedashboard_page import FieldExecutiveDashboardPage
from pages.login_page import LoginPage
from pages.policiesandprocedures_page import HRPoliciesPage

TEST_POLICY_TITLE = f"Important Policy {uuid4().hex[:8]}"
TEST_PROCEDURE_TITLE = f"important procedure {uuid4().hex[:8]}"

@pytest.mark.order(9)
class TestHRPoliciesProcedures:
    """Tests for HR Policies & Procedures."""


    def test_hr_policies_heading_visible(self, logged_in_page):
        """Verify the Policies heading is visible."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()
        policies_page.verify_policies_heading()

    def test_add_new_policy_button_working(self, logged_in_page):
        """Verify Add New Policy opens the dialog."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()
        policies_page.click_add_new_policy()

        # Close the dialog so the next test starts cleanly.
        policies_page.close_add_policy_dialog_if_open()

    def test_create_new_policy(self, logged_in_page):
        """Create a policy and verify the saved result."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()

        pdf_path = (
            Path(__file__).resolve().parents[1]
            / "testdata"
            / "Sai_B_certificate.pdf"
        )

        policies_page.create_new_policy(pdf_path, TEST_POLICY_TITLE)

    def test_search_important_policy(self, logged_in_page):
        """Verify searching for an existing policy."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()

        policies_page.verify_search_functionality(TEST_POLICY_TITLE)

    def test_policy_sort_dropdown(self, logged_in_page):
        """Verify a randomly selected sorting option is applied."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()

        selected_option = (
            policies_page.verify_sort_dropdown_functionality()
        )

        print(
            f"\nSorting functionality selected: {selected_option}"
        )

    def test_policy_version_history_pdf(self, logged_in_page):
        """Verify Version History, PDF preview, download and closing."""

        policies_page = HRPoliciesPage(logged_in_page)

        policies_page.open_policies_procedures()

        # Step 1: Open Version History.
        policies_page.open_version_history(TEST_POLICY_TITLE)

        # Step 2: Click the eye icon and open PDF Preview.
        policies_page.verify_pdf_preview()

        # Step 3: Click Close in PDF Preview.
        policies_page.close_pdf_preview()

        # Step 4: Download the PDF from Version History.
        policies_page.verify_pdf_download()

        # Step 5: Close Version History.
        policies_page.close_version_history()

    def test_view_policy_details_and_close(self, logged_in_page):
        """Verify View Policy opens details and Close dismisses them."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()
        policies_page.verify_view_policy_and_close(TEST_POLICY_TITLE)

    def test_edit_policy_target_audience(self, logged_in_page):
        """Verify that a policy can be assigned two roles."""

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()

        policies_page.edit_policy_target_audience(TEST_POLICY_TITLE)

    def test_procedures_heading_visible(self, logged_in_page):
        """Verify the heading and description on the Procedures tab."""

        policies_page = HRPoliciesPage(logged_in_page)

        # Navigate to the existing Policies & Procedures page.
        policies_page.open_policies_procedures()

        # Click Procedures and verify the heading and description.
        policies_page.open_procedures_tab()
        policies_page.verify_procedures_heading()
    def test_create_new_procedure(self, logged_in_page):
        """Create a procedure and verify the saved result."""

        policies_page = HRPoliciesPage(logged_in_page)

        # Step 4: Locate the PDF in the project's testdata folder.
        pdf_path = (
            Path(__file__).resolve().parents[1]
            / "testdata"
            / "Sai_B_certificate.pdf"
        )

        # Step 5: Create and verify the procedure.
        policies_page.create_new_procedure(pdf_path, TEST_PROCEDURE_TITLE)

    def test_view_procedure_details_and_close(self, logged_in_page):
        """Verify View procedure opens details and Close dismisses them."""

        policies_page = HRPoliciesPage(logged_in_page)

        policies_page.verify_view_procedure_and_close(
            TEST_PROCEDURE_TITLE
        )

    def test_edit_procedure_target_audience(self, logged_in_page):
        """Assign a random employee to an existing procedure."""

        policies_page = HRPoliciesPage(logged_in_page)

        # Step 4: Edit the procedure and select a random employee.
        policies_page.edit_procedure_target_audience(
            TEST_PROCEDURE_TITLE
        )

    def test_restore_procedure_for_all_employees(self, logged_in_page):
        """Restore employee visibility after testing specific assignment."""
        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()
        policies_page.open_procedures_tab()
        policies_page.set_procedure_target_audience_all_employees(
            TEST_PROCEDURE_TITLE
        )

    def test_search_procedure_and_clear(self, logged_in_page):
        """Verify procedure search and clear functionality."""

        policies_page = HRPoliciesPage(logged_in_page)

        # Step 4: Search for the procedure and clear the search.
        policies_page.verify_procedure_search_and_clear(
            TEST_PROCEDURE_TITLE
        )
    def test_procedures_next_previous_pagination(self, logged_in_page):
        """Verify Next and Previous pagination functionality."""

        policies_page = HRPoliciesPage(logged_in_page)

        # Step 1: Open Policies & Procedures.
        policies_page.open_policies_procedures()

        # Step 2: Open the Procedures tab.
        policies_page.open_procedures_tab()

        # Step 3: Verify the Procedures page.
        policies_page.verify_procedures_heading()

        # Step 4: Capture the first row before navigating.
        first_row = logged_in_page.locator("table tbody tr").first
        expect(first_row).to_be_visible(timeout=10000)
        expect(first_row).not_to_have_text("", timeout=15000)
        first_row_cells = first_row.locator("td")
        first_row_before = [
            cell.inner_text().strip()
            for cell in first_row_cells.all()
        ]
        assert any(first_row_before), (
            "No procedure data found on the current page."
        )

        # Step 5: Navigate to the next page and wait for its content to load.
        next_button = logged_in_page.get_by_role(
            "button",
            name=HRPoliciesLocators.PROCEDURES_NEXT_BUTTON,
            exact=True,
        )
        previous_button = logged_in_page.get_by_role(
            "button",
            name=HRPoliciesLocators.PROCEDURES_PREVIOUS_BUTTON,
            exact=True,
        )
        next_button.click()
        expect(first_row).not_to_have_text(
            " ".join(first_row_before),
            timeout=15000,
        )

        # Step 6: Return to the previous page after Previous is enabled.
        expect(previous_button).to_be_enabled(timeout=15000)
        previous_button.click()

        # Step 7: Verify the original page has loaded again.
        expect(first_row_cells).to_have_count(
            len(first_row_before),
            timeout=10000,
        )
        for index, expected_text in enumerate(first_row_before):
            expect(first_row_cells.nth(index)).to_have_text(
                expected_text,
                use_inner_text=True,
                timeout=15000,
            )

    @pytest.mark.order(
        after=(
            "TestFieldExecutiveEmployeePolicies::"
            "test_assigned_policy_and_procedures_are_available"
        )
    )
    def test_delete_created_policy_and_procedure(self, logged_in_page):
        """Relogin as admin and delete the records created by this suite."""
        DashboardPage(logged_in_page).logout()
        LoginPage(logged_in_page).login("admin")
        logged_in_page.wait_for_load_state("networkidle")

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_policies_procedures()
        policies_page.delete_policy(TEST_POLICY_TITLE)

        policies_page.open_procedures_tab()
        policies_page.delete_procedure(TEST_PROCEDURE_TITLE)

class TestFieldExecutiveEmployeePolicies:
    """Verify assigned policies and procedures as a Field Executive."""

    def test_assigned_policy_and_procedures_are_available(self, logged_in_page):
        DashboardPage(logged_in_page).logout()

        LoginPage(logged_in_page).login("Field executive")
        logged_in_page.wait_for_load_state("networkidle")

        FieldExecutiveDashboardPage(logged_in_page).refresh_dashboard()

        policies_page = HRPoliciesPage(logged_in_page)
        policies_page.open_employee_policies()
        policies_page.verify_employee_policy_visible(
            TEST_POLICY_TITLE
        )
        policies_page.accept_employee_policy(
            TEST_POLICY_TITLE
        )
        policies_page.preview_employee_procedure_and_verify_status(
            TEST_PROCEDURE_TITLE
        )