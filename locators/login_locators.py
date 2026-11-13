class LoginLocators:

    TENANT = "#tenantId"

    EMPLOYEE_ID = "#employeeId"

    PASSWORD = "#password"

    LOGIN_BUTTON = "button[type='submit']"
    ORGANIZATION_VERIFIED = "text=Organization verified"
    ORGANIZATION_NOT_FOUND = "text=Organization not found"
    INVALID_CREDENTIALS = (
        "text=The Employee ID or Password you entered is incorrect. "
        "Please try again."
    )