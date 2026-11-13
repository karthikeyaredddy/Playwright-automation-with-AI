import re
from datetime import date, timedelta
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError, Page
from locators.route_locators import RouteLocators

class RoutePage:
    ROUTE_URL = (
        "https://ayksadev-adminportal.onrender.com/"
        "dashboard/field-executive/route"
    )

    def __init__(self, page: Page):
        self.page = page

        self.field_executive_menu = page.get_by_role(
            "button",
            name=RouteLocators.FIELD_EXECUTIVE_MENU,
            exact=True,
        )

        # The sidebar submenu item
        self.route_menu = page.get_by_role(
            "button",
            name=RouteLocators.ROUTE_MENU,
            exact=True,
        )

        self.month_filter = page.get_by_role(
            "button",
            name=RouteLocators.MONTH_FILTER_PATTERN,
        )

        self.create_route_button = page.get_by_role(
            "button",
            name=RouteLocators.CREATE_ROUTE_BUTTON,
            exact=True,
        )

        self.nearby_partners_heading = page.get_by_text(
            RouteLocators.NEARBY_PARTNERS_HEADING,
            exact=True,
        )

        self.add_partner_buttons = page.get_by_role(
            "button",
            name=RouteLocators.ADD_PARTNER_BUTTON_PATTERN,
        )

        self.confirm_selection_button = page.get_by_role(
            "button",
            name=RouteLocators.CONFIRM_SELECTION_BUTTON_PATTERN,
        )

    def open_field_executive_menu(self):
        """Expand Field Executive and wait for the Route submenu."""

        expect(self.field_executive_menu).to_be_visible(timeout=10000)

        # Expand only if Route is not already visible.
        if not self.route_menu.is_visible():
            self.field_executive_menu.click()

        expect(self.route_menu).to_be_visible(timeout=10000)

    def navigate_to_route(self):
        """Navigate through Field Executive > Route."""

        route_url = self.ROUTE_URL.rstrip("/")

        if self.page.url.rstrip("/") != route_url:
            self.open_field_executive_menu()
            self.route_menu.click()

            self.page.wait_for_url(
                "**/dashboard/field-executive/route",
                timeout=15000,
            )

        expect(self.page).to_have_url(route_url, timeout=15000)

        expect(
            self.page.get_by_text("My Routes", exact=True)
        ).to_be_visible(timeout=10000)

    def verify_month_filter_visible(self):
        """Verify the monthly filter is visible."""

        expect(self.month_filter).to_be_visible(timeout=10000)

    def get_selected_month(self):
        """Read the month currently displayed."""

        self.verify_month_filter_visible()
        return self.month_filter.inner_text().strip()

    def open_month_filter(self):
        """Open the month selector."""

        self.verify_month_filter_visible()
        self.month_filter.click()

    def close_month_filter(self):
        """Close the month selector if it is open."""

        self.page.keyboard.press("Escape")


    def click_create_route(self):
        """Open the Create Route page and wait for it to load."""

        expect(
            self.create_route_button
        ).to_be_visible(timeout=10000)

        self.create_route_button.click()

        expect(self.page).to_have_url(
            re.compile(r"/dashboard/field-executive/route/create/?$")
        )

        expect(
            self.nearby_partners_heading
        ).to_be_visible(timeout=15000)

    def select_two_nearby_partners(self):
        """Select two distinct nearby partners."""

        expect(
            self.nearby_partners_heading
        ).to_be_visible(timeout=15000)

        buttons = self.add_partner_buttons

        expect(buttons.first).to_be_visible(timeout=10000)

        if buttons.count() < 2:
            raise AssertionError(
                "At least two nearby partners must be available."
            )

        # Select the first available partner.
        buttons.first.click()

        # Wait for the available list to update, then select another.
        expect(buttons.first).to_be_visible(timeout=10000)
        buttons.first.click()

        # The UI should show that two partners are selected.
        expect(
            self.page.get_by_text("2 selected", exact=True)
        ).to_be_visible(timeout=10000)

        expect(
            self.confirm_selection_button
        ).to_be_enabled(timeout=10000)

    def confirm_partner_selection(self):
        """Confirm selection and wait for the schedule popup."""

        expect(
            self.confirm_selection_button
        ).to_be_enabled(timeout=10000)

        self.confirm_selection_button.click()

        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=15000)

        expect(
            dialog.get_by_text(
                RouteLocators.PLAN_ROUTE_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

    def verify_two_route_stops(self):
        """Verify the two selected partners are shown in Route Stops."""

        expect(
            self.page.get_by_text("Route Stops", exact=True)
        ).to_be_visible()

        expect(
            self.page.get_by_text("2 selected", exact=True)
        ).to_be_visible(timeout=10000)

    def fill_route_schedule_form(self):
        """Fill and validate the route schedule popup after partner confirmation."""

        # Wait for the popup to open after Confirm.
        dialog = self.page.get_by_role(
            "dialog", name="Plan route schedule"
        )
        expect(dialog).to_be_visible(timeout=15000)

        # 1. Route Name
        route_name = dialog.get_by_role(
            "textbox", name="Route name", exact=True
        )
        route_name.click()
        route_name.fill("Urgent")

        # 2. Route Schedule: select Weekly Route only.
        schedule = dialog.get_by_role(
            "combobox", name="Route schedule", exact=True
        )
        schedule.click()

        weekly_option = self.page.get_by_role(
            "option", name="Weekly Route", exact=True
        )
        expect(weekly_option).to_be_visible(timeout=5000)
        weekly_option.click()

        # Verify the selected schedule.
        expect(schedule).to_contain_text("Weekly Route")

        # 3. Effective From: tomorrow.
        tomorrow = date.today() + timedelta(days=1)
        from_text = tomorrow.strftime("%Y-%m-%d")

        effective_from = dialog.get_by_role(
            "textbox", name="Effective from", exact=True
        )
        effective_from.click()
        effective_from.fill(from_text)

        # 4. Select No End Date, then deselect it.
        no_end_date = dialog.get_by_role(
            "checkbox", name="No end date", exact=True
        )

        if not no_end_date.is_checked():
            no_end_date.check()

        expect(no_end_date).to_be_checked()

        no_end_date.uncheck()
        expect(no_end_date).not_to_be_checked()

        # 5. Effective Until: two days after Effective From.
        until_date = tomorrow + timedelta(days=2)
        until_text = until_date.strftime("%Y-%m-%d")

        effective_until = dialog.get_by_role(
            "textbox", name="Effective until", exact=True
        )
        effective_until.click()
        effective_until.fill(until_text)

        # 6. Select three days, excluding Sunday.
        selected_days = ["Mon", "Tue", "Wed"]

        for day in selected_days:
            day_checkbox = dialog.get_by_role(
                "checkbox", name=day, exact=True
            )
            expect(day_checkbox).to_be_enabled(timeout=5000)

            if not day_checkbox.is_checked():
                day_checkbox.check()

            expect(day_checkbox).to_be_checked()

        # 7. Route Notes
        notes = dialog.get_by_role(
            "textbox", name="Route notes", exact=True
        )
        notes.click()
        notes.fill("Immediate route")

        # Validate all entered values before saving.
        expect(route_name).to_have_value("Urgent")
        expect(effective_from).to_have_value(from_text)
        expect(effective_until).to_have_value(until_text)
        expect(no_end_date).not_to_be_checked()
        expect(notes).to_have_value("Immediate route")

        for day in selected_days:
            expect(
                dialog.get_by_role("checkbox", name=day, exact=True)
            ).to_be_checked()

        return {
            "name": "Urgent",
            "schedule": "Weekly Route",
            "effective_from": from_text,
            "effective_until": until_text,
            "days": selected_days,
            "notes": "Immediate route",
        }

    def close_schedule_dialog_if_open(self):
        """Close the schedule dialog if the fixture opens on an existing form."""
        dialog = self.page.get_by_role("dialog", name="Plan route schedule")

        if dialog.is_visible():
            cancel_button = dialog.get_by_role(
                "button", name="Cancel", exact=True
            )
            cancel_button.click()
            expect(dialog).to_be_hidden(timeout=5000)

    def save_route_schedule(self):
        """Save the route and wait for the popup to close."""

        dialog = self.page.get_by_role(
            "dialog", name="Plan route schedule"
        )

        save_button = dialog.get_by_role(
            "button", name="Save route", exact=True
        )

        expect(save_button).to_be_enabled(timeout=5000)
        save_button.click()

        expect(dialog).to_be_hidden(timeout=15000)

    def open_edit_route(self, route_name="Urgent"):
        """Open an existing route and display its edit schedule dialog."""

        # Navigate to the route list first.
        self.navigate_to_route()

        # Locate the saved route.
        route_name_locator = self.page.get_by_text(
            route_name, exact=True
        ).first
        expect(route_name_locator).to_be_visible(timeout=15000)

        # Locate the route card containing the route name.
        route_card = self.page.locator(
            "div.MuiCard-root"
        ).filter(has=route_name_locator).first

        # Open route options.
        options_button = route_card.get_by_role(
            "button", name="Route options", exact=True
        )
        expect(options_button).to_be_visible(timeout=5000)
        options_button.click()

        # Choose Edit route.
        edit_option = self.page.get_by_role(
            "menuitem", name="Edit route", exact=True
        )
        expect(edit_option).to_be_visible(timeout=5000)
        edit_option.click()

        # Wait for the existing stops page.
        expect(
            self.page.get_by_text("Route Stops", exact=True)
        ).to_be_visible(timeout=15000)

        # The selected stops are already present.
        # Click the actual button accessible name from the page.
        confirm_button = self.page.get_by_role(
            "button",
            name="Save route changes",
            exact=True,
        )
        expect(confirm_button).to_be_visible(timeout=10000)
        expect(confirm_button).to_be_enabled()
        confirm_button.click()

        # Editing opens "Edit route schedule", not "Plan route schedule".
        dialog = self.page.get_by_role(
            "dialog", name="Edit route schedule", exact=True
        )
        expect(dialog).to_be_visible(timeout=15000)

        expect(
            dialog.get_by_role(
                "heading",
                name="Edit route schedule",
                exact=True,
            )
        ).to_be_visible()

        return dialog

    def update_route_name(self, new_route_name="Urgent visit"):
        """Update the route name and save the edited route."""

        dialog = self.page.get_by_role(
            "dialog", name="Edit route schedule"
        )
        expect(dialog).to_be_visible(timeout=10000)

        route_name_input = dialog.get_by_role(
            "textbox", name="Route name", exact=True
        )
        route_name_input.fill(new_route_name)
        expect(route_name_input).to_have_value(new_route_name)

        # Accessible name is 'Update route', with a lowercase r.
        update_button = dialog.get_by_role(
            "button",
            name=RouteLocators.UPDATE_ROUTE_BUTTON,
            exact=True,
        )

        expect(update_button).to_be_visible(timeout=5000)
        expect(update_button).to_be_enabled(timeout=5000)
        update_button.click()

        # Wait for the schedule dialog to close.
        expect(dialog).to_be_hidden(timeout=15000)

        # Verify that the updated route appears in My Routes.
        expect(
            self.page.get_by_text("My Routes", exact=True)
        ).to_be_visible(timeout=15000)

        updated_route = self.page.get_by_text(
            new_route_name, exact=True
        ).first
        expect(updated_route).to_be_visible(timeout=15000)

    def start_route(self):
        """Start the saved route and verify the route detail page remains loaded."""

        start_route_button = self.page.get_by_role(
            "button",
            name="Start Route",
            exact=True,
        )

        expect(start_route_button).to_be_visible(timeout=15000)
        expect(start_route_button).to_be_enabled()
        start_route_button.click()

        # Wait for the page to finish its navigation, if any.
        self.page.wait_for_load_state(
            "domcontentloaded",
            timeout=15000,
        )

        # Verify that the route detail page is still displayed.
        expect(
            self.page.get_by_text("Route Stops", exact=True)
        ).to_be_visible(timeout=15000)

        print("Route started and route detail page loaded successfully.")

    def return_to_route_page(self):
        """Open Field Executive > Route and verify the Route page loads."""

        self.navigate_to_route()

        expect(
            self.page.get_by_text("My Routes", exact=True)
        ).to_be_visible(timeout=15000)

        print("Field Executive > Route page loaded successfully.")

    def delete_route(self, route_name="Urgent Visit"):
        """Delete a route using its Route options menu."""

        # Find the route name and its containing card.
        route_name_locator = self.page.get_by_text(
            route_name,
            exact=True,
        ).first

        expect(route_name_locator).to_be_visible(timeout=15000)

        # Locate the nearest route-card container.
        route_card = self.page.locator(
            "div.MuiCard-root"
        ).filter(
            has=route_name_locator
        ).first

        # Click the three-dot Route options button.
        options_button = route_card.get_by_role(
            "button",
            name="Route options",
            exact=True,
        )

        expect(options_button).to_be_visible(timeout=10000)
        options_button.click()

        # Click Delete route in the opened menu.
        delete_option = self.page.get_by_role(
            "menuitem",
            name="Delete route",
            exact=True,
        )

        expect(delete_option).to_be_visible(timeout=5000)
        delete_option.click()

        # Handle a confirmation dialog if the application displays one.
        dialog = self.page.get_by_role("dialog")

        if dialog.count() > 0 and dialog.is_visible():
            confirm_button = dialog.get_by_role(
                "button",
                name=re.compile(r"^(Delete|Confirm|Yes|Delete route)$", re.I),
            )

            expect(confirm_button.first).to_be_visible(timeout=5000)
            confirm_button.first.click()

        # Verify that the selected route has been removed.
        expect(
            route_card
        ).not_to_be_visible(timeout=15000)

        print(f"Route '{route_name}' deleted successfully.")
