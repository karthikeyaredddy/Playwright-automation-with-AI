
import re


class RouteLocators:
    """Locators for the Route page."""

    FIELD_EXECUTIVE_MENU = "Field Executive"
    ROUTE_MENU = "Route"

    MONTH_FILTER_PATTERN = re.compile(
        r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}$"
    )

    CREATE_ROUTE_BUTTON = "Create Route"

    # Nearby partner selection
    NEARBY_PARTNERS_HEADING = "Nearby Partners"
    ADD_PARTNER_BUTTON_PATTERN = re.compile(
        r"^Add .+ to route$",
        re.IGNORECASE,
    )
    CONFIRM_SELECTION_BUTTON_PATTERN = re.compile(
        r"^Confirm(?: selection)?(?:\s*\(\d+\))?$",
        re.IGNORECASE,
    )

    # Selected partners
    ROUTE_STOPS_HEADING = "Route Stops"
    PARTNERS_SELECTED_PATTERN = re.compile(
        r"Partners Selected\s*\d+",
        re.IGNORECASE,
    )

    # Route schedule form
    ROUTE_NAME = "Route name"
    ROUTE_SCHEDULE = "Route schedule"
    WEEKLY_ROUTE = "Weekly Route"
    EFFECTIVE_FROM = "Effective from"
    NO_END_DATE = "No end date"
    EFFECTIVE_UNTIL = "Effective until"
    ROUTE_NOTES = "Route notes"

    SAVE_ROUTE_BUTTON = "Save Route"
    CANCEL_BUTTON = "Cancel"
    PLAN_ROUTE_HEADING = "Plan route schedule"

    RUN_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    ROUTE_OPTIONS_BUTTON = "Route options"
    EDIT_ROUTE_OPTION = "Edit route"
    CONFIRM_PARTNERS_BUTTON = "Confirm (2)"
    UPDATE_ROUTE_BUTTON = "Update route"
    CONFIRM_ROUTE_CHANGES_BUTTON = "Save route changes"

    DELETE_ROUTE_MENU_ITEM = "Delete route"


