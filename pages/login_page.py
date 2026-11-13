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

    def get_login_credentials(self, role="admin"):
        excel_path = os.path.join(
            os.getcwd(),
            "testdata",
            "Logincredentials.xlsx"
        )

        users = ExcelReader.get_login_data(excel_path)
        return next(
            u for u in users
            if u["role"].lower() == role.lower()
        )

    def fill_credentials(self, tenant, employee_id, password):
        self.page.evaluate("""
                document.getElementById('tenantId').removeAttribute('readonly');
                document.getElementById('employeeId').removeAttribute('readonly');
                document.getElementById('password').removeAttribute('readonly');
            """)

        self.page.locator(LoginLocators.TENANT).fill(str(tenant))
        self.page.locator(LoginLocators.EMPLOYEE_ID).fill(str(employee_id))
        self.page.locator(LoginLocators.PASSWORD).fill(str(password))

    def submit_login(self):
        self.page.locator(LoginLocators.LOGIN_BUTTON).click()

    def login(self, role="admin"):
        user = self.get_login_credentials(role)

        # Wait until login page loads
        self.page.wait_for_load_state("domcontentloaded")

        # Enter credentials
        self.fill_credentials(
            user["tenant"],
            user["employee_id"],
            user["password"]
        )

        # Login
        self.submit_login()

        # Wait for dashboard URL
        self.page.wait_for_url(
            "**/dashboard/**",
            timeout=120000
        )

        self.page.reload(
            wait_until="networkidle",
            timeout=120000,
        )
        self.page.wait_for_url(
            "**/dashboard/**",
            timeout=120000,
        )

        return self.page