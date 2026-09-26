# import pytest
#
# from config.config import BASE_URL
# from pages.login_page import LoginPage
#
#
# class TestLogin:
#
#     @pytest.mark.parametrize("role", ["admin"])
#     def test_login(self, page, role):
#         page.goto(BASE_URL)
#
#         login = LoginPage(page)
#         login.login(role)
#
#         assert "/dashboard/" in page.url