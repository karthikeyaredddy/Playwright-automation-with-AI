import os
from locators.login_locators import LoginLocators
from utils.excel_reader import ExcelReader

class LoginPage:
    URL = "https://ayksadev-adminportal.onrender.com/login"

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, role="admin"):
        excel_path = os.path.join(
            os.getcwd(),
            "testdata",
            "Logincredentials.xlsx"
        )

        users = ExcelReader.get_login_data(excel_path)
        user = next(
            u for u in users
            if u["role"].lower() == role.lower()
        )

        # Wait until login page loads
        self.page.wait_for_load_state("domcontentloaded")

        # Remove readonly attributes
        self.page.evaluate("""
                document.getElementById('tenantId').removeAttribute('readonly');
                document.getElementById('employeeId').removeAttribute('readonly');
                document.getElementById('password').removeAttribute('readonly');
            """)

        # Enter credentials
        self.page.locator(
            LoginLocators.TENANT
        ).fill(user["tenant"])

        self.page.locator(
            LoginLocators.EMPLOYEE_ID
        ).fill(user["employee_id"])

        self.page.locator(
            LoginLocators.PASSWORD
        ).fill(user["password"])

        # Login
        self.page.locator(
            LoginLocators.LOGIN_BUTTON
        ).click()

        # Wait for dashboard URL
        self.page.wait_for_url(
            "**/dashboard/**",
            timeout=120000
        )

        return self.page