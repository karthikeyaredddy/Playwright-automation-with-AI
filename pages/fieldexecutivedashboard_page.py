from playwright.sync_api import expect

from locators.fieldexecutive_locators import FieldExecutiveLocators

class FieldExecutiveDashboardPage:

    def __init__(self, page):
        self.page = page

    def open_field_executive_dashboard(self):
        # Click Field Executive menu
        field_executive = self.page.get_by_role(
            "button",
            name="Field Executive"
        )

        expect(field_executive).to_be_visible(timeout=10000)

        field_executive.click()

        # Click Dashboard submenu
        dashboard = self.page.locator(
            "//span[normalize-space()='Dashboard']"
        ).last

        expect(dashboard).to_be_visible(timeout=10000)

        dashboard.click()

        self.page.wait_for_load_state("networkidle")

    def verify_dashboard_heading(self):
        # Verify URL
        self.page.wait_for_url(
            "**/dashboard/field-executive/dashboard"
        )

        # Verify Dashboard loaded
        expect(
            self.page.get_by_text(
                "Visits Today",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        return True

    def verify_greeting_section(self):
        greeting = self.page.locator(
            FieldExecutiveLocators.GREETING
        )

        current_date = self.page.locator(
            FieldExecutiveLocators.CURRENT_DATE
        ).first

        updated = self.page.locator(
            FieldExecutiveLocators.UPDATED_TEXT
        )

        expect(greeting).to_be_visible(timeout=10000)
        expect(current_date).to_be_visible(timeout=10000)
        expect(updated).to_be_visible(timeout=10000)

        return True

    def verify_visits_today(self):
        visits = self.page.locator(
            FieldExecutiveLocators.VISITS_TODAY
        )

        expect(visits).to_be_visible(timeout=10000)

        return True

    def verify_orders_today(self):
        orders = self.page.locator(
            FieldExecutiveLocators.ORDERS_TODAY
        )

        expect(orders).to_be_visible(timeout=10000)

        return True

    def verify_revenue_today(self):
        revenue = self.page.locator(
            FieldExecutiveLocators.REVENUE_TODAY
        )

        expect(revenue).to_be_visible(timeout=10000)

        return True

    def verify_today_work_plan(self):
        # Today's Work Plan heading
        expect(
            self.page.get_by_text(
                "Today's Work Plan",
                exact=False
            )
        ).to_be_visible(timeout=10000)

        # Planned
        expect(
            self.page.get_by_text(
                "Planned",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Completed
        expect(
            self.page.get_by_text(
                "Completed",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Pending
        expect(
            self.page.get_by_text(
                "Pending",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Missed
        expect(
            self.page.get_by_text(
                "Missed",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Empty state message
        expect(
            self.page.get_by_text(
                "No meets & visits planned today",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Description
        expect(
            self.page.get_by_text(
                "Select a partner from My Partners",
                exact=False
            )
        ).to_be_visible(timeout=10000)

        # Schedule Meet / Visit button
        schedule_btn = self.page.get_by_role(
            "button",
            name="Schedule Meet / Visit →"
        )

        expect(schedule_btn).to_be_visible(timeout=10000)
        expect(schedule_btn).to_be_enabled()

        # Timeline section
        expect(
            self.page.get_by_text(
                "Timeline",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.get_by_text(
                "Nothing on your timeline yet today.",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        return True

    def verify_revenue_section(self):
        expect(
            self.page.get_by_text("Revenue", exact=True)
        ).to_be_visible()

        expect(
            self.page.get_by_text("Last 7 days", exact=True)
        ).to_be_visible()

        # Revenue graph
        expect(
            self.page.locator("svg.recharts-surface").first
        ).to_be_visible()

        # Revenue insight
        expect(
            self.page.get_by_text("No revenue recorded", exact=False)
        ).to_be_visible()

        return True

    def verify_performance_section(self):
        # Performance heading
        expect(
            self.page.get_by_text("Performance", exact=True)
        ).to_be_visible(timeout=10000)

        # KPI text
        expect(
            self.page.get_by_text("KPI completion by metric")
        ).to_be_visible()

        # Daily Visits
        expect(
            self.page.get_by_text("Daily Visits").first
        ).to_be_visible()

        # Weekly Orders
        expect(
            self.page.get_by_text("Weekly Orders").first
        ).to_be_visible()

        # Monthly Revenue
        expect(
            self.page.get_by_text("Monthly Revenue").first
        ).to_be_visible()

        # Task Completion
        expect(
            self.page.get_by_text("Task Completion").first
        ).to_be_visible()

        # Progress circles
        expect(
            self.page.locator("[role='progressbar']").first
        ).to_be_visible()

        assert self.page.locator("[role='progressbar']").count() >= 4

        # Details
        expect(
            self.page.get_by_text("Details", exact=True)
        ).to_be_visible()

        # Smart Insight
        expect(
            self.page.get_by_text("Smart insight").nth(2)
        ).to_be_visible()

        return True

    def verify_interaction_insights(self):
        # Scroll until section is visible
        self.page.get_by_text(
            "Interaction Insights",
            exact=True
        ).scroll_into_view_if_needed()

        # Heading
        expect(
            self.page.get_by_text(
                "Interaction Insights",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Today dropdown
        expect(
            self.page.get_by_text(
                "Today",
                exact=True
            ).first
        ).to_be_visible(timeout=10000)

        # Description
        expect(
            self.page.get_by_text(
                "Unique partner engagement overview",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        # Empty state
        expect(
            self.page.get_by_text(
                "No activity recorded",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.get_by_text(
                "Start by visiting or meeting a partner",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        return True

    def verify_quick_actions_button(self):
        quick_action = self.page.locator(
            FieldExecutiveLocators.QUICK_ACTIONS_BUTTON
        )

        expect(quick_action).to_be_visible(timeout=10000)
        expect(quick_action).to_be_enabled()

        # Open Quick Actions
        quick_action.click()

        self.page.wait_for_timeout(1000)

        # Verify button is still visible
        expect(quick_action).to_be_visible()

        # Close Quick Actions by pressing Escape
        self.page.keyboard.press("Escape")

        self.page.wait_for_timeout(1000)

        return True