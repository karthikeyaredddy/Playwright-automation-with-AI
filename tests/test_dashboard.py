import pytest
from pages.dashboard_page import DashboardPage

@pytest.mark.order(1)
class TestDashboard:

    #logo

    def test_logo_visible(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_logo_visible()


    def test_sidebar_lock_toggle(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_sidebar_lock_toggle()

    def test_admin_button_working(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_admin_button_working()

    def test_my_profile_working(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_my_profile()

    # def test_change_password_working(self, logged_in_page):
    #     dashboard = DashboardPage(logged_in_page)
    #
    #     assert dashboard.verify_change_password()

    def test_logout_popup_working(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_logout_popup()


    def test_account_settings_working(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_account_settings()



