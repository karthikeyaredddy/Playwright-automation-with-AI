import re
from datetime import datetime
from pathlib import Path
import pytest
from playwright.sync_api import expect
from locators.HREM_locators import HREMLocators
class HREMPage:
    def __init__(self, page):
        self.page = page
    # ==========================================================
    # HR Module
    # ==========================================================

    def verify_hr_module(self):

        expect(
            self.page.locator(
                HREMLocators.HR_DASHBOARD
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.locator(
                HREMLocators.EMPLOYEE_MANAGEMENT
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.locator(
                HREMLocators.ORGANIZATION
            )
        ).to_be_visible(timeout=10000)

        return True

         # ==========================================================
         # Employee Management
         # ==========================================================

    def verify_employee_management(self):

        expect(
            self.page.get_by_role(
                "heading",
                name="Employee Directory"
            )
        ).to_be_visible(timeout=10000)

        expect(
            self.page.get_by_text(
                "Manage employee records, roles, departments, and account access."
            )
        ).to_be_visible(timeout=10000)

        return True

        return True
            # ==========================================================
            # Employee Directory
            # ==========================================================

    def verify_employee_directory(self):
        expect(
            self.page.locator(HREMLocators.EMPLOYEE_DIRECTORY_HEADING)
        ).to_be_visible(timeout=10000)

        expect(
            self.page.locator(HREMLocators.EMPLOYEE_DIRECTORY_DESCRIPTION)
        ).to_be_visible(timeout=10000)

        return True

    def verify_search_box(self):

        search = self.page.locator(HREMLocators.SEARCH_BOX)

        # Verify search box is visible
        expect(search).to_be_visible(timeout=10000)

        # Enter any sample text
        search.fill("test")

        # Verify text is entered
        expect(search).to_have_value("test")

        # Clear the search box
        search.clear()

        # Verify search box is empty
        expect(search).to_have_value("")

        return True


    def verify_status_dropdown(self):
        status = self.page.locator(HREMLocators.STATUS_DROPDOWN)

        expect(status).to_be_visible(timeout=10000)

        status.click()

        expect(
            self.page.locator("ul[role='listbox']")
        ).to_be_visible(timeout=5000)

        self.page.keyboard.press("Escape")

        return True

    def verify_department_dropdown(self):
        department = self.page.locator(HREMLocators.DEPARTMENT_DROPDOWN)

        expect(department).to_be_visible(timeout=10000)

        department.click()

        expect(
            self.page.locator("ul[role='listbox']")
        ).to_be_visible(timeout=5000)

        self.page.keyboard.press("Escape")

        return True

    def verify_role_dropdown(self):
        role = self.page.locator(HREMLocators.ROLE_DROPDOWN)

        expect(role).to_be_visible(timeout=10000)

        role.click()

        expect(
            self.page.locator("ul[role='listbox']")
        ).to_be_visible(timeout=5000)

        self.page.keyboard.press("Escape")

        return True

    def verify_independent_employees(self):
        toggle = self.page.locator(HREMLocators.INDEPENDENT_EMPLOYEES)

        expect(toggle).to_be_visible(timeout=10000)

        toggle.check(force=True)

        expect(toggle).to_be_checked()

        toggle.uncheck(force=True)

        expect(toggle).not_to_be_checked()

        return True

    def verify_reset_button(self):
        reset = self.page.locator(HREMLocators.RESET_BUTTON)

        expect(reset).to_be_visible(timeout=10000)

        reset.click()

        self.page.wait_for_timeout(2000)

        return True

    def verify_bulk_upload(self):

        bulk_upload = self.page.locator(HREMLocators.BULK_UPLOAD_BUTTON)

        # Verify button is visible
        expect(bulk_upload).to_be_visible(timeout=10000)

        # Verify button is enabled
        expect(bulk_upload).to_be_enabled()

        # Click the button
        bulk_upload.click()

        # Wait for upload dialog/page
        self.page.wait_for_timeout(2000)

        return True

    def verify_download_excel_template(self):

        # Popup is already open
        download_btn = self.page.locator(HREMLocators.DOWNLOAD_EXCEL_TEMPLATE)

        expect(download_btn).to_be_visible(timeout=10000)
        expect(download_btn).to_be_enabled()

        download_btn.click()

        # Wait until download starts or finishes
        self.page.wait_for_timeout(3000)

        return True

    def verify_select_excel_file(self):

        # Popup is already open

        file_input = self.page.locator(HREMLocators.SELECT_EXCEL_FILE)

        expect(file_input).to_be_attached(timeout=10000)

        project_root = Path(__file__).resolve().parent.parent

        file_path = project_root / "testdata" / "user_bulk_upload_template.xlsx"

        file_input.set_input_files(str(file_path))

        upload_btn = self.page.locator(HREMLocators.UPLOAD_USERS_BUTTON)
        expect(upload_btn).to_be_enabled(timeout=10000)

        # Close popup
        close_btn = self.page.get_by_role("button", name="Close")
        expect(close_btn).to_be_visible(timeout=10000)
        close_btn.click()

        # Wait until popup disappears
        expect(close_btn).not_to_be_visible(timeout=10000)

        return True

    # ==========================================================
    # ADD USER
    # ==========================================================

    def open_add_user(self):

        # Find Add User only in the main page area
        add_user_button = (
            self.page
            .get_by_role("main")
            .get_by_role(
                "button",
                name="Add User",
                exact=True
            )
        )

        expect(
            add_user_button
        ).to_be_visible(timeout=15000)

        expect(
            add_user_button
        ).to_be_enabled()

        add_user_button.scroll_into_view_if_needed()

        add_user_button.click()

        # Wait for MUI dialog rendering
        self.page.wait_for_timeout(1000)

        dialog = self.page.get_by_role(
            "dialog"
        )

        expect(
            dialog
        ).to_be_visible(timeout=15000)

        # Verify Add User heading
        expect(
            dialog.get_by_role(
                "heading",
                name="Add User",
                exact=True
            )
        ).to_be_visible(timeout=10000)

        return dialog

    # ==========================================================
    # GENERATE DUMMY DATA
    # ==========================================================

    def generate_dummy_user_data(self):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )

        return {
            "employee_id": f"TEST{timestamp}",

            "full_name": "Test Employee",

            "email": (
                f"testemployee{timestamp}@example.com"
            ),

            "password": "Test@12345",

            "designation": "Test Executive",

            "mobile": "1465378890",

            "address": (
                "Service Road, Green Glen Layout, "
                "Bellandur, Bengaluru, Karnataka, 560103, India"
            ),

            "latitude": "12.923981898472297",

            "longitude": "77.67186260887135",

            "role": "Field Executive",
        }
    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    def fill_basic_information(self, dialog, data):

        # ==========================================
        # Employee ID
        # ==========================================

        employee_id = dialog.get_by_role(
            "textbox",
            name="Employee ID *",
            exact=True
        )

        expect(
            employee_id
        ).to_be_visible(timeout=10000)

        employee_id.fill(
            data["employee_id"]
        )

        # ==========================================
        # Full Name
        # ==========================================

        full_name = dialog.get_by_role(
            "textbox",
            name="Full Name *",
            exact=True
        )

        expect(
            full_name
        ).to_be_visible(timeout=10000)

        full_name.fill(
            data["full_name"]
        )

        # ==========================================
        # Email
        # ==========================================

        email = dialog.get_by_role(
            "textbox",
            name="Email *",
            exact=True
        )

        expect(
            email
        ).to_be_visible(timeout=10000)

        email.fill(
            data["email"]
        )

        # ==========================================
        # Password
        # ==========================================

        password = dialog.get_by_role(
            "textbox",
            name="Password",
            exact=True
        )

        expect(
            password
        ).to_be_visible(timeout=10000)

        password.fill(
            data["password"]
        )
    # ==========================================================
    # ROLE
    # ==========================================================
    def select_role(
            self,
            dialog,
            role="Field Executive"
    ):

        # Find Role dropdown
        role_dropdown = dialog.locator(
            HREMLocators.ROLE_SELECT
        )

        expect(
            role_dropdown
        ).to_be_visible(timeout=10000)

        role_dropdown.scroll_into_view_if_needed()

        role_dropdown.click()

        # MUI renders dropdown outside the dialog
        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        # Actual option names are like:
        # Field Executive (L3)
        #
        # So don't use exact=True.
        option = listbox.get_by_role(
            "option",
            name=re.compile(
                rf"^{re.escape(role)}\s*\("
            )
        )

        expect(
            option
        ).to_be_visible(timeout=5000)

        option.click()

        self.page.wait_for_timeout(500)

        print(
            f"Selected Role: {role}"
        )
    # ==========================================================
    # DESIGNATION
    # ==========================================================

    def fill_designation(
            self,
            dialog,
            designation=None
    ):

        designation_dropdown = dialog.get_by_role(
            "combobox",
            name="Designation *",
            exact=True
        )

        expect(
            designation_dropdown
        ).to_be_visible(timeout=10000)

        designation_dropdown.scroll_into_view_if_needed()

        designation_dropdown.click()

        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        options = listbox.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=5000)

        if designation:

            matching = options.filter(
                has_text=designation
            )

            if matching.count() > 0:
                matching.first.click()
            else:
                options.first.click()

        else:
            options.first.click()

        self.page.wait_for_timeout(500)

    # ==========================================================
    # DEPARTMENT
    # ==========================================================

    def select_department(self, dialog):

        department_dropdown = dialog.get_by_role(
            "combobox",
            name="Department *",
            exact=True
        )

        expect(
            department_dropdown
        ).to_be_visible(timeout=10000)

        department_dropdown.scroll_into_view_if_needed()

        department_dropdown.click()

        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        options = listbox.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=5000)

        options.first.click()

        self.page.wait_for_timeout(500)
    # ==========================================================
    # DATE OF JOINING
    # ==========================================================

    def fill_date_of_joining(self, dialog):

        date_field = dialog.get_by_role(
            "textbox",
            name="Date of joining",
            exact=True
        )

        expect(
            date_field
        ).to_be_visible(timeout=10000)

        today = datetime.now().strftime(
            "%d-%m-%Y"
        )

        date_field.fill(today)
    # ==========================================================
    # SHIFT
    # ==========================================================

    def select_shift(self, dialog):

        shift_dropdown = dialog.get_by_role(
            "combobox",
            name="Shift",
            exact=True
        )

        expect(
            shift_dropdown
        ).to_be_visible(timeout=10000)

        shift_dropdown.scroll_into_view_if_needed()

        shift_dropdown.click()

        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        options = listbox.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=5000)

        options.first.click()

        self.page.wait_for_timeout(500)

    # ==========================================================
    # TIMEZONE
    # ==========================================================

    def select_timezone(self, dialog):

        timezone_dropdown = dialog.get_by_role(
            "combobox",
            name="TimeZone",
            exact=True
        )

        expect(
            timezone_dropdown
        ).to_be_visible(timeout=10000)

        timezone_dropdown.scroll_into_view_if_needed()

        timezone_dropdown.click()

        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        options = listbox.get_by_role(
            "option"
        )

        expect(
            options.first
        ).to_be_visible(timeout=5000)

        options.first.click()

        self.page.wait_for_timeout(500)
    # ==========================================================
    # LOCATION
    # ==========================================================

    def fill_location(self, dialog, data):

        # ==========================================
        # Address
        # ==========================================

        address = dialog.get_by_role(
            "textbox",
            name="Address",
            exact=True
        )

        expect(
            address
        ).to_be_visible(timeout=10000)

        address.fill(
            data["address"]
        )

        # ==========================================
        # Latitude
        # ==========================================

        latitude = dialog.get_by_role(
            "spinbutton",
            name="Latitude",
            exact=True
        )

        expect(
            latitude
        ).to_be_visible(timeout=10000)

        latitude_value = latitude.input_value()

        print(
            "Latitude automatically populated:",
            latitude_value
        )

        assert latitude_value != "", (
            "Latitude is empty"
        )

        # ==========================================
        # Longitude
        # ==========================================

        longitude = dialog.get_by_role(
            "spinbutton",
            name="Longitude",
            exact=True
        )

        expect(
            longitude
        ).to_be_visible(timeout=10000)

        longitude_value = longitude.input_value()

        print(
            "Longitude automatically populated:",
            longitude_value
        )

        assert longitude_value != "", (
            "Longitude is empty"
        )
    # ==========================================================
    # COUNTRY
    # ==========================================================

    def select_country(self, dialog):

        country_dropdown = dialog.get_by_role(
            "combobox",
            name="Country",
            exact=True
        )

        expect(
            country_dropdown
        ).to_be_visible(timeout=10000)

        country_dropdown.scroll_into_view_if_needed()

        country_dropdown.click()

        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        # Prefer India
        india = listbox.get_by_role(
            "option",
            name="India",
            exact=True
        )

        if india.count() > 0:
            india.click()
        else:
            listbox.get_by_role(
                "option"
            ).first.click()

        self.page.wait_for_timeout(500)
    # ==========================================================
    # MOBILE
    # ==========================================================

    def fill_mobile(self, dialog, mobile):

        mobile_field = dialog.get_by_role(
            "textbox",
            name="Mobile number, 10 digits",
            exact=True
        )

        expect(
            mobile_field
        ).to_be_visible(timeout=10000)

        mobile_field.fill(
            mobile

        )
    # ==========================================================
    # VEHICLE
    # ==========================================================

    def select_vehicle_type(
            self,
            dialog,
            vehicle_type="Two Wheeler"
    ):

        vehicle_dropdown = dialog.get_by_role(
            "combobox",
            name="Vehicle Type Vehicle Type",
            exact=True
        )

        expect(
            vehicle_dropdown
        ).to_be_visible(timeout=10000)

        vehicle_dropdown.scroll_into_view_if_needed()

        expect(
            vehicle_dropdown
        ).to_be_enabled()

        # Open dropdown
        vehicle_dropdown.click()

        # Wait for options
        listbox = self.page.get_by_role(
            "listbox"
        )

        expect(
            listbox
        ).to_be_visible(timeout=5000)

        # Select vehicle
        vehicle_option = listbox.get_by_role(
            "option",
            name=vehicle_type,
            exact=True
        )

        expect(
            vehicle_option
        ).to_be_visible(timeout=5000)

        vehicle_option.click()

    # ==========================================================
    # STATUS
    # ==========================================================

    def select_active_status(
            self,
            dialog
    ):

        active = dialog.get_by_label(
            "Active",
            exact=True
        )

        if active.count() > 0:
            if active.is_visible():
                active.check()

    # ==========================================================
    # CREATE
    # ==========================================================

    def click_create(self, dialog):

        create_button = dialog.get_by_role(
            "button",
            name="Create",
            exact=True
        )

        expect(
            create_button
        ).to_be_visible(timeout=10000)

        expect(
            create_button
        ).to_be_enabled()

        create_button.click()
    # ==========================================================
    # COMPLETE ADD USER FLOW
    # ==========================================================

    def create_dummy_user(self):

        # ==========================================
        # Generate dummy data
        # ==========================================

        data = self.generate_dummy_user_data()

        print("\n======================================")
        print("Creating Dummy Employee")
        print("======================================")
        print("Employee ID :", data["employee_id"])
        print("Name        :", data["full_name"])
        print("Email       :", data["email"])
        print("Mobile      :", data["mobile"])
        print("======================================")

        # ==========================================
        # Open Add User dialog
        # ==========================================

        dialog = self.open_add_user()

        # ==========================================
        # Basic Information
        # ==========================================

        self.fill_basic_information(
            dialog,
            data
        )

        # ==========================================
        # Work Information
        # ==========================================

        self.select_role(
            dialog,
            "Field Executive"
        )

        self.fill_designation(
            dialog
        )

        self.select_department(
            dialog
        )

        self.fill_date_of_joining(
            dialog
        )

        self.select_shift(
            dialog
        )

        self.select_timezone(
            dialog
        )

        # ==========================================
        # Location
        # ==========================================

        self.fill_location(
            dialog,
            data
        )

        self.select_country(
            dialog
        )

        # ==========================================
        # Contact
        # ==========================================

        self.fill_mobile(
            dialog,
            data["mobile"]
        )

        # ==========================================
        # Create
        # ==========================================

        self.click_create(
            dialog
        )

        # ==========================================
        # Wait for dialog to close
        # ==========================================

        expect(
            dialog
        ).to_be_hidden(timeout=15000)

        print(
            "\nSUCCESS: Employee created successfully."
        )

        print(
            "Employee ID:",
            data["employee_id"]
        )

        return data

    # ==========================================================
    # EMPLOYEE VIEW
    # ==========================================================

    def verify_list_view(self):

        list_view = self.page.locator(
            HREMLocators.LIST_VIEW_BUTTON
        )

        expect(list_view).to_be_visible(timeout=10000)
        expect(list_view).to_be_enabled()

        # Click List View
        list_view.click()

        self.page.wait_for_timeout(1000)

        # Verify employee table is displayed
        table = self.page.locator("table")

        expect(table).to_be_visible(timeout=10000)

        # Verify important table header
        expect(
            self.page.locator(
                HREMLocators.FULL_NAME_HEADER
            )
        ).to_be_visible(timeout=10000)

        print("List View is working successfully.")

        return True

    def verify_hierarchy_view(self):

        hierarchy_view = self.page.locator(
            HREMLocators.HIERARCHY_VIEW_BUTTON
        )

        expect(hierarchy_view).to_be_visible(timeout=10000)
        expect(hierarchy_view).to_be_enabled()

        # Click Hierarchy View
        hierarchy_view.click()

        self.page.wait_for_timeout(1500)

        print("Hierarchy View button clicked successfully.")

        return True

    # ==========================================================
    # EMPLOYEE TABLE HEADERS
    # ==========================================================

    def verify_employee_table_headers(self):

        headers = [
            ("Full Name", HREMLocators.FULL_NAME_HEADER),
            ("Employee ID", HREMLocators.EMPLOYEE_ID_HEADER),
            ("Email", HREMLocators.EMAIL_HEADER),
            ("Role", HREMLocators.ROLE_HEADER),
            ("Designation", HREMLocators.DESIGNATION_HEADER),
            ("Department", HREMLocators.DEPARTMENT_HEADER),
            ("Mobile", HREMLocators.MOBILE_HEADER),
            ("Zone", HREMLocators.ZONE_HEADER),
            ("State", HREMLocators.STATE_HEADER),
            ("City", HREMLocators.CITY_HEADER),
            ("Tenant ID", HREMLocators.TENANT_ID_HEADER),
            ("Status", HREMLocators.STATUS_HEADER),
            ("Actions", HREMLocators.ACTIONS_HEADER),
        ]

        for header_name, locator in headers:
            header = self.page.locator(locator)

            expect(
                header
            ).to_be_visible(timeout=10000)

            print(
                f"PASS: {header_name} header is visible."
            )

        print(
            "\nPASS: All Employee Directory table headers are visible."
        )

        return True

    # ==========================================================
    # EMPLOYEE ACTIONS
    # ==========================================================

    def verify_employee_actions(self):

        # ==========================================
        # Switch to List View
        # ==========================================

        self.verify_list_view()

        # Wait for employee table
        self.page.wait_for_selector(
            "tbody tr",
            timeout=10000
        )

        # ==========================================
        # Check employee records
        # ==========================================

        rows = self.page.locator("tbody tr")

        if rows.count() == 0:
            pytest.skip(
                "No employee records available for action testing."
            )

        print(
            f"Employee rows found: {rows.count()}"
        )

        # Use first employee row
        first_row = rows.first

        # ==========================================
        # VIEW / VISIBILITY ICON
        # ==========================================

        view_button = first_row.locator(
            HREMLocators.VIEW_BUTTON
        )

        expect(
            view_button
        ).to_be_visible(timeout=10000)

        expect(
            view_button
        ).to_be_enabled()

        print("PASS: View / Visibility icon is visible.")

        # Click View
        view_button.click()

        # Wait for View dialog
        view_dialog = self.page.locator(
            HREMLocators.VIEW_DIALOG
        )

        expect(
            view_dialog
        ).to_be_visible(timeout=10000)

        print("PASS: View dialog opened successfully.")

        # ==========================================
        # CLOSE VIEW DIALOG
        # ==========================================

        close_button = view_dialog.get_by_role(
            "button",
            name="Close",
            exact=True
        )

        expect(
            close_button
        ).to_be_visible(timeout=10000)

        close_button.click()
        expect(
            view_dialog
        ).not_to_be_visible(timeout=10000)

        print("PASS: View dialog closed successfully.")

        # ==========================================
        # EDIT ICON
        # ==========================================

        edit_button = first_row.locator(
            HREMLocators.EDIT_BUTTON
        )

        expect(
            edit_button
        ).to_be_visible(timeout=10000)

        expect(
            edit_button
        ).to_be_enabled()

        print("PASS: Edit icon is visible.")

        # Click Edit
        edit_button.click()

        # Wait for Edit dialog
        edit_dialog = self.page.locator(
            HREMLocators.EDIT_DIALOG
        )

        expect(
            edit_dialog
        ).to_be_visible(timeout=10000)

        print("PASS: Edit dialog opened successfully.")

        # ==========================================
        # CANCEL EDIT
        # ==========================================

        cancel_button = edit_dialog.get_by_role(
            "button",
            name="Cancel",
            exact=True
        )

        expect(
            cancel_button
        ).to_be_visible(timeout=10000)

        cancel_button.click()

        expect(
            edit_dialog
        ).not_to_be_visible(timeout=10000)

        print("PASS: Edit dialog cancelled successfully.")

        # ==========================================
        # DELETE ICON
        # ==========================================

        delete_button = first_row.locator(
            HREMLocators.DELETE_BUTTON
        )

        expect(
            delete_button
        ).to_be_visible(timeout=10000)

        expect(
            delete_button
        ).to_be_enabled()

        print("PASS: Delete icon is visible.")

        # Click Delete
        delete_button.click()

        # ==========================================
        # DELETE CONFIRMATION DIALOG
        # ==========================================

        delete_dialog = self.page.locator(
            HREMLocators.VIEW_DIALOG
        )

        expect(
            delete_dialog
        ).to_be_visible(timeout=10000)

        print(
            "PASS: Delete confirmation dialog opened successfully."
        )

        # ==========================================
        # CANCEL DELETE
        # ==========================================

        cancel_delete = delete_dialog.get_by_role(
            "button",
            name="Cancel",
            exact=True
        )

        expect(
            cancel_delete
        ).to_be_visible(timeout=10000)

        cancel_delete.click()

        expect(
            delete_dialog
        ).not_to_be_visible(timeout=10000)

        print(
            "PASS: Delete operation cancelled successfully."
        )

        print(
            "\nPASS: View → Close → Edit → Cancel → Delete → Cancel flow completed successfully."
        )

        return True