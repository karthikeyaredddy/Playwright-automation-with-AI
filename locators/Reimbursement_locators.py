class ReimbursementLocators:
    MY_CLAIMS_BUTTON = "button:has-text('My Claims')"
    MY_CLAIMS_HEADING = "h2:has-text('Claims Overview')"
    MY_CLAIMS_PAGE = "h1:has-text('My Claims')"
    CLAIMS_OVERVIEW = "h2:has-text('Claims Overview')"
    CLAIMS_DESCRIPTION = "text=View and manage your reimbursement claims."
    MYCLAIMS_FROM_DATE = "input#my-claims-from"
    MYCLAIMS_TO_DATE = "input#my-claims-to"
# Filter Buttons
    ALL_FILTER = "button:has-text('All')"
    IN_PROGRESS_FILTER = "button:has-text('In Progress')"
    APPROVED_FILTER = "button:has-text('Approved')"
    REJECTED_FILTER = "button:has-text('Rejected')"
    APPLY_FILTER = "button:has-text('Apply')"
    # Claims Table
    CLAIMS_TABLE = "table"

    # ==========================
    # Claims Table Headers
    # ==========================
    TYPE_HEADER = "//th[normalize-space()='Type']"
    STATUS_HEADER = "//th[normalize-space()='Status']"
    CLAIMED_HEADER = "//th[contains(normalize-space(),'Claimed')]"
    APPROVED_HEADER = "//th[contains(normalize-space(),'Approved')]"
    DATE_HEADER = "//th[normalize-space()='Date']"
    REASON_HEADER = "//th[normalize-space()='Reason']"
    RECEIPTS_HEADER = "//th[normalize-space()='Receipts']"
    RECEIPTS_VIEW_BUTTON = "button[aria-label='View receipts']"
    RECEIPTS_DIALOG = "div[role='dialog']"
    CLAIM_DETAILS = "text=Claim Details"
    CLOSE_RECEIPTS = "button:has-text('Close')"
    # ==========================
    # Pagination
    # ==========================
    ROWS_PER_PAGE_LABEL = "text=Rows per page"
    ROWS_PER_PAGE_DROPDOWN = "div[role='combobox'][aria-haspopup='listbox']"
    ROWS_PER_PAGE_OPTIONS = "ul[role='listbox'] li"
    DISPLAYED_ROWS = "p.MuiTablePagination-displayedRows"
    NEW_CLAIM_BUTTON = "button:has-text('New claim')"
    NEW_CLAIM_TITLE = "text=New Claim"
    # Search & Filters
    SEARCH_BOX = "input[placeholder='Search by type, status, or reason']"
    FROM_DATE = "input[aria-label='From date']"
    TO_DATE = "input[aria-label='To date']"
    RESET_BUTTON = "button:has-text('Reset')"
    ADMIN_CLAIM_APPROVALS = "//span[normalize-space()='Admin Claim Approvals']"
    ADMIN_CLAIM_APPROVALS_HEADING = "//h4[normalize-space()='Admin Claim Approvals']"
    ADMIN_ALL_FILTER = "button:has-text('All')"
    ADMIN_IN_PROGRESS_FILTER = "button:has-text('In progress')"
    ADMIN_APPROVED_FILTER = "button:has-text('Approved')"
    ADMIN_REJECTED_FILTER = "button:has-text('Rejected')"
    ADMIN_SEARCH_BOX = "input[placeholder='Search employee by name or ID']"
    ADMIN_EMP_ID_HEADER = "//th[normalize-space()='Emp ID']"
    ADMIN_NAME_HEADER = "//th[normalize-space()='Name']"
    ADMIN_TYPE_HEADER = "//th[normalize-space()='Type']"
    ADMIN_TOTAL_HEADER = "//th[contains(normalize-space(),'Total')]"
    ADMIN_CLAIM_PERIOD_HEADER = "//th[contains(normalize-space(),'Claim period')]"
    ADMIN_STATUS_HEADER = "//th[normalize-space()='Status']"
    ADMIN_ACTIONS_HEADER = "//th[normalize-space()='Actions']"
    ADMIN_RECEIPTS_HEADER = "//th[normalize-space()='Receipts']"
    VIEW_RECEIPT_BUTTON = "button[aria-label='View receipt']"
    RECEIPT_DIALOG = "[role='dialog']"
    RECEIPT_CLOSE_BUTTON = "[role='dialog'] button"
    PREVIOUS_PAGE = "button[aria-label='Go to previous page']"
    NEXT_PAGE = "button[aria-label='Go to next page']"
    MANAGER_CLAIM_APPROVALS = "//span[normalize-space()='Manager Claim Approvals']"
    MANAGER_CLAIM_APPROVALS_HEADING = (
        "h2:has-text('Review and approve employee reimbursement claims')"
    )
    # ==========================================================
    # Manager Claim Table Headers
    # ==========================================================
    MANAGER_EMP_ID_HEADER = "//th[normalize-space()='Emp ID']"
    MANAGER_NAME_HEADER = "//th[normalize-space()='Name']"
    MANAGER_TYPE_HEADER = "//th[normalize-space()='Type']"
    MANAGER_TOTAL_HEADER = "//th[contains(normalize-space(),'Total')]"
    MANAGER_CLAIM_PERIOD_HEADER = "//th[contains(normalize-space(),'Claim period')]"
    MANAGER_STATUS_HEADER = "//th[normalize-space()='Status']"
    MANAGER_ACTIONS_HEADER = "//th[normalize-space()='Actions']"
    MANAGER_RECEIPTS_HEADER = "//th[normalize-space()='Receipts']"
    MANAGER_VIEW_BUTTON = "button[aria-label='View receipt']"
    MANAGER_RECEIPT_DIALOG = "[role='dialog']"
    MANAGER_RECEIPT_CLOSE = "[role='dialog'] button"
    # ==========================================================
    # Manager Rows Per Page
    # ==========================================================
    MANAGER_ROWS_PER_PAGE_LABEL = "text=Rows per page"
    MANAGER_ROWS_PER_PAGE_DROPDOWN = "div[role='combobox']"
    MANAGER_ROWS_PER_PAGE_OPTIONS = "ul[role='listbox'] li"
    MANAGER_DISPLAYED_ROWS = "p.MuiTablePagination-displayedRows"
    # ==========================================================
    # Manager Claim Filters
    # ==========================================================
    MANAGER_SEARCH = "#manager-claims-search"
    MANAGER_FROM_DATE = "#manager-claims-from"
    MANAGER_TO_DATE = "#manager-claims-to"
    MANAGER_RESET_BUTTON = "button:has-text('Reset')"
    # ==========================================================
    # Claim Stats & History
    # ==========================================================
    CLAIM_STATS_HISTORY_MENU = "//span[normalize-space()='Claim Stats & History']"
    CLAIM_STATS_HISTORY_HEADING = "text=Claim Stats & History"
    CLAIM_ANALYTICS_SEARCH = "input[placeholder='Search employee by name or ID']"
    CLAIM_ANALYTICS_FROM_DATE = "input#claim-stats-from"  # keep for reference, unused now
    CLAIM_ANALYTICS_TO_DATE = "input#claim-stats-to"  # keep for reference, unused now
    CLAIM_ANALYTICS_RESET = "button:has-text('Reset')"
    PREVIOUS_MONTH = "button:has-text('Previous Month')"
    PRESENT_MONTH = "button:has-text('Present Month')"
    ALL_TIME = "button:has-text('All Time')"
    # ==============================
    # Claim Analytics Table Headers
    # ==============================

    EMPLOYEE_HEADER = "th:has-text('Employee')"
    CLAIMED_AMOUNT_HEADER = "th:has-text('Claimed Amount')"
    APPROVED_AMOUNT_HEADER = "th:has-text('Approved Amount')"
    STAGE_HEADER = "th:has-text('Stage')"
    ACTIONS_HEADER = "th:has-text('Actions')"

    # Dialog
    VIEW_DIALOG = '[role="dialog"]'
    # View Details button
    VIEW_BUTTON = "button[aria-label='View details']"
    # Claim Details dialog
    CLAIM_DETAILS_DIALOG = "div[role='dialog']"
    # Dialog title
    CLAIM_DETAILS_TITLE = "h6:has-text('Claim Details')"
    # Close button
    CLOSE_BUTTON = "button:has-text('Close')"
    DOWNLOAD_EXCEL_BUTTON = "button:has-text('Download Excel')"
    # ==========================
    # Apply Buttons (per module)
    # ==========================
    APPLY_BUTTON = "button:has-text('Apply')"                 # My Claims
    ADMIN_APPLY_BUTTON = "button:has-text('Apply')"            # Admin Claim Approvals
    MANAGER_APPLY_BUTTON = "button:has-text('Apply')"          # Manager Claim Approvals
    CLAIM_ANALYTICS_APPLY = "button:has-text('Apply')"         # Claim Stats & History
    STATUS_DROPDOWN = "//div[@role='combobox' and .//text()[contains(.,'Status')]]"