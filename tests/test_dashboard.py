from pages.dashboard_page import DashboardPage


class TestDashboard:

    #logo

    def test_logo_visible(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_logo_visible()


class TestSidebar:

    def test_sidebar_collapsed(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_sidebar_collapsed()
class TestAdminMenu:

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
class TestLogout:

    def test_logout_popup_working(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_logout_popup()

class TestAccountSettings:

    def test_account_settings_working(self, logged_in_page):

        dashboard = DashboardPage(logged_in_page)

        assert dashboard.verify_account_settings()




