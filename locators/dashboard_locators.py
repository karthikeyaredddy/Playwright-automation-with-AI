class DashboardLocators:
    LOGO = "//img[@alt='Tunez']"
    MENU_BUTTON = "button[aria-label='open drawer']"
    MENU_ICON = "button[aria-label='Collapse sidebar']"
    SIDEBAR = "nav[aria-label='mailbox folders']"
    ADMIN_BUTTON = 'button[id="account-menu-button"]'
    MY_PROFILE = 'p:has-text("My Profile")'
    PROFILE_DRAWER = "div.MuiDrawer-paper"
    PROFILE_TITLE = "h6:has-text('ADMIN')"
    EMPLOYEE_ID = "text=EMPLOYEE ID"
    ROLE = "text=ROLE"
    ORGANIZATION = "text=ORGANIZATION"
    EMAIL = "text=EMAIL"
    PHONE = "text=PHONE"
    EDIT_PROFILE_BUTTON = "button:has-text('Edit profile')"
    CLOSE_PROFILE = "button[aria-label='Close profile']"
    CHANGE_PASSWORD = 'text=Change Password'
    CHANGE_PASSWORD_DIALOG = 'div[role="dialog"]'

    CURRENT_PASSWORD = 'input[placeholder="Current Password"]'
    NEW_PASSWORD = 'input[placeholder="New Password"]'
    CONFIRM_PASSWORD = 'input[placeholder="Confirm New Password"]'
    LOGOUT_BUTTON = 'text=Logout'
    CONFIRM_LOGOUT_TITLE = 'text=Confirm Logout'
    CANCEL_BUTTON = 'button:has-text("Cancel")'
    # ============================
    # Account Settings
    # ============================
    ACCOUNT_SETTINGS = "text=Account Settings"
    CONFIGURATION_HUB = "text=Configuration Hub"
    SEARCH_SETTINGS = 'input[aria-label="Search settings"]'
    # ============================
    # Organization & Access
    # ============================
    ORGANIZATION_ACCESS = "h2:has-text('Organization & Access')"
    FEATURE_PERMISSION = "h3:has-text('Feature Permission')"
    USER_MANAGEMENT = "h3:has-text('User Management')"
    ROLE_MANAGEMENT = "h3:has-text('Role Management')"
    # ============================
    # Financial Configuration
    # ============================
    FINANCIAL_CONFIGURATION = "h2:has-text('Financial Configuration')"
    FARE_CONFIGURATION = "h3:has-text('Fare Configuration')"
    CLAIM_ELIGIBILITY = "h3:has-text('Claim Eligibility Amount Management')"
    PARTNER_BENEFITS = "h3:has-text('Partner Benefits')"
    # ============================
    # Branding & Templates
    # ============================
    BRANDING_TEMPLATES = "h2:has-text('Branding & Templates')"
    ANNOUNCEMENTS = "h3:has-text('Announcements')"
    # ============================
    # Logos and Brand
    # ============================
    LOGOS_AND_BRAND = "h2:has-text('Logos and Brand')"
    COMPANY_LOGO = "h3:has-text('Company Logo')"
    TENANT_TEMPLATE_MANAGEMENT = "h3:has-text('Tenant Template Management')"
    # ============================
    # System & Operations
    # ============================
    SYSTEM_OPERATIONS = "h2:has-text('System & Operations')"
    PMS_CONFIGURATION = "h3:has-text('PMS Configuration')"
    # ============================
    # Categories & Modules
    # ============================
    CATEGORIES_CHIP = "text=5 categories"
    MODULES_CHIP = "text=modules"
    EXPAND_ALL = "button:has-text('Expand all')"
    COLLAPSE_ALL = "button:has-text('Collapse all')"
    # =====================
    # FIELD EXECUTIVE
    # =====================
    FIELD_EXECUTIVE = "button:has-text('Field Executive')"

    FIELD_EXECUTIVE_DASHBOARD = "div[data-sidebar-active='true'] span:has-text('Dashboard')"

    #==================
    #PARTNER VERIFICATION
    #===================
    PARTNER_VERIFICATION = "text=Partner Verification"
    # ==========================
    # Reimbursement
    # ==========================
    REIMBURSEMENT_MENU = "button:has-text('Reimbursement')"
    CLAIMS_OVERVIEW = "h2:has-text('Claims Overview')"
    MY_CLAIMS_HEADING = "h2:has-text('Claims Overview')"
    ADMIN_CLAIM_APPROVALS = "text=Admin Claim Approvals"
    MANAGER_CLAIM_APPROVALS = "text=Manager Claim Approvals"
    CLAIM_STATS_HISTORY = "text=Claim Stats & History"
    # Sidebar
    EMS_MENU = "button:has-text('EMS')"
