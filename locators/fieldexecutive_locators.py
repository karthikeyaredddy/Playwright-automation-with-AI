class FieldExecutiveLocators:
    # Sections
    WORK_PLAN = "//h6[contains(.,\"Today's Work Plan\")]"
    PERFORMANCE = "//h6[contains(.,'Performance')]"
    WEEKLY_VISITS = "//h6[contains(.,'Weekly Visits')]"
    RECENT_ACTIVITY = "//h6[contains(.,'Recent Activity')]"
    GREETING = "//div[contains(text(),'Good ')]"
    CURRENT_DATE = (
        "//p[contains(text(),'Monday') or "
        "contains(text(),'Tuesday') or "
        "contains(text(),'Wednesday') or "
        "contains(text(),'Thursday') or "
        "contains(text(),'Friday') or "
        "contains(text(),'Saturday') or "
        "contains(text(),'Sunday')]"
    )
    UPDATED_TEXT = "//p[contains(text(),'Updated')]"
    REFRESH_BUTTON = "//button[@aria-label='Refresh dashboard']"
    VISITS_TODAY = "text=Visits Today"
    ORDERS_TODAY = "text=Orders Today"
    REVENUE_TODAY = "text=Revenue Today"
    TODAY_WORK_PLAN = "text=Today's Work Plan"
    # Revenue Section
    REVENUE_SECTION = "text=Revenue"
    REVENUE_AMOUNT = "text=₹0"
    REVENUE_CHART = "svg.recharts-surface"
    SMART_INSIGHT = "text=Smart insight"
    SMART_INSIGHT_MESSAGE = "text=No revenue recorded for this period yet."
    REVENUE_DROPDOWN = "div[role='combobox']:has-text('Last 7 days')"
    KPI_TEXT = "text=KPI completion by metric"
    DAILY_VISITS = "text=Daily Visits"
    WEEKLY_ORDERS = "text=Weekly Orders"
    MONTHLY_REVENUE = "text=Monthly Revenue"
    TASK_COMPLETION = "text=Task Completion"
    DETAILS = "text=Details"
    PROGRESS_BARS = "[role='progressbar']"
    # Interaction Insights
    INTERACTION_INSIGHTS = "text=Interaction Insights"
    TODAY_DROPDOWN = "div[role='combobox'] >> text=Today"
    UNIQUE_PARTNER_TEXT = "text=Unique partner engagement overview"
    NO_ACTIVITY = "text=No activity recorded"
    START_VISITING = "text=Start by visiting or meeting a partner"
    # Existing locators...
    # Quick Actions
    QUICK_ACTIONS_BUTTON = "button[aria-label='Open quick actions menu']"
    # Material UI backdrop (used to close the menu)
    QUICK_ACTIONS_BACKDROP = ".MuiBackdrop-root"

