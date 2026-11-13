import pytest
from datetime import date, timedelta

from playwright.sync_api import expect
from pages.route_page import RoutePage


@pytest.mark.order(5)
class TestRoute:
    def test_route_navigation(self, logged_in_page):
        """Verify Field Executive > Route navigation."""

        route_page = RoutePage(logged_in_page)
        route_page.navigate_to_route()

        expect(logged_in_page).to_have_url(RoutePage.ROUTE_URL)
        route_page.verify_month_filter_visible()

    def test_route_monthly_filter(self, logged_in_page):
        """Verify the monthly filter is visible and opens."""

        route_page = RoutePage(logged_in_page)

        selected_month = route_page.get_selected_month()
        assert selected_month, "No month is displayed"

        route_page.open_month_filter()

        expect(
            logged_in_page.get_by_role(
                "menuitem",
                name="January",
                exact=True,
            )
        ).to_be_visible(timeout=5000)

        route_page.close_month_filter()

    def test_create_route_opens_successfully(self, logged_in_page):
        """Verify Create Route opens the partner-selection page."""

        route_page = RoutePage(logged_in_page)
        route_page.click_create_route()

        expect(
            route_page.nearby_partners_heading
        ).to_be_visible(timeout=15000)

    def test_select_two_nearby_partners(self, logged_in_page):
        """Verify two nearby partners can be selected."""

        route_page = RoutePage(logged_in_page)

        route_page.select_two_nearby_partners()

        expect(
            logged_in_page.get_by_text("2 selected", exact=True)
        ).to_be_visible(timeout=10000)

    def test_confirm_two_selected_partners(self, logged_in_page):
        """Verify confirmation opens the route schedule popup."""

        route_page = RoutePage(logged_in_page)
        route_page.confirm_partner_selection()

        dialog = logged_in_page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=15000)
        expect(
            dialog.get_by_text(
                "Plan route schedule",
                exact=True,
            )
        ).to_be_visible(timeout=10000)

    def test_save_urgent_route(self, logged_in_page):
        """Save the route and verify it appears under My Routes."""

        route_page = RoutePage(logged_in_page)

        # Continue from the already-open Plan route schedule popup.
        details = route_page.fill_route_schedule_form()
        route_page.save_route_schedule()

        page = logged_in_page

        # Wait until the My Routes page is displayed.
        expect(
            page.get_by_text("My Routes", exact=True)
        ).to_be_visible(timeout=15000)

        # Find the card for the newly created route.
        route_name = page.get_by_text("Urgent", exact=True).first
        expect(route_name).to_be_visible(timeout=15000)

        # Verify the saved route's effective date range.
        expected_from = date.today() + timedelta(days=1)
        expected_until = expected_from + timedelta(days=2)

        expect(
            page.get_by_text(
                f"{expected_from.day} {expected_from.strftime('%b %Y')} – "
                f"{expected_until.day} {expected_until.strftime('%b %Y')}",
                exact=False,
            ).first
        ).to_be_visible(timeout=10000)

        # Verify the selected weekdays displayed on the route card.
        expect(
            page.get_by_text(
                "Runs every Monday, Tuesday, Wednesday",
                exact=False,
            ).first

        ).to_be_visible(timeout=10000)

        # Verify the route notes if they are displayed on the card.
        # The notes may only be visible when opening the route details.
        assert details["name"] == "Urgent"
        assert details["schedule"] == "Weekly Route"
        assert details["notes"] == "Immediate route"

    def test_edit_saved_urgent_route(self, logged_in_page):
        route_page = RoutePage(logged_in_page)

        dialog = route_page.open_edit_route("Urgent")

        # Verify the existing route details.
        expect(
            dialog.get_by_role(
                "textbox", name="Route name", exact=True
            )
        ).to_have_value("Urgent")

        expect(
            dialog.get_by_role(
                "combobox", name="Route schedule", exact=True
            )
        ).to_contain_text("Weekly Route")

        # Close the dialog so this test leaves the page clean.
        dialog.get_by_role(
            "button", name="Cancel", exact=True
        ).click()

        expect(dialog).not_to_be_visible()

    def test_update_route_name_to_urgent_visit(self, logged_in_page):
        route_page = RoutePage(logged_in_page)

        # Open the saved route for editing.
        # Use the route's current name in your test environment.
        dialog = route_page.open_edit_route("Urgent")

        # Update the route name.
        route_name_field = dialog.get_by_role(
            "textbox",
            name="Route name",
            exact=True,
        )
        route_name_field.fill("Urgent Visit")

        expect(route_name_field).to_have_value("Urgent Visit")

        # Save the changes.
        update_button = dialog.get_by_role(
            "button",
            name="Update route",
            exact=True,
        )
        expect(update_button).to_be_enabled()
        update_button.click()

        # Wait for the edit dialog to close.
        expect(dialog).not_to_be_visible(timeout=15000)

        # Verify that the route detail page has loaded.
        start_route_button = logged_in_page.get_by_role(
            "button",
            name="Start Route",
            exact=True,
        )
        expect(start_route_button).to_be_visible(timeout=15000)

        # Verify the updated route schedule/details are visible.
        expect(
            logged_in_page.get_by_text("Route Stops", exact=True)
        ).to_be_visible(timeout=15000)

        # Click Start Route and verify the detail page loads.
        route_page.start_route()

        # Navigate to Field Executive > Route.
        route_page.return_to_route_page()

    def test_delete_urgent_visit_route(self, logged_in_page):
        route_page = RoutePage(logged_in_page)

        route_page.navigate_to_route()
        route_page.delete_route("Urgent Visit")