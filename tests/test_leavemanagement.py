import pytest
from playwright.sync_api import expect

from pages.dashboard_page import DashboardPage
from pages.fieldexecutivedashboard_page import FieldExecutiveDashboardPage
from pages.leavemanagement_page import LeaveManagementPage
from pages.login_page import LoginPage


@pytest.fixture(scope="class")
def keep_ems_submenu_open(logged_in_page):
    """Keep EMS expanded for the complete Leave Management test sequence."""
    nav = logged_in_page.get_by_label("mailbox folders")
    ems_menu = nav.get_by_role(
        "button", name="EMS", exact=True
    )
    leave_management_menu = nav.get_by_role(
        "button", name="Leave Management", exact=True
    )

    expect(ems_menu).to_be_visible()
    ems_menu.click()
    expect(leave_management_menu).to_be_visible()

    yield

    ems_menu.click()
    expect(leave_management_menu).not_to_be_visible()


@pytest.mark.order(10)
@pytest.mark.usefixtures("keep_ems_submenu_open")
class TestLeaveManagement:

    def test_leave_management_navigation(self, logged_in_page):
        """Verify EMS > Leave Management navigation."""

        leave_page = LeaveManagementPage(logged_in_page)

        # Navigate to Leave Management through EMS
        leave_page.navigate_to_leave_management()

        # Verify that the Leave Management page opens successfully
        leave_page.verify_leave_management_page()

    def test_leave_types_navigation(self, logged_in_page):
        """Verify heading and navigation to Leave Types."""

        leave_page = LeaveManagementPage(logged_in_page)

        # Click Leave Types and verify the section opens
        leave_page.click_leave_types()

    def test_create_leave_type(self, logged_in_page):
        leave_page = LeaveManagementPage(logged_in_page)

        leave_page.create_leave_type()

    def test_edit_leave_type_disable_same_day(self, logged_in_page):
        """Verify same-day application can be disabled and saved."""

        leave_page = LeaveManagementPage(logged_in_page)

        leave_page.disable_same_day_application()

    def test_edit_leave_type_and_cancel(self, logged_in_page):
        """Verify editing a leave type can be cancelled."""

        leave_page = LeaveManagementPage(logged_in_page)

        leave_page.click_leave_types()
        leave_page.edit_leave_type_and_cancel()

    def test_verify_created_leave_type_without_refresh(self, logged_in_page):
        """Verify the newly created leave type remains visible in this session."""

        leave_page = LeaveManagementPage(logged_in_page)

        leave_page.click_leave_types()
        expect(leave_page._urgent_leave_row()).to_contain_text("Urgent only")

    def test_leave_policies_add_entitlement_popup(self, logged_in_page):
        """Verify Leave Policies heading and Add Entitlement popup."""

        leave_page = LeaveManagementPage(logged_in_page)

        dialog = leave_page.verify_leave_policies_and_open_entitlement()

        # Confirm the popup is displayed correctly
        expect(dialog).to_be_visible()

    def test_create_leave_policy_entitlement(self, logged_in_page):
        """Verify entitlement creation, summary, add-row, delete-row, and save."""

        leave_page = LeaveManagementPage(logged_in_page)
        leave_page.create_leave_policy_entitlement()

    def test_leave_policy_year_filter_updates_entitlements(self, logged_in_page):
        """Verify changing the policy year updates the displayed entitlements."""
        leave_page = LeaveManagementPage(logged_in_page)
        leave_page.navigate_to_leave_management()
        leave_page.verify_leave_management_page()

        logged_in_page.get_by_role(
            "button",
            name="Open Leave Policies",
            exact=True
        ).click()

        expect(
            logged_in_page.get_by_role(
                "heading",
                name="Leave Policy Directory",
                exact=True
            )
        ).to_be_visible()

        year_dropdown = logged_in_page.get_by_role("combobox").first
        year_dropdown.click()
        year_options = logged_in_page.get_by_role("option")
        available_years = [
            option.inner_text().strip()
            for option in year_options.all()
        ]

        assert "2026" in available_years, (
            f"Expected 2026 in the Year dropdown; found {available_years}."
        )
        other_year = next(
            (year for year in available_years if year != "2026"),
            None
        )
        assert other_year is not None, (
            f"Expected a year besides 2026 in the Year dropdown; found {available_years}."
        )

        logged_in_page.get_by_role(
            "option", name="2026", exact=True
        ).click()
        expect(year_dropdown).to_contain_text("2026")

        urgent_entitlement = logged_in_page.locator("tr").filter(
            has_text="Urgent Leave"
        ).filter(
            has_text="1"
        )
        expect(urgent_entitlement.first).to_be_visible()

        year_dropdown.click()
        logged_in_page.get_by_role(
            "option", name=other_year, exact=True
        ).click()
        expect(year_dropdown).to_contain_text(other_year)
        expect(urgent_entitlement).to_have_count(0)

        year_dropdown.click()
        logged_in_page.get_by_role(
            "option", name="2026", exact=True
        ).click()
        expect(year_dropdown).to_contain_text("2026")
        expect(urgent_entitlement.first).to_be_visible()

    def test_add_entitlement_cancel(self, logged_in_page):
        """Verify the Add Entitlement popup closes on Cancel."""

        leave_page = LeaveManagementPage(logged_in_page)

        leave_page.verify_add_entitlement_cancel()

@pytest.mark.order(11)
class TestFieldExecutiveMyLeaves:

    def test_login_as_field_executive_and_open_my_leaves(self, logged_in_page):
        """Switch from the admin account to Field Executive and open My Leaves."""
        DashboardPage(logged_in_page).logout()

        login_page = LoginPage(logged_in_page)
        login_page.login("Field executive")
        logged_in_page.wait_for_load_state("networkidle")

        field_executive_page = FieldExecutiveDashboardPage(logged_in_page)
        field_executive_page.refresh_dashboard()
        field_executive_page.open_my_leaves()
