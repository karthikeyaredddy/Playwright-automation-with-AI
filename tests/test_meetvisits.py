import pytest
from urllib.parse import urlsplit

from pages.field_meets_visits_page import FieldExecutivePage


@pytest.fixture(scope="session")
def meet_visits_page(logged_in_page):
    base_url = urlsplit(logged_in_page.url)
    origin = f"{base_url.scheme}://{base_url.netloc}"
    logged_in_page.context.grant_permissions(
        ["camera", "geolocation", "microphone"],
        origin=origin,
    )
    logged_in_page.context.set_geolocation(
        {
            "latitude": 12.9239542,
            "longitude": 77.6716266,
        }
    )
    return logged_in_page

@pytest.mark.order(8)
class TestMeetsAndVisits:

    # ---------------------------------------------------------
    # TEST 1: OPEN MY ATTENDANCE
    # ---------------------------------------------------------
    def test_open_my_attendance(self, meet_visits_page):
        field_page = FieldExecutivePage(meet_visits_page)

        field_page.open_my_attendance()

        # The 5-second wait is required before checking attendance
        # button visibility in the combined attendance workflow.
        print("PASS: My Attendance page opened successfully.")

    # ---------------------------------------------------------
    # TEST 2: ATTENDANCE CONDITION + OPEN MEETS & VISITS
    # ---------------------------------------------------------
    def test_check_in(self, meet_visits_page):
        field_page = FieldExecutivePage(meet_visits_page)

        # The page object handles the 5000 ms wait, checks the
        # visible attendance button, and navigates to Meets & Visits.
        field_page.run_attendance_or_visits_flow()

        print(
            "PASS: Attendance condition handled and "
            "Meets & Visits workflow started."
        )

    # ---------------------------------------------------------
    # TEST 3: OPEN MEETS & VISITS
    # ---------------------------------------------------------
    def test_open_meets_and_visits_page(self, meet_visits_page):
        field_page = FieldExecutivePage(meet_visits_page)

        field_page.open_meets_and_visits()
        field_page.verify_meets_and_visits_page()

        print("PASS: Meets & Visits page opened successfully.")

    # ---------------------------------------------------------
    # TEST 4: PARTNER SEARCH
    # ---------------------------------------------------------
    def test_partner_search(self, meet_visits_page):
        field_page = FieldExecutivePage(meet_visits_page)

        field_page.open_meets_and_visits()
        field_page.test_partner_search()

        print("PASS: Partner search test completed.")

    # ---------------------------------------------------------
    # TEST 5: RANDOM PARTNER VISIT / MEETING
    # ---------------------------------------------------------
    def test_begin_visit_or_meeting_for_random_partner(
        self,
        meet_visits_page,
    ):
        field_page = FieldExecutivePage(meet_visits_page)

        field_page.open_meets_and_visits()

        selected_partner = (
            field_page.select_random_partner_and_begin_visit()
        )

        assert selected_partner, (
            "No partner was selected for the visit or meeting."
        )

        print(
            f"PASS: Visit or meeting opened for "
            f"'{selected_partner}'."
        )
