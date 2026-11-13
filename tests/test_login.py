import re

import pytest
from playwright.sync_api import expect

from config.config import BASE_URL
from locators.login_locators import LoginLocators
from pages.login_page import LoginPage


class TestLogin:

    @pytest.mark.parametrize("role", ["admin"])
    def test_login(self, page, role):
        page.goto(BASE_URL)

        login = LoginPage(page)
        login.login(role)

        assert "/dashboard/" in page.url

    def _open_login(self, page):
        login = LoginPage(page)
        login.open()
        return login

    def _fill_valid_tenant(self, page, login, employee_id, password):
        user = login.get_login_credentials("admin")
        login.fill_credentials(user["tenant"], employee_id, password)
        expect(
            page.locator(LoginLocators.ORGANIZATION_VERIFIED)
        ).to_be_visible(timeout=15000)
        return user

    def _assert_login_rejected(self, page, error_locator):
        expect(page).to_have_url(re.compile(r".*/login/?$"))
        expect(
            page.locator(error_locator).first
        ).to_be_visible(timeout=15000)
        expect(page).not_to_have_url(re.compile(r".*/dashboard/.*"))

    def _assert_required_field(self, page, selector):
        field = page.locator(selector)
        expect(field).to_have_attribute("required", "")
        expect(page.locator(LoginLocators.LOGIN_BUTTON)).to_be_disabled()
        assert field.evaluate("(element) => element.validationMessage")

    def test_invalid_password(self, page):
        login = self._open_login(page)
        user = login.get_login_credentials("admin")
        self._fill_valid_tenant(
            page,
            login,
            user["employee_id"],
            "Incorrect-Password-920!"
        )

        login.submit_login()

        self._assert_login_rejected(
            page,
            LoginLocators.INVALID_CREDENTIALS
        )

    def test_invalid_employee_id(self, page):
        login = self._open_login(page)
        self._fill_valid_tenant(
            page,
            login,
            "invalid-employee-987654",
            "Valid-Format-Password-920!"
        )

        login.submit_login()

        self._assert_login_rejected(
            page,
            LoginLocators.INVALID_CREDENTIALS
        )

    def test_invalid_company_id(self, page):
        login = self._open_login(page)
        login.fill_credentials(
            "invalid-company-987654",
            "invalid-employee-987654",
            "Valid-Format-Password-920!"
        )

        expect(
            page.locator(LoginLocators.ORGANIZATION_NOT_FOUND)
        ).to_be_visible(timeout=15000)

        login_button = page.locator(LoginLocators.LOGIN_BUTTON)
        if login_button.is_enabled():
            login.submit_login()
        else:
            expect(login_button).to_be_disabled()

        self._assert_login_rejected(
            page,
            LoginLocators.ORGANIZATION_NOT_FOUND
        )

    def test_empty_credentials(self, page):
        login = self._open_login(page)
        login.fill_credentials("", "", "")

        self._assert_required_field(page, LoginLocators.TENANT)
        self._assert_required_field(page, LoginLocators.EMPLOYEE_ID)
        self._assert_required_field(page, LoginLocators.PASSWORD)

    def test_empty_password(self, page):
        login = self._open_login(page)
        user = login.get_login_credentials("admin")
        self._fill_valid_tenant(page, login, user["employee_id"], "")

        self._assert_required_field(page, LoginLocators.PASSWORD)

    def test_empty_employee_id(self, page):
        login = self._open_login(page)
        self._fill_valid_tenant(
            page,
            login,
            "",
            "Valid-Format-Password-920!"
        )

        self._assert_required_field(page, LoginLocators.EMPLOYEE_ID)

    def test_empty_company_id(self, page):
        login = self._open_login(page)
        user = login.get_login_credentials("admin")
        login.fill_credentials(
            "",
            user["employee_id"],
            "Valid-Format-Password-920!"
        )

        self._assert_required_field(page, LoginLocators.TENANT)

    def test_invalid_credentials(self, page):
        login = self._open_login(page)
        self._fill_valid_tenant(
            page,
            login,
            "invalid-employee-654321",
            "Incorrect-Password-920!"
        )

        login.submit_login()

        self._assert_login_rejected(
            page,
            LoginLocators.INVALID_CREDENTIALS
        )