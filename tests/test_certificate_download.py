# from pages.dashboard_page import DashboardPage
#
#
# class TestCertificateDownload:
#
#     def test_certificate_download_visible(self, logged_in_page):
#        dashboard = DashboardPage(logged_in_page)
#
#         dashboard.open_side_menu()
#
#         dashboard.page.get_by_role(
#            "button",
#             name="Certificate Download"
#        ).click()
#
#         assert dashboard.verify_certificate_download_visible()