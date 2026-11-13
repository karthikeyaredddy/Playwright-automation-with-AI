import pytest
from pages.fieldexecutivedashboard_page import (
    FieldExecutiveDashboardPage
)


@pytest.mark.order(2)
class TestFieldExecutiveDashboard:

    def test_dashboard_heading(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        fe.open_field_executive_dashboard()

        assert fe.verify_dashboard_heading()

    def test_greeting_section(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_greeting_section()

    def test_dashboard_cards(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_visits_today()
        assert fe.verify_orders_today()
        assert fe.verify_revenue_today()

    def test_today_work_plan(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_today_work_plan()

    def test_revenue_section(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_revenue_section()

    def test_performance_section(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_performance_section()

    def test_interaction_insights(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_interaction_insights()

    def test_quick_actions(self, logged_in_page):
        fe = FieldExecutiveDashboardPage(logged_in_page)

        assert fe.verify_quick_actions_button()