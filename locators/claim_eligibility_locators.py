class ClaimEligibilityLocators:

    # Navigation
    ADMIN_BUTTON = 'button[id="account-menu-button"]'
    ACCOUNT_SETTINGS = "text=Account Settings"

    # Financial Configuration
    FINANCIAL_CONFIGURATION = "h2:has-text('Financial Configuration')"

    CLAIM_ELIGIBILITY_CARD = (
        "button[aria-label*='Claim Eligibility Amount Management']"
    )

    CLAIM_ELIGIBILITY_TITLE = (
        "h3:has-text('Claim Eligibility Amount Management')"
    )
    # Claim Rules Management
    ADD_RULE_BUTTON = "button:has-text('Add Rule')"
    # Add Claim Rule Form
    ROLE_DESIGNATION_FIELD = "label:has-text('Role / Designation')"
    CLAIM_TYPE_FIELD = "label:has-text('Claim Type')"

    MIN_VISITS_PER_DAY = "input"
    DEADLINE_FIELD = "input"

    STATUS_FIELD = "label:has-text('Status')"

    SAVE_BUTTON = "button:has-text('Save')"
    CANCEL_BUTTON = "button:has-text('Cancel')"

    # Modal
    ADD_CLAIM_RULE_MODAL = '[role="dialog"]'

    ROLE_DESIGNATION_LABEL = "Role / Designation"
    CLAIM_TYPE_LABEL = "Claim Type"
    MIN_VISITS_LABEL = "Min visits per day"
    DEADLINE_LABEL = "Day of next month (deadline)"
    STATUS_LABEL = "Status"
    # Existing Role Claim Rule
    EXISTING_ROLE_CARD = "div.MuiPaper-root"

    # Add Claim Rule Dialog
    CLAIM_RULE_DIALOG = '[role="dialog"]'