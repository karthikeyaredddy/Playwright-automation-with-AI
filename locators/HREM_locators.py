class HREMLocators:

    HR_MENU = "div[role='button']:has-text('HR')"

    HR_DASHBOARD = "div[role='button']:has-text('HR Dashboard')"

    EMPLOYEE_MANAGEMENT = "div[role='button']:has-text('Employee Management')"

    ORGANIZATION = "div[role='button']:has-text('Organization')"

    ROLES = "div[role='button']:has-text('Roles')"

    DEPARTMENT = "div[role='button']:has-text('Department')"

    EMPLOYEE_DIRECTORY = "h2"

    EMPLOYEE_DIRECTORY_HEADING = (
        "//h2[normalize-space()='Employee Directory']"
    )

    EMPLOYEE_DIRECTORY_DESCRIPTION = (
        "//p[contains(text(),'Manage employee records, roles, departments, and account access.')]"
    )

    SEARCH_BOX = "input[placeholder='Search employee']"

    STATUS_DROPDOWN = (
        "div[aria-labelledby='employee-status-label']"
    )

    DEPARTMENT_DROPDOWN = (
        "div[aria-labelledby='employee-department-label']"
    )

    ROLE_DROPDOWN = (
        "div[aria-labelledby='employee-role-label']"
    )

    INDEPENDENT_EMPLOYEES = "input[type='checkbox']"

    RESET_BUTTON = "button:has-text('Reset')"

    LIST_VIEW = (
        "div[aria-labelledby='employee-view-by-label']"
    )

    VIEW_BY_DROPDOWN = (
        "div[aria-labelledby='employee-view-by-label']"
    )

    CARD_VIEW_OPTION = "li[data-value='card']"

    LIST_VIEW_OPTION = "li[data-value='list']"


    # ---------------------------------
    # Pagination
    # ---------------------------------

    PREVIOUS_PAGE = (
        "button[aria-label='Go to previous page']"
    )

    NEXT_PAGE = (
        "button[aria-label='Go to next page']"
    )

    PAGE_1 = "button[aria-label='Go to page 1']"

    PAGE_2 = "button[aria-label='Go to page 2']"

    # ---------------------------------
    # Bulk Upload
    # ---------------------------------

    BULK_UPLOAD_BUTTON = (
        "button:has-text('Bulk Upload')"
    )

    DOWNLOAD_EXCEL_TEMPLATE = (
        "button:has-text('Download Excel Template')"
    )

    SELECT_EXCEL_FILE = (
        "input#bulk-upload-file-input"
    )

    UPLOAD_USERS_BUTTON = (
        "button:has-text('Upload Users')"
    )



    # =================================
    # Add User
    # =================================

    ADD_USER_BUTTON = "button:has-text('Add User')"

    ADD_USER_DIALOG = "div[role='dialog']"

    CREATE_BUTTON = "button:has-text('Create')"

    ROLE_SELECT = "#mui-component-select-role"

    # ---------------------------------
    # Basic Information
    # ---------------------------------

    EMPLOYEE_ID = "input[name='employee_id']"
    FULL_NAME = "input[name='full_name']"
    EMAIL = "input[type='email']"

    PASSWORD = (
        "input[name='password']"
    )
    # ---------------------------------
    # Contact
    # ---------------------------------

    MOBILE = "input[placeholder='Mobile number, 10 digits']"

    # ---------------------------------
    # Location
    # ---------------------------------

    ADDRESS = "textarea"

    LATITUDE = (
        "input[placeholder='Latitude']"
    )

    LONGITUDE = (
        "input[placeholder='Longitude']"
    )
    # ---------------------------------
    # Employee View
    # ---------------------------------

    LIST_VIEW_BUTTON = (
        "button:has-text('List View')"
    )

    HIERARCHY_VIEW_BUTTON = (
        "button:has-text('Hierarchy View')"
    )

    LIST_VIEW_TEXT = (
        "button:has-text('List View')"
    )

    HIERARCHY_VIEW_TEXT = (
        "button:has-text('Hierarchy View')"
    )
    # ---------------------------------
    # Table Headers
    # ---------------------------------

    FULL_NAME_HEADER = "//th[normalize-space()='Full Name']"

    EMPLOYEE_ID_HEADER = "//th[normalize-space()='Employee ID']"

    EMAIL_HEADER = "//th[normalize-space()='Email']"

    ROLE_HEADER = "//th[normalize-space()='Role']"

    DESIGNATION_HEADER = "//th[normalize-space()='Designation']"

    DEPARTMENT_HEADER = "//th[normalize-space()='Department']"

    MOBILE_HEADER = "//th[normalize-space()='Mobile']"

    ZONE_HEADER = "//th[normalize-space()='Zone']"

    STATE_HEADER = "//th[normalize-space()='State']"

    CITY_HEADER = "//th[normalize-space()='City']"

    TENANT_ID_HEADER = "//th[normalize-space()='Tenant ID']"

    STATUS_HEADER = "//th[normalize-space()='Status']"

    ACTIONS_HEADER = "//th[normalize-space()='Actions']"

    # ---------------------------------
    # Employee Actions
    # ---------------------------------

    VIEW_EMPLOYEE = (
        "button[aria-label='View employee']"
    )

    EDIT_EMPLOYEE = (
        "button[aria-label='Edit employee']"
    )

    DELETE_EMPLOYEE = (
        "button[aria-label='Delete employee']"
    )

    VIEW_BUTTON = (
        "button[aria-label='View employee']"
    )

    EDIT_BUTTON = (
        "button[aria-label='Edit employee']"
    )

    DELETE_BUTTON = (
        "button[aria-label='Delete employee']"
    )

    VIEW_DIALOG = "div[role='dialog']"

    EDIT_DIALOG = "div[role='dialog']"

    CLOSE_BUTTON = "button:has-text('Close')"

    CANCEL_BUTTON = "button:has-text('Cancel')"

    CANCEL_DELETE = "button:has-text('Cancel')"