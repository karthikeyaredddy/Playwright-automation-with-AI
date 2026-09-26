from pages.dashboard_page import DashboardPage
from pages.Reimbursement_page import ReimbursementPage

class BaseReimbursement:

    def open_my_claims(self, page):

        dashboard = DashboardPage(page)
        dashboard.open_reimbursement()

        reimbursement = ReimbursementPage(page)
        reimbursement.verify_my_claims()

        return reimbursement

    def open_admin_claims(self, page):

        dashboard = DashboardPage(page)
        dashboard.open_reimbursement()

        reimbursement = ReimbursementPage(page)
        reimbursement.verify_admin_claim_approvals()

        return reimbursement

    def open_manager_claims(self, page):

        dashboard = DashboardPage(page)
        dashboard.open_reimbursement()

        reimbursement = ReimbursementPage(page)
        reimbursement.verify_manager_claim_approvals()

        return reimbursement

    def open_claim_stats(self, page):

        dashboard = DashboardPage(page)
        dashboard.open_reimbursement()

        reimbursement = ReimbursementPage(page)
        reimbursement.verify_claim_stats_history()

        return reimbursement

# ==========================================================
# MY CLAIMS
# ==========================================================

class TestMyClaims(BaseReimbursement):

    def test_my_claims_complete(self, logged_in_page):

        reimbursement = self.open_my_claims(logged_in_page)

        assert reimbursement.verify_claim_filters()

        assert reimbursement.verify_all_filter_table_headers()

        assert reimbursement.verify_view_receipts()

        assert reimbursement.verify_rows_per_page()

        assert reimbursement.verify_search_and_filters()

        assert reimbursement.verify_new_claim()

# ==========================================================
# ADMIN CLAIM APPROVALS
# ==========================================================

class TestAdminClaimApprovals(BaseReimbursement):

    def test_admin_claims_complete(self, logged_in_page):

        reimbursement = self.open_admin_claims(logged_in_page)

        assert reimbursement.verify_admin_claim_filters()

        assert reimbursement.verify_admin_claim_table_headers()

        assert reimbursement.verify_view_receipt_working()

        assert reimbursement.verify_admin_rows_per_page()

        assert reimbursement.verify_admin_search_filters()


# ==========================================================
# MANAGER CLAIM APPROVALS
# ==========================================================

class TestManagerClaimApprovals(BaseReimbursement):

    def test_manager_claims_complete(self, logged_in_page):

        reimbursement = self.open_manager_claims(
            logged_in_page
        )

        assert reimbursement.verify_manager_claim_filters()

        assert reimbursement.verify_manager_claim_table_headers()

        assert reimbursement.verify_manager_receipt_close_button()

        assert reimbursement.verify_manager_rows_per_page()

        assert reimbursement.verify_manager_search_working()

        assert reimbursement.verify_manager_from_date_working()

        assert reimbursement.verify_manager_to_date_working()

        assert reimbursement.verify_manager_reset_button_working()


# ==========================================================
# CLAIM STATS & HISTORY
# ==========================================================
 
class TestClaimStats(BaseReimbursement):

    def test_claim_stats_complete(self, logged_in_page):

        reimbursement = self.open_claim_stats(logged_in_page)

        assert reimbursement.verify_claim_analytics_dashboard()

        assert reimbursement.verify_claim_analytics_filters()

        assert reimbursement.verify_time_filters()

        assert reimbursement.verify_claim_table_headers_visible()

        assert reimbursement.verify_view_dialog()

        assert reimbursement.verify_claim_stats_rows_per_page()

        assert reimbursement.verify_download_excel_dialog()

        assert reimbursement.verify_export_file_name()