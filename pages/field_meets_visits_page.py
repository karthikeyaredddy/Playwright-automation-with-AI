import random
import re

from playwright.sync_api import (
    expect,
    TimeoutError as PlaywrightTimeoutError,
)

from locators.field_meets_and_visits_locators import (
    FieldMeetsAndVisitsLocators,
)


class FieldExecutivePage:

    def __init__(self, page):
        self.page = page
        self.locators = FieldMeetsAndVisitsLocators

    # ---------------------------------------------------------
    # COMMON LOCATORS
    # ---------------------------------------------------------

    def _button(self, name):
        return self.page.get_by_role(
            "button",
            name=name,
            exact=True,
        )

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def open_field_executive_menu(self):
        """Open the submenu only when its items are not visible."""

        attendance_menu = self.page.get_by_role(
            "button",
            name=self.locators.MY_ATTENDANCE_MENU,
            exact=True,
        )

        visits_menu = self.page.get_by_role(
            "button",
            name=self.locators.MEETS_AND_VISITS_MENU,
            exact=True,
        )

        # Do not use attendance_menu.or_(visits_menu).
        # Both items can be visible at the same time.
        if attendance_menu.is_visible() or visits_menu.is_visible():
            print("INFO: Field Executive submenu is already open.")
            return

        field_menu = self.page.get_by_role(
            "button",
            name=self.locators.FIELD_EXECUTIVE_MENU,
            exact=True,
        )

        expect(field_menu).to_be_visible(timeout=15000)
        field_menu.click()

        # Wait for either submenu item without combining locators.
        expect(
            self.page.get_by_role(
                "button",
                name=self.locators.MY_ATTENDANCE_MENU,
                exact=True,
            )
        ).to_be_visible(timeout=15000)

        print("PASS: Field Executive submenu is open.")

    def open_my_attendance(self):
        """
        Navigate to My Attendance and wait for the main
        attendance content to appear.
        """

        attendance_url = re.compile(
            r".*/dashboard/field-executive/attendance/?$"
        )

        if attendance_url.search(self.page.url):
            self.verify_my_attendance_page()
            print("INFO: Already on My Attendance.")
            return

        attendance_menu = self._button(
            self.locators.MY_ATTENDANCE_MENU
        )

        if not attendance_menu.is_visible():
            self.open_field_executive_menu()

        expect(attendance_menu).to_be_visible(timeout=15000)
        attendance_menu.click()

        expect(self.page).to_have_url(
            attendance_url,
            timeout=20000,
        )

        self.verify_my_attendance_page()

        print("PASS: Navigated to My Attendance.")

    def navigate_to_my_attendance(self):
        """
        Compatibility method for existing tests.
        """
        self.open_my_attendance()

    def open_meets_and_visits(self):
        """
        Navigate to Meeting & Visits using the existing
        Field Executive sidebar.
        """

        visits_url = re.compile(
            r".*/dashboard/field-executive/meetings-visits/?$"
        )

        if visits_url.search(self.page.url):
            self.verify_meets_and_visits_page()
            print("INFO: Already on Meets & Visits.")
            return

        visits_menu = self._button(
            self.locators.MEETS_AND_VISITS_MENU
        )

        if not visits_menu.is_visible():
            self.open_field_executive_menu()

        expect(visits_menu).to_be_visible(timeout=15000)
        visits_menu.click()

        expect(self.page).to_have_url(
            visits_url,
            timeout=20000,
        )

        self.verify_meets_and_visits_page()

        print("PASS: Navigated to Meets & Visits.")

    # ---------------------------------------------------------
    # MY ATTENDANCE PAGE VERIFICATION
    # ---------------------------------------------------------

    def verify_my_attendance_page(self):
        """
        Wait for the actual Attendance page content before
        checking any attendance action buttons.
        """

        attendance_heading = self.page.get_by_role(
            "heading",
            name=re.compile(
                r"Let.s Track Your Attendance!",
                re.IGNORECASE,
            ),
        )

        expect(attendance_heading).to_be_visible(timeout=30000)

        attendance_status = self.page.get_by_role(
            "heading",
            name=re.compile(
                r"Attendance Status & Clock In",
                re.IGNORECASE,
            ),
        )

        expect(attendance_status).to_be_visible(timeout=30000)

        # The page content is now present. Wait for the browser's
        # current navigation/rendering work to settle.
        self.page.wait_for_load_state("domcontentloaded")

        print("PASS: My Attendance page has loaded.")
    # ---------------------------------------------------------
    # ATTENDANCE STATE DETECTION
    # ---------------------------------------------------------

    def is_choose_transport_visible(self):
        return self._button(
            self.locators.CHOOSE_TRANSPORT_BUTTON
        ).is_visible()

    def is_check_in_visible(self):
        return self._button(
            self.locators.CHECK_IN_BUTTON
        ).is_visible()

    def is_check_out_visible(self):
        return self._button(
            self.locators.CHECK_OUT_BUTTON
        ).is_visible()

    def get_attendance_state(self):
        """
        Detect the current attendance state using visible buttons.

        Priority:
        1. Check Out visible: already checked in; skip attendance actions.
        2. Choose transport visible: run transport and check-in workflow.
        3. Check In visible: run the existing check-in workflow.
        """

        check_out = self.page.get_by_role(
            "button",
            name=re.compile(r"^\s*check\s*out\s*$", re.IGNORECASE),
            exact=True,
        )

        choose_transport = self.page.get_by_role(
            "button",
            name=re.compile(r"^\s*choose\s*transport\s*$", re.IGNORECASE),
            exact=True,
        )

        check_in = self.page.get_by_role(
            "button",
            name=re.compile(r"^\s*check\s*in\s*$", re.IGNORECASE),
            exact=True,
        )

        # Check Out must take priority: do not perform attendance actions
        # when the user is already checked in.
        if check_out.is_visible():
            print("INFO: Check Out is visible.")
            return "checked_in"

        if choose_transport.is_visible():
            print("INFO: Choose transport button is visible.")
            return "choose_transport"

        if check_in.is_visible():
            print("INFO: Check In button is visible.")
            return "check_in"

        buttons = self.page.locator("button").evaluate_all(
            """elements => elements
                .filter(element => {
                    const style = window.getComputedStyle(element);
                    return style.display !== "none"
                        && style.visibility !== "hidden";
                })
                .map(element => element.innerText.trim())
                .filter(Boolean)"""
        )

        raise AssertionError(
            "Unable to identify the attendance state. "
            f"Visible buttons: {buttons}"
        )

    def run_attendance_or_visits_flow(self):
        """
        Open My Attendance, wait 5 seconds, detect the visible button,
        handle attendance if needed, and navigate to Meets & Visits.
        """

        # Step 1: Open My Attendance using the existing navigation method.
        self.open_my_attendance()

        # Step 2: Always wait 5000 ms before checking button visibility.
        print("INFO: Waiting 5000 ms for My Attendance to load...")
        self.page.wait_for_timeout(5000)

        # Step 3: Determine the current attendance state.
        state = self.get_attendance_state()
        print(f"INFO: Attendance state after wait: {state}")

        if state == "checked_in":
            # Check Out is visible, so attendance is already active.
            # Do not click Check Out or perform any attendance actions.
            print(
                "INFO: Check Out is visible. "
                "Skipping transport selection, check-in, and selfie capture."
            )

        elif state == "choose_transport":
            print(
                "INFO: Choose transport is visible. "
                "Starting the attendance workflow."
            )

            # Re-check the state immediately before attempting transport
            # selection in case the application updated after the first check.
            latest_state = self.get_attendance_state()

            if latest_state == "checked_in":
                print(
                    "INFO: Check Out appeared before transport selection. "
                    "Skipping the remaining attendance actions."
                )

            else:
                if latest_state == "choose_transport":
                    vehicle = self.select_random_transport_and_confirm()

                    # The selection method may return None if the UI changed.
                    if not vehicle:
                        latest_state = self.get_attendance_state()

                        if latest_state != "checked_in":
                            raise AssertionError(
                                "Transport selection did not complete, "
                                "and Check Out is not visible."
                            )

                        print(
                            "INFO: Attendance state changed to checked in. "
                            "Skipping further attendance actions."
                        )

                else:
                    vehicle = None

                # Continue only when the transport workflow returned a vehicle.
                if vehicle:
                    print("INFO: Confirmed transport selection.")
                    self.complete_check_in()

        elif state == "check_in":
            # Fallback for the state where Check In is visible directly.
            # Do not select transport unless Choose transport is visible.
            print(
                "INFO: Check In is visible. "
                "Running the existing check-in and selfie workflow."
            )
            self.complete_check_in()

        else:
            raise AssertionError(
                f"Unexpected attendance state: {state}"
            )

        # Step 4: Continue to Meets & Visits in all successful branches.
        self.open_meets_and_visits()
        self.verify_meets_and_visits_page()

        print(
            "PASS: Attendance state handled and Meets & Visits opened."
        )

    # ---------------------------------------------------------
    # TRANSPORT SELECTION
    # ---------------------------------------------------------

    def select_random_transport_and_confirm(self):
        """Select and confirm a random transport, if still required."""

        # Check the current UI before attempting to click Choose transport.
        state = self.get_attendance_state()

        if state == "checked_in":
            print(
                "INFO: Check Out is visible. "
                "Skipping transport selection."
            )
            return None

        if state != "choose_transport":
            print(
                f"INFO: Transport selection is not required. "
                f"Current state: {state}"
            )
            return None

        choose_transport = self.page.get_by_role(
            "button",
            name=re.compile(
                r"^\s*choose\s*transport\s*$",
                re.IGNORECASE,
            ),
            exact=True,
        )

        expect(choose_transport).to_be_visible(timeout=15000)
        expect(choose_transport).to_be_enabled(timeout=10000)
        choose_transport.click(timeout=15000)

        transport_dialog = self.page.get_by_role("dialog").filter(
            has_text=self.locators.TRANSPORT_POPUP_HEADING,
        )
        expect(transport_dialog).to_be_visible(timeout=15000)

        transport_dropdown = transport_dialog.get_by_role("combobox")
        expect(transport_dropdown).to_be_visible(timeout=10000)
        transport_dropdown.click()

        options = self.page.get_by_role("option")
        expect(options.first).to_be_visible(timeout=10000)

        available_options = [
            options.nth(index)
            for index in range(options.count())
            if options.nth(index).is_visible()
            and options.nth(index).is_enabled()
        ]

        if not available_options:
            option_labels = [
                options.nth(index).inner_text().strip()
                for index in range(options.count())
            ]
            self.page.keyboard.press("Escape")
            close_button = transport_dialog.get_by_role("button").first
            if close_button.is_visible():
                close_button.click()
            expect(transport_dialog).to_be_hidden(timeout=10000)
            raise AssertionError(
                "No selectable transport modes are configured. "
                f"Available options: {option_labels}"
            )

        selected_option = random.choice(available_options)
        selected_vehicle = selected_option.inner_text().strip()
        selected_option.click()

        confirm_button = transport_dialog.get_by_role(
            "button",
            name=self.locators.CONFIRM_SELECTION_BUTTON,
            exact=True,
        )
        expect(confirm_button).to_be_visible(timeout=10000)
        expect(confirm_button).to_be_enabled(timeout=10000)
        confirm_button.click()

        expect(transport_dialog).to_be_hidden(timeout=15000)
        expect(
            self.page.get_by_role(
                "button",
                name=re.compile(r"^\s*check\s*in\s*$", re.IGNORECASE),
                exact=True,
            )
        ).to_be_visible(timeout=15000)

        return selected_vehicle

    # ---------------------------------------------------------
    # CHECK-IN
    # ---------------------------------------------------------

    def click_check_in(self):
        """
        Click Check In only when it is visible and enabled.
        """

        check_in = self._button(
            self.locators.CHECK_IN_BUTTON
        )

        expect(check_in).to_be_visible(timeout=15000)
        expect(check_in).to_be_enabled(timeout=10000)

        check_in.click(force=True)

        print("PASS: Clicked Check In.")

    # ---------------------------------------------------------
    # SELFIE AND CAPTURED PHOTO
    # ---------------------------------------------------------

    def capture_selfie(self):
        """
        Capture the selfie and confirm it using the exact
        controls shown in the supplied screenshots.
        """

        selfie_dialog = self.page.get_by_role(
            "dialog"
        ).filter(
            has=self.page.get_by_role(
                "heading",
                name=self.locators.TAKE_SELFIE_DIALOG,
                exact=True,
            )
        )

        expect(selfie_dialog).to_be_visible(timeout=20000)

        expect(
            selfie_dialog.get_by_role(
                "heading",
                name=self.locators.TAKE_SELFIE_DIALOG,
                exact=True,
            )
        ).to_be_visible(timeout=10000)

        # Step 1: Click Capture Photo.
        capture_button = selfie_dialog.get_by_role(
            "button",
            name=self.locators.CAPTURE_PHOTO_BUTTON,
            exact=True,
        )

        expect(capture_button).to_be_visible(timeout=15000)
        expect(capture_button).to_be_enabled(timeout=10000)

        capture_button.click(force=True)

        # Step 2: Wait for the actual captured image.
        # This locator comes from the supplied DOM screenshot:
        # <img alt="Captured selfie" ...>
        captured_photo = selfie_dialog.locator(
            self.locators.CAPTURED_PHOTO_PREVIEW
        )

        expect(captured_photo).to_be_visible(timeout=20000)

        # Confirm the image has finished loading.
        self.page.wait_for_function(
            """() => {
                const dialog = Array.from(
                    document.querySelectorAll('[role="dialog"]')
                ).find(element =>
                    element.innerText.includes('Take Selfie')
                );

                if (!dialog) {
                    return false;
                }

                const image = dialog.querySelector(
                    'img[alt="Captured selfie"]'
                );

                return Boolean(
                    image &&
                    image.complete &&
                    image.naturalWidth > 0 &&
                    image.naturalHeight > 0
                );
            }""",
            timeout=20000,
        )

        # Step 3: Confirm & Continue.
        confirm_button = selfie_dialog.get_by_role(
            "button",
            name=self.locators.CONFIRM_CONTINUE_BUTTON,
            exact=True,
        )

        expect(confirm_button).to_be_visible(timeout=10000)
        expect(confirm_button).to_be_enabled(timeout=10000)

        confirm_button.click(force=True)

        # Step 4: Wait for the selfie dialog to close.
        expect(selfie_dialog).to_be_hidden(timeout=20000)

        print(
            "PASS: Captured selfie loaded and "
            "Confirm & Continue was clicked."
        )

    def complete_check_in(self):
        """
        Complete the check-in action and confirm that the
        account reaches the checked-in state.
        """

        self.click_check_in()
        self.capture_selfie()

        check_out = self._button(
            self.locators.CHECK_OUT_BUTTON
        )

        expect(check_out).to_be_visible(timeout=30000)

        print("PASS: Check-in completed successfully.")

    # ---------------------------------------------------------
    # COMBINED ATTENDANCE STATE FLOW
    # ---------------------------------------------------------

    def handle_attendance_state(self):
        """
        Handle Choose Transport, Check In, and Check Out
        according to the current visible application state.
        """

        self.open_my_attendance()

        state = self.get_attendance_state()

        print(f"INFO: Current attendance state: {state}")

        # Scenario B: Check Out is visible.
        # This means the user is already checked in.
        if state == "checked_in":
            print(
                "INFO: Check Out is visible. Skipping transport "
                "selection and check-in."
            )
            return "checked_in"

        # Scenario A: Choose Transport is visible.
        if state == "choose_transport":
            print(
                "INFO: Choose Transport is visible. "
                "Selecting a random vehicle."
            )

            self.select_random_transport_and_confirm()

            # Check the UI again after transport confirmation.
            updated_state = self.get_attendance_state()

            if updated_state == "checked_in":
                print(
                    "INFO: The account is already checked in "
                    "after transport confirmation."
                )
                return "checked_in"

            if updated_state != "check_in":
                raise AssertionError(
                    "Transport was confirmed, but Check In was "
                    "not displayed. "
                    f"Current state: {updated_state}"
                )

            self.complete_check_in()

            return "checked_in"

        # Scenario C: Check In is already visible.
        # Do not select transport again.
        if state == "check_in":
            print(
                "INFO: Check In is visible. Skipping transport "
                "selection and proceeding to check-in."
            )

            self.complete_check_in()

            return "checked_in"

        # An unknown state should not silently pass.
        raise AssertionError(
            "Unable to determine the attendance state. "
            "Expected one of these buttons to be visible: "
            "'Choose transport', 'Check In', or 'Check Out'. "
            "Inspect the current My Attendance page."
        )

    # ---------------------------------------------------------
    # MEETS & VISITS PAGE VERIFICATION
    # ---------------------------------------------------------

    def verify_meets_and_visits_page(self):
        """Verify the Meets & Visits page and partner search field."""

        heading = self.page.get_by_role(
            "heading",
            name=re.compile(
                r"Let's Manage Visits & Meetings!",
                re.IGNORECASE,
            ),
        )
        expect(heading).to_be_visible(timeout=20000)

        expect(
            self.page.get_by_role(
                "heading",
                name=self.locators.AVAILABLE_PARTNERS_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=15000)

        search_field = self.page.locator(
            self.locators.PARTNER_SEARCH_FIELD
        )
        expect(search_field).to_be_visible(timeout=15000)

        usage_pattern = re.compile(
            self.locators.USAGE_COUNT_PATTERN,
            re.IGNORECASE,
        )
        usage_counter = self.page.get_by_text(usage_pattern).first
        expect(usage_counter).to_be_visible(timeout=30000)

        usage_text = usage_counter.inner_text()
        match = usage_pattern.search(usage_text)
        assert match, (
            "The visits usage counter is visible but could not be parsed: "
            f"{usage_text!r}"
        )

        used_count = int(match.group(1).replace(",", ""))
        total_count = int(match.group(2).replace(",", ""))

        assert total_count > 0, (
            f"The visits usage limit must be greater than zero: {usage_text!r}"
        )
        assert used_count < total_count, (
            f"Visit limit reached: {usage_text.strip()}"
        )

        print(f"INFO: Usage information: {usage_text.strip()}")

        print("PASS: Meets & Visits page verified.")

    # ---------------------------------------------------------
    # PARTNER SEARCH
    # ---------------------------------------------------------

    def get_visible_partner_cards(self):
        """
        Return all partner cards that are currently visible.
        """

        cards = self.page.locator(
            self.locators.PARTNER_CARD
        )

        visible_cards = []

        for index in range(cards.count()):
            card = cards.nth(index)

            if card.is_visible():
                action_buttons = card.get_by_role(
                    "button",
                    name=re.compile(
                        r"Begin Visit(?: or Meeting)?|Begin Meeting",
                        re.IGNORECASE,
                    ),
                )
                if any(
                    action_buttons.nth(button_index).is_visible()
                    and action_buttons.nth(button_index).is_enabled()
                    for button_index in range(action_buttons.count())
                ):
                    visible_cards.append(card)

        return visible_cards

    def get_partner_name(self, card):
        """
        Read the partner name from a partner card.
        """

        name_locator = card.locator("p").first

        expect(name_locator).to_be_visible(timeout=5000)

        partner_name = name_locator.inner_text().strip()

        if not partner_name:
            raise AssertionError(
                "A visible partner card has no readable name."
            )

        return partner_name

    def test_partner_search(self):
        """
        Search for a partner after the partner cards have loaded,
        verify the matching result, and clear the search field.
        """

        self.open_meets_and_visits()

        search_field = self.page.locator(
            self.locators.PARTNER_SEARCH_FIELD
        )

        expect(search_field).to_be_visible(timeout=15000)
        expect(search_field).to_be_enabled(timeout=10000)

        # Wait for the partner list to render.
        cards = self.page.locator(
            self.locators.PARTNER_CARD
        )

        expect(cards.first).to_be_visible(timeout=20000)

        # Read the cards after the wait, not before it.
        visible_cards = self.get_visible_partner_cards()

        if not visible_cards:
            raise AssertionError(
                "No available partners were returned for this account; "
                "partner search cannot be validated."
            )

        # Use a partner name from an actual visible card.
        expected_partner = self.get_partner_name(visible_cards[0])

        print(
            f"INFO: Searching for partner: {expected_partner}"
        )

        search_field.fill(expected_partner)

        # Wait for a matching card to appear after filtering.
        matching_card = cards.filter(
            has_text=expected_partner
        ).first

        expect(matching_card).to_be_visible(timeout=15000)

        actual_partner = self.get_partner_name(matching_card)

        assert actual_partner.casefold() == expected_partner.casefold(), (
            f"Search result mismatch. Expected '{expected_partner}', "
            f"but found '{actual_partner}'."
        )

        print(
            f"PASS: Partner search returned '{actual_partner}'."
        )

        # Clear the search field and verify it is empty.
        search_field.fill("")

        expect(search_field).to_have_value(
            "",
            timeout=5000,
        )

        print("PASS: Partner search field cleared successfully.")

    # ---------------------------------------------------------
    # RANDOM PARTNER AND BEGIN VISIT / MEETING
    # ---------------------------------------------------------

    def select_random_partner_and_begin_visit(self):
        """
        Select a random visible partner with an enabled
        Begin Visit or Begin Meeting button.
        """

        self.open_meets_and_visits()

        cards = self.page.locator(
            self.locators.PARTNER_CARD
        )

        expect(cards.first).to_be_visible(timeout=15000)

        available_partners = []

        action_pattern = re.compile(
            r"Begin Visit(?: or Meeting)?|Begin Meeting",
            re.IGNORECASE,
        )

        for index in range(cards.count()):
            card = cards.nth(index)

            if not card.is_visible():
                continue

            action_buttons = card.get_by_role(
                "button",
                name=action_pattern,
            )

            for button_index in range(action_buttons.count()):
                button = action_buttons.nth(button_index)

                if button.is_visible() and button.is_enabled():
                    partner_name = self.get_partner_name(card)

                    available_partners.append(
                        (button, partner_name)
                    )

        if not available_partners:
            raise AssertionError(
                "No visible partner has an enabled "
                "Begin Visit or Begin Meeting button."
            )

        _, partner_name = random.choice(
            available_partners
        )

        print(
            f"INFO: Selected random partner: {partner_name}"
        )

        search_field = self.page.locator(
            self.locators.PARTNER_SEARCH_FIELD
        )
        expect(search_field).to_be_visible(timeout=10000)
        search_field.fill(partner_name)

        matching_card = cards.filter(
            has=self.page.get_by_text(
                partner_name,
                exact=True,
            )
        ).first
        expect(matching_card).to_be_visible(timeout=15000)

        actual_partner = self.get_partner_name(matching_card)
        assert actual_partner.casefold() == partner_name.casefold(), (
            f"Partner search result mismatch. Expected '{partner_name}', "
            f"but found '{actual_partner}'."
        )

        selected_button = matching_card.get_by_role(
            "button",
            name=action_pattern,
        ).first
        expect(selected_button).to_be_visible(timeout=10000)
        expect(selected_button).to_be_enabled(timeout=10000)
        selected_button.click()

        partner_visit_url = re.compile(
            r".*/dashboard/field-executive/partner-visit/"
            r"[^/?#]+/?$"
        )

        expect(self.page).to_have_url(
            partner_visit_url,
            timeout=20000,
        )

        expect(
            self.page.get_by_role(
                "heading",
                name=self.locators.PARTNER_VISIT_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=20000)

        expect(
            self.page.get_by_text(
                partner_name,
                exact=True,
            ).first
        ).to_be_visible(timeout=15000)

        print(
            f"PASS: Partner Visit page opened for "
            f"'{partner_name}'."
        )

        self.complete_start_visit_workflow()

        return partner_name

    def complete_start_visit_workflow(self):
        """Configure and start a visit, then capture its start selfie."""

        expect(
            self.page.get_by_role(
                "heading",
                name=self.locators.START_INTERACTION_HEADING,
                exact=True,
            )
        ).to_be_visible(timeout=15000)

        notes_field = self.page.get_by_role(
            "textbox",
            name=self.locators.NOTES_FIELD,
            exact=True,
        )
        if notes_field.is_visible():
            print(
                "INFO: Visit is already at Record Notes & Audio; "
                "continuing the active session."
            )
            self.complete_meeting_session()
            return

        capture_start_selfie = self.page.get_by_role(
            "button",
            name=self.locators.CAPTURE_START_SELFIE_BUTTON,
            exact=True,
        )

        if not capture_start_selfie.is_visible():
            interaction_fields = self.page.get_by_role("combobox")
            expect(interaction_fields.nth(0)).to_be_visible(timeout=10000)
            interaction_fields.nth(0).click()

            offline_option = self.page.get_by_role(
                "option",
                name=re.compile(
                    rf"^{re.escape(self.locators.OFFLINE_VISIT_OPTION)}$",
                    re.IGNORECASE,
                ),
            )
            expect(offline_option).to_be_visible(timeout=10000)
            offline_option.click()

            start_button = self.page.get_by_role(
                "button",
                name=self.locators.START_BUTTON,
                exact=True,
            )

            if (
                interaction_fields.count() > 1
                and interaction_fields.nth(1).is_visible()
            ):
                interaction_fields.nth(1).click()
                purpose_options = self.page.get_by_role("option")
                expect(purpose_options.first).to_be_visible(timeout=10000)

                available_purposes = []
                for index in range(purpose_options.count()):
                    option = purpose_options.nth(index)
                    purpose = option.inner_text().strip()
                    if (
                        purpose
                        and purpose != self.locators.PURPOSE_PLACEHOLDER
                        and option.is_visible()
                        and option.is_enabled()
                    ):
                        available_purposes.append((option, purpose))

                assert available_purposes, (
                    "No interaction purposes are available in the purpose "
                    "dropdown."
                )

                selected_purpose = random.choice(available_purposes)
                selected_purpose[0].click()
                print(
                    f"INFO: Selected interaction purpose: "
                    f"{selected_purpose[1]}"
                )

            if start_button.is_visible():
                expect(start_button).to_be_enabled(timeout=10000)
                start_button.click()

        expect(capture_start_selfie).to_be_visible(timeout=60000)
        capture_start_selfie.click()

        selfie_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=self.locators.TAKE_SELFIE_HEADING,
                exact=True,
            )
        )
        expect(selfie_dialog).to_be_visible(timeout=20000)

        capture_photo = selfie_dialog.get_by_role(
            "button",
            name=self.locators.CAPTURE_START_PHOTO_BUTTON,
            exact=True,
        )
        expect(capture_photo).to_be_visible(timeout=20000)
        expect(capture_photo).to_be_enabled(timeout=20000)
        capture_photo.click()

        confirm_continue = selfie_dialog.get_by_role(
            "button",
            name=self.locators.CONFIRM_CONTINUE_BUTTON,
            exact=True,
        )
        expect(confirm_continue).to_be_visible(timeout=20000)
        expect(confirm_continue).to_be_enabled(timeout=20000)
        confirm_continue.click()

        expect(selfie_dialog).to_be_hidden(timeout=20000)
        expect(
            self.page.locator(self.locators.ACTIVE_STEP_LABEL)
        ).to_have_text(
            self.locators.NEXT_SESSION_STEP,
            timeout=20000,
        )

        self.complete_meeting_session()

        print(
            "PASS: Visit, recording, summary, end selfie, and session "
            "completion finished successfully."
        )

    def _visible_enabled_button(self, name):
        """Return the sole visible, enabled button with the given name."""
        buttons = self._button(name)
        matches = [
            buttons.nth(index)
            for index in range(buttons.count())
            if buttons.nth(index).is_visible()
        ]
        assert len(matches) == 1, (
            f"Expected one visible '{name}' button, found {len(matches)}."
        )
        expect(matches[0]).to_be_enabled()
        return matches[0]

    def _record_meeting_audio(self):
        start_recording = self._visible_enabled_button(
            self.locators.START_RECORDING_BUTTON
        )
        start_recording.click()

        stop_recording = self._button(
            self.locators.STOP_RECORDING_BUTTON
        )
        expect(stop_recording).to_be_visible(timeout=15000)
        expect(stop_recording).to_be_enabled(timeout=15000)

        # Keep each recording active for the required five seconds.
        self.page.wait_for_timeout(5000)
        stop_recording.click()

        play_recording = self._button(
            self.locators.PLAY_RECORDING_BUTTON
        )
        replace_recording = self._button(
            self.locators.REPLACE_RECORDING_BUTTON
        )
        expect(play_recording).to_be_visible(timeout=20000)
        expect(replace_recording).to_be_visible(timeout=20000)
        expect(replace_recording).to_be_enabled(timeout=20000)

    def complete_meeting_session(self):
        notes = self.page.get_by_role(
            "textbox",
            name=self.locators.NOTES_FIELD,
            exact=True,
        )
        expect(notes).to_be_visible(timeout=20000)
        expect(notes).to_be_enabled(timeout=10000)
        notes.click()
        notes.fill("important meeting")

        self._record_meeting_audio()

        play_recording = self._button(
            self.locators.PLAY_RECORDING_BUTTON
        )
        if play_recording.is_visible() and play_recording.is_enabled():
            play_recording.click()

        replace_recording = self._visible_enabled_button(
            self.locators.REPLACE_RECORDING_BUTTON
        )
        replace_recording.click()

        replace_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=self.locators.REPLACE_RECORDING_DIALOG_HEADING,
                exact=True,
            )
        )
        expect(replace_dialog).to_be_visible(timeout=15000)

        start_new_recording = replace_dialog.get_by_role(
            "button",
            name=self.locators.START_NEW_RECORDING_BUTTON,
            exact=True,
        )
        expect(start_new_recording).to_be_visible(timeout=10000)
        expect(start_new_recording).to_be_enabled(timeout=10000)
        start_new_recording.click()
        expect(replace_dialog).to_be_hidden(timeout=15000)

        stop_recording = self._button(
            self.locators.STOP_RECORDING_BUTTON
        )
        expect(stop_recording).to_be_visible(timeout=15000)
        expect(stop_recording).to_be_enabled(timeout=15000)
        self.page.wait_for_timeout(5000)
        stop_recording.click()

        continue_recording = self._visible_enabled_button("Continue")
        continue_recording.click()

        summary = self.page.get_by_role(
            "textbox",
            name=self.locators.SUMMARY_FIELD,
            exact=True,
        )
        expect(summary).to_be_visible(timeout=20000)
        expect(summary).to_be_enabled(timeout=10000)
        summary.click()
        summary.fill("important information")

        self._visible_enabled_button("Continue").click()

        capture_end_selfie = self._button(
            self.locators.CAPTURE_END_SELFIE_BUTTON
        )
        expect(capture_end_selfie.first).to_be_visible(timeout=30000)
        capture_end_selfie = self._visible_enabled_button(
            self.locators.CAPTURE_END_SELFIE_BUTTON
        )
        capture_end_selfie.click()

        end_selfie_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=self.locators.TAKE_SELFIE_HEADING,
                exact=True,
            )
        )
        expect(end_selfie_dialog).to_be_visible(timeout=20000)

        capture_photo = end_selfie_dialog.get_by_role(
            "button",
            name=self.locators.CAPTURE_START_PHOTO_BUTTON,
            exact=True,
        )
        expect(capture_photo).to_be_visible(timeout=15000)
        expect(capture_photo).to_be_enabled(timeout=15000)
        capture_photo.click()

        confirm_continue = end_selfie_dialog.get_by_role(
            "button",
            name=self.locators.CONFIRM_CONTINUE_BUTTON,
            exact=True,
        )
        expect(confirm_continue).to_be_visible(timeout=15000)
        expect(confirm_continue).to_be_enabled(timeout=15000)
        confirm_continue.click()
        expect(end_selfie_dialog).to_be_hidden(timeout=20000)

        complete_session = self.page.get_by_text(
            self.locators.COMPLETE_SESSION_SECTION,
            exact=True,
        )
        expect(complete_session).to_be_visible(timeout=20000)
        self._visible_enabled_button("Continue").click()

        completed_dialog = self.page.get_by_role("dialog").filter(
            has=self.page.get_by_role(
                "heading",
                name=self.locators.MEETING_COMPLETED_HEADING,
                exact=True,
            )
        )
        expect(completed_dialog).to_be_visible(timeout=30000)

        close_button = completed_dialog.get_by_role(
            "button",
            name=self.locators.CLOSE_BUTTON,
            exact=True,
        )
        expect(close_button).to_be_visible(timeout=10000)
        expect(close_button).to_be_enabled(timeout=10000)
        close_button.click()
        expect(completed_dialog).to_be_hidden(timeout=15000)