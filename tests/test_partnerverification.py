from pages.dashboard_page import DashboardPage
from pages.partnerverification_page import PartnerVerificationPage

class TestPartnerVerification:

    def test_partner_verification_page(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)
        partner = PartnerVerificationPage(logged_in_page)

        assert dashboard.open_partner_verification()
        assert partner.verify_partner_verification_module()

    def test_tabs(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)
        partner = PartnerVerificationPage(logged_in_page)

        dashboard.open_partner_verification()

        assert partner.verify_basic_details_tab()
        assert partner.verify_business_gst_tab()
        assert partner.verify_documents_tab()
        assert partner.verify_invalid_partners_tab()

    # def test_counts(self, logged_in_page):
    #     dashboard = DashboardPage(logged_in_page)
    #     partner = PartnerVerificationPage(logged_in_page)
    #
    #     dashboard.open_partner_verification()
    #
    #     assert partner.verify_pending_count()
    #     assert partner.verify_verified_today_count()

    def test_filters(self, logged_in_page):
        dashboard = DashboardPage(logged_in_page)
        partner = PartnerVerificationPage(logged_in_page)

        dashboard.open_partner_verification()

        assert partner.verify_search_working()
        assert partner.verify_state_filter()
        assert partner.verify_business_gst_filters()
        assert partner.verify_documents_filters()
        assert partner.verify_invalid_partners_filters()

