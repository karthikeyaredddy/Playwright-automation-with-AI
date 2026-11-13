import pytest
from pages.dashboard_page import DashboardPage
from pages.HREM_page import HREMPage


@pytest.mark.order(7)
class TestHRModule:


    def test_hr_module_working(self, logged_in_page):

        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_hr_module()

        hr = HREMPage(
            logged_in_page
        )

        assert hr.verify_hr_module()


class TestEmployeeManagement:

    def test_employee_directory(
        self,
        logged_in_page
    ):

        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_employee_management()

        assert hrem.verify_employee_directory()


    # def test_add_user(
    #     self,
    #     logged_in_page
    # ):
    #
    #     dashboard = DashboardPage(
    #         logged_in_page
    #     )
    #
    #     dashboard.open_employee_management()
    #
    #     hrem = HREMPage(
    #         logged_in_page
    #     )
    #
    #     data = hrem.create_dummy_user()
    #
    #     print(
    #         "Created Employee ID:",
    #         data["employee_id"]
    #     )
    #
    #     print(
    #         "Created Email:",
    #         data["email"]
    #     )
    #
    #     print(
    #         "Created Mobile:",
    #         data["mobile"]
    #     )


    def test_search(
        self,
        logged_in_page
    ):

        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_search_box()


    def test_filters(
        self,
        logged_in_page
    ):

        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_status_dropdown()

        assert hrem.verify_department_dropdown()

        assert hrem.verify_role_dropdown()

        assert hrem.verify_independent_employees()

        assert hrem.verify_reset_button()


    def test_bulk_upload(
        self,
        logged_in_page
    ):

        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_bulk_upload()

        assert hrem.verify_download_excel_template()

        assert hrem.verify_select_excel_file()

    def test_employee_list_and_hierarchy_view(
            self,
            logged_in_page
    ):
        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        # ==========================================
        # LIST VIEW
        # ==========================================

        assert hrem.verify_list_view()

        # ==========================================
        # HIERARCHY VIEW
        # ==========================================

        assert hrem.verify_hierarchy_view()

        # ==========================================
        # SWITCH BACK TO LIST VIEW
        # ==========================================

        assert hrem.verify_list_view()

    def test_employee_table_headers(
            self,
            logged_in_page
    ):
        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_employee_table_headers()

    def test_employee_actions(
            self,
            logged_in_page
    ):
        dashboard = DashboardPage(
            logged_in_page
        )

        dashboard.open_employee_management()

        hrem = HREMPage(
            logged_in_page
        )

        assert hrem.verify_employee_actions()