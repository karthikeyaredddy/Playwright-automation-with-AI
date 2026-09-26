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