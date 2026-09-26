import re

from playwright.sync_api import expect
from locators.Reimbursement_locators import ReimbursementLocators


class ReimbursementPage:

    def __init__(self, page):
        self.page = page

        # ==========================================================

    # Common Reusable Helpers
    # ==========================================================

    def open_reimbursement_module(self, module_name):

        menu = self.page.get_by_role(
            "button",
            name=module_name
        )

        expect(menu).to_be_visible(timeout=10000)

        menu.click()

        self.page.wait_for_load_state("networkidle")

        heading_map = {
            "My Claims": "Claims Overview",
            "Admin Claim Approvals": "Review and approve employee reimbursement claims",
            "Manager Claim Approvals": "Review and approve employee reimbursement claims",
        }

        if module_name in heading_map:
            expect(
                self.page.get_by_role(
                    "heading",
                    name=heading_map[module_name]
                )
            ).to_be_visible(timeout=10000)

        return True

    def no_claims_available(self):

        return self.page.get_by_text(
            "0 claims match your filters"
        ).is_visible()

    def click_button(self, locator):

        button = self.page.locator(locator)

        expect(button).to_be_visible(timeout=10000)
        expect(button).to_be_enabled()

        button.click()

        return button

    def fill_search(self, locator, value):

        search = self.page.locator(locator)

        expect(search).to_be_visible(timeout=10000)

        search.fill(value)

        expect(search).to_have_value(value)

        return search

    def fill_date(self, locator, value):

        field = self.page.locator(locator)

        expect(field).to_be_visible(timeout=10000)

        field.fill(value)

        expect(field).to_have_value(value)

        return field

    def verify_table_headers(self, headers):

        for header in headers:
            expect(
                self.page.get_by_role(
                    "columnheader",
                    name=header
                )
            ).to_be_visible(timeout=10000)

        return True

    def verify_filter_buttons(
            self,
            filters,
            verify_empty=True
    ):

        for name in filters:

            button = self.page.get_by_role(
                "button",
                name=name
            )

            expect(button).to_be_visible(timeout=10000)

            button.click()

            self.page.wait_for_load_state("networkidle")

            table = self.page.locator("table")

            if verify_empty:

                if table.count() > 0:
                    expect(table).to_be_visible()

                else:
                    expect(
                        self.page.get_by_text(
                            "claims match your filters"
                        )
                    ).to_be_visible()

            else:
                expect(table).to_be_visible()

        return True

    def verify_receipt_dialog(
            self,
            button_name="View receipt"
    ):

        button = self.page.get_by_role(
            "button",
            name=button_name
        )

        if button.count() == 0:
            print(f"No {button_name} button available.")
            return True

        expect(button.first).to_be_visible(timeout=10000)

        button.first.click()

        dialog = self.page.get_by_role("dialog")

        expect(dialog).to_be_visible(timeout=10000)

        close = dialog.get_by_role(
            "button",
            name="Close"
        )

        expect(close).to_be_visible(timeout=10000)

        close.click()

        expect(dialog).not_to_be_visible(timeout=10000)

        return True

    def verify_rows_dropdown(self, pagination_locator=None):

        try:

            dropdown = self.page.get_by_role(
                "combobox",
                name=re.compile(
                    r"Rows per page",
                    re.IGNORECASE
                )
            )

            if dropdown.count() == 0:
                print(
                    "Rows per page is not available because no records are present."
                )

                return True

            expect(dropdown).to_be_visible(
                timeout=10000
            )

            expect(dropdown).to_be_enabled()

            dropdown.click()

            options = self.page.get_by_role(
                "option"
            )

            if options.count() > 1:
                options.nth(1).click()

                self.page.wait_for_load_state(
                    "networkidle"
                )

            if pagination_locator:

                pagination = self.page.locator(
                    pagination_locator
                )

                if pagination.count() > 0:
                    expect(
                        pagination
                    ).to_be_visible(
                        timeout=10000
                    )

            return True

        except Exception as e:

            raise AssertionError(
                f"Failed to fetch Rows Per Page: {e}"
            )

    def click_apply(self):
        """Click the Apply button after changing a filter."""

        apply_button = self.page.get_by_role(
            "button",
            name="Apply",
            exact=True
        )

        expect(apply_button).to_be_visible(timeout=10000)
        expect(apply_button).to_be_enabled(timeout=10000)

        apply_button.click()

        return True

    # ==========================================================

    # My Claims
    # ==========================================================

    def verify_my_claims(self):

        return self.open_reimbursement_module(
            "My Claims"
        )

        # ==========================================================

    # Claim Filters
    # ==========================================================

    def verify_claim_filters(self):

        return self.verify_filter_buttons(
            [
                "All",
                "In progress",
                "Approved",
                "Rejected"
            ]
        )

        # ==========================================================

    # Table Headers
    # ==========================================================

    def verify_all_filter_table_headers(self):

        self.page.get_by_role(
            "button",
            name="All"
        ).click()

        self.page.wait_for_load_state(
            "networkidle"
        )

        if self.no_claims_available():
            print(
                "No claims available. Skipping table verification."
            )

            return True

        headers = [
            "Type",
            "Status",
            "Claimed (₹)",
            "Approved (₹)",
            "Date",
            "Reason",
            "Receipts",
        ]

        return self.verify_table_headers(
            headers
        )

        # ==========================================================

    # View Receipts
    # ==========================================================

    def verify_view_receipts(self):

        if self.no_claims_available():
            print(
                "No claims available. Skipping receipt test."
            )

            return True

        return self.verify_receipt_dialog(
            button_name="View receipts"
        )

        # ==========================================================

    # Rows Per Page
    # ==========================================================

    def verify_rows_per_page(self):

        if self.no_claims_available():
            print(
                "No claims available. Skipping pagination."
            )

            return True

        return self.verify_rows_dropdown()

        # ==========================================================

    # Search
    # ==========================================================

    def verify_search_and_filters(self):
        """Verify search, date and status filters using Apply."""

        # Search
        search = self.page.locator(ReimbursementLocators.SEARCH_BOX)
        expect(search).to_be_visible(timeout=10000)

        search.fill("Local")
        expect(search).to_have_value("Local")

        self.click_apply()

        # Date
        from_date = self.page.locator(ReimbursementLocators.FROM_DATE)
        to_date = self.page.locator(ReimbursementLocators.TO_DATE)

        from_date.fill("2026-07-01")
        to_date.fill("2026-07-31")

        expect(from_date).to_have_value("2026-07-01")
        expect(to_date).to_have_value("2026-07-31")

        self.click_apply()

        # Status
        approved = self.page.get_by_role(
            "button",
            name="Approved",
            exact=True
        )

        expect(approved).to_be_visible(timeout=10000)
        approved.click()

        self.click_apply()

        return True

        # ==========================================================

    # New Claim
    # ==========================================================

    def verify_new_claim(self):

        dialog = self.page.locator(
            ReimbursementLocators.NEW_CLAIM_TITLE
        )

        if dialog.is_visible():
            return True

        button = self.page.locator(
            ReimbursementLocators.NEW_CLAIM_BUTTON
        )

        expect(
            button
        ).to_be_visible(
            timeout=10000
        )

        expect(
            button
        ).to_be_enabled()

        button.click()

        expect(
            dialog
        ).to_be_visible(
            timeout=10000
        )

        return True

        # ==========================================================

    # Admin Claim Approvals
    # ==========================================================

    def verify_admin_claim_approvals(self):

        return self.open_reimbursement_module(
            "Admin Claim Approvals"
        )

        # ==========================================================

    # Admin Filters
    # ==========================================================

    def verify_admin_claim_filters(self):

        return self.verify_filter_buttons(
            [
                "All",
                "In progress",
                "Approved",
                "Rejected"
            ],
            verify_empty=False
        )

        # ==========================================================

    # Admin Table Headers
    # ==========================================================

    def verify_admin_claim_table_headers(self):

        headers = [
            "Emp ID",
            "Name",
            "Type",
            "Total (₹)",
            "Claim period",
            "Status",
            "Actions",
            "Receipts"
        ]

        return self.verify_table_headers(
            headers
        )

        # ==========================================================

    # View Receipt
    # ==========================================================

    def verify_view_receipt_working(self):

        return self.verify_receipt_dialog(
            button_name="View receipt"
        )

        # ==========================================================

    # Admin Rows Per Page
    # ==========================================================

    def verify_admin_rows_per_page(self):

        return self.verify_rows_dropdown(
            pagination_locator="text=/.*of.*/"
        )

        # ==========================================================

    # Admin Search
    # ==========================================================

    def verify_search_and_filters(self):
        """Verify search, date and status filters using Apply."""

        # Search
        search = self.page.locator(ReimbursementLocators.SEARCH_BOX)
        expect(search).to_be_visible(timeout=10000)

        search.fill("Local")
        expect(search).to_have_value("Local")

        self.click_apply()

        # Date
        from_date = self.page.locator(ReimbursementLocators.FROM_DATE)
        to_date = self.page.locator(ReimbursementLocators.TO_DATE)

        from_date.fill("2026-07-01")
        to_date.fill("2026-07-31")

        expect(from_date).to_have_value("2026-07-01")
        expect(to_date).to_have_value("2026-07-31")

        self.click_apply()

        # Status
        approved = self.page.get_by_role(
            "button",
            name="Approved",
            exact=True
        )

        expect(approved).to_be_visible(timeout=10000)
        approved.click()

        self.click_apply()

        return True

        # ==========================================================

    # Manager Claim Approvals
    # ==========================================================

    def verify_manager_claim_approvals(self):

        return self.open_reimbursement_module(
            "Manager Claim Approvals"
        )

        # ==========================================================

    # Manager Filters
    # ==========================================================

    def verify_manager_claim_filters(self):

        return self.verify_filter_buttons(
            [
                "All",
                "In progress",
                "Approved",
                "Rejected"
            ],
            verify_empty=False
        )

        # ==========================================================

    # Manager Table Headers
    # ==========================================================

    def verify_manager_claim_table_headers(self):

        headers = [
            "Emp ID",
            "Name",
            "Type",
            "Total (₹)",
            "Claim period",
            "Status",
            "Actions",
            "Receipts"
        ]

        return self.verify_table_headers(
            headers
        )

        # ==========================================================

    # Manager View Receipt
    # ==========================================================

    def verify_manager_view_receipt_working(self):

        return self.verify_receipt_dialog(
            button_name="View receipt"
        )

        # ==========================================================

    # Manager Receipt Close Button
    # ==========================================================

    def verify_manager_receipt_close_button(self):

        return self.verify_receipt_dialog(
            button_name="View receipt"
        )

        # ==========================================================

    # Manager Rows Per Page
    # ==========================================================

    def verify_manager_rows_per_page(self):

        return self.verify_rows_dropdown(
            pagination_locator=
            ReimbursementLocators.MANAGER_DISPLAYED_ROWS
        )

        # ==========================================================

    # Manager Search
    # ==========================================================

    def verify_manager_search_working(self):

        self.fill_search(
            ReimbursementLocators.MANAGER_SEARCH,
            "emp002"
        )

        return True

        # ==========================================================

    # Manager From Date
    # ==========================================================

    def verify_manager_from_date_working(self):

        self.fill_date(
            ReimbursementLocators.MANAGER_FROM_DATE,
            "2026-07-01"
        )

        return True

        # ==========================================================

    # Manager To Date
    # ==========================================================

    def verify_manager_to_date_working(self):

        self.fill_date(
            ReimbursementLocators.MANAGER_TO_DATE,
            "2026-07-31"
        )

        return True

        # ==========================================================

    # Manager Reset Button
    # ==========================================================

    def verify_manager_reset_button_working(self):

        self.fill_search(
            ReimbursementLocators.MANAGER_SEARCH,
            "emp002"
        )

        self.fill_date(
            ReimbursementLocators.MANAGER_FROM_DATE,
            "2026-07-01"
        )

        self.fill_date(
            ReimbursementLocators.MANAGER_TO_DATE,
            "2026-07-31"
        )

        reset_button = self.page.locator(
            ReimbursementLocators.MANAGER_RESET_BUTTON
        )

        expect(
            reset_button
        ).to_be_visible(
            timeout=10000
        )

        expect(
            reset_button
        ).to_be_enabled()

        reset_button.click()

        expect(
            self.page.locator(
                ReimbursementLocators.MANAGER_SEARCH
            )
        ).to_have_value("")

        expect(
            self.page.locator(
                ReimbursementLocators.MANAGER_FROM_DATE
            )
        ).to_have_value("")

        expect(
            self.page.locator(
                ReimbursementLocators.MANAGER_TO_DATE
            )
        ).to_have_value("")

        return True



        # ==========================================================
    # Claim Stats & History
    # ==========================================================

    def verify_claim_stats_history(self):

        menu = self.page.get_by_role(
            "button",
            name="Claim Stats & History",
            exact=True
        )

        expect(
            menu
        ).to_be_visible(
            timeout=10000
        )

        if "/dashboard/claim-stats" not in self.page.url:

            menu.click()

        expect(
            self.page
        ).to_have_url(
            re.compile(
                r".*/dashboard/claim-stats.*"
            ),
            timeout=60000
        )

        # Wait until spinner disappears
        spinner = self.page.locator(
            "[role='progressbar']"
        )

        try:

            expect(
                spinner
            ).to_be_hidden(
                timeout=120000
            )

        except:
            pass

        self.page.wait_for_load_state(
            "domcontentloaded"
        )

        self.page.wait_for_load_state(
            "networkidle"
        )

        return True

    # ==========================================================
    # Claim Analytics Dashboard
    # ==========================================================

    def verify_claim_analytics_dashboard(self):

        heading = self.page.get_by_role(
            "heading",
            name="Claims Analytics & Insights"
        )

        expect(
            heading
        ).to_be_visible(
            timeout=60000
        )

        expect(
            self.page.get_by_text(
                "Track claim volumes, approval trends, and performance across your organization."
            )
        ).to_be_visible()

        expect(
            self.page.locator(
                ReimbursementLocators.CLAIM_ANALYTICS_SEARCH
            )
        ).to_be_visible(
            timeout=60000
        )

        return True

    # ==========================================================
    # Analytics Filters
    # ==========================================================

    def verify_claim_analytics_filters(self):

        self.fill_search(
            ReimbursementLocators.CLAIM_ANALYTICS_SEARCH,
            "emp001"
        )

        from_date = self.page.get_by_role(
            "textbox",
            name="From date"
        )
        expect(from_date).to_be_visible(timeout=10000)
        from_date.fill("2026-07-01")

        to_date = self.page.get_by_role(
            "textbox",
            name="To date"
        )
        expect(to_date).to_be_visible(timeout=10000)
        to_date.fill("2026-07-31")

        # Apply filters
        apply_button = self.page.locator(
            ReimbursementLocators.CLAIM_ANALYTICS_APPLY
        )
        expect(apply_button).to_be_visible(timeout=10000)
        expect(apply_button).to_be_enabled()
        apply_button.click()

        self.page.wait_for_load_state("networkidle")

        reset = self.page.locator(
            ReimbursementLocators.CLAIM_ANALYTICS_RESET
        )
        if reset.count() > 0:
            expect(reset).to_be_visible(timeout=10000)
            expect(reset).to_be_enabled()
            reset.click()

        return True
    # ==========================================================
    # Time Filters
    # ==========================================================

    def verify_time_filters(self):

        filters = [
            "Previous Month",
            "Present Month",
            "All Time"

        ]

        for name in filters:

            button = self.page.get_by_role(
                "button",
                name=name
            )

            expect(
                button
            ).to_be_visible(
                timeout=10000
            )

            expect(
                button
            ).to_be_enabled()

            button.click()

            self.page.wait_for_load_state(
                "networkidle"
            )

        return True

    # ==========================================================
    # Claim Table Headers
    # ==========================================================

    def verify_claim_table_headers_visible(self):

        headers = [
            "Employee",
            "Type",
            "Claimed Amount",
            "Approved Amount",
            "Status",
            "Stage",
            "Date",
            "Actions"
        ]

        return self.verify_table_headers(
            headers
        )

    # ==========================================================
    # View Details Dialog
    # ==========================================================

    def verify_view_dialog(self):

        button = self.page.get_by_role(
            "button",
            name="View details"
        )

        if button.count() == 0:

            print(
                "No View Details button available."
            )

            return True

        button.first.click()

        dialog = self.page.locator(
            ReimbursementLocators.CLAIM_DETAILS_DIALOG
        )

        expect(dialog).to_be_visible(timeout=10000)

        title = dialog.locator(
            ReimbursementLocators.CLAIM_DETAILS_TITLE
        )

        expect(title).to_have_text(
            "Claim Details"
        )

        self.page.locator(
            ReimbursementLocators.CLOSE_BUTTON
        ).click()

        expect(
            dialog
        ).not_to_be_visible(
            timeout=10000
        )

        return True

    # ==========================================================
    # Claim Stats Rows Per Page
    # ==========================================================

    def verify_claim_stats_rows_per_page(self):

        return self.verify_rows_dropdown(
            pagination_locator=
            "p.MuiTablePagination-displayedRows"
        )

    # ==========================================================
    # Download Excel Dialog
    # ==========================================================

    def verify_download_excel_dialog(self):

        dialog = self.page.get_by_role(
            "dialog",
            name="Export Claims to Excel"
        )

        if dialog.count() > 0 and dialog.is_visible():

            return True

        download = self.page.get_by_role(
            "button",
            name="Download Excel",
            exact=True
        )

        expect(
            download
        ).to_be_visible(
            timeout=10000
        )

        expect(
            download
        ).to_be_enabled()

        download.click()

        expect(
            dialog
        ).to_be_visible(
            timeout=10000
        )

        expect(
            dialog.get_by_role(
                "heading",
                name="Export Claims to Excel"
            )
        ).to_be_visible(
            timeout=10000
        )

        return True

    # ==========================================================
    # Export File Name
    # ==========================================================

    def verify_export_file_name(self):

        dialog = self.page.get_by_role(
            "dialog",
            name="Export Claims to Excel"
        )

        expect(
            dialog
        ).to_be_visible(
            timeout=10000
        )

        file_name = dialog.get_by_role(
            "textbox",
            name="File Name"
        )

        expect(
            file_name
        ).to_be_visible(
            timeout=10000
        )

        value = file_name.input_value()

        assert value.endswith(
            ".xlsx"
        )

        dialog.get_by_role(
            "button",
            name="Cancel"
        ).click()

        expect(
            dialog
        ).not_to_be_visible(
            timeout=10000
        )

        return True