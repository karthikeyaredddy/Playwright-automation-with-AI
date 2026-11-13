from playwright.sync_api import expect
import re

from locators.dashboard_locators import DashboardLocators
class DashboardPage:
    def __init__(self, page):
        self.page = page
        #logo
    def verify_logo_visible(self):
        logo = self.page.locator(
            DashboardLocators.LOGO
        ).first
        expect(logo).to_be_visible(timeout=10000)
        return True

    #open side menu
    def open_side_menu(self):
        menu = self.page.locator(DashboardLocators.MENU_BUTTON)
        if menu.is_visible():
            menu.click()

    # Sidebar lock

    def verify_sidebar_lock_toggle(self):
        sidebar = self.page.locator(
            DashboardLocators.SIDEBAR
        )
        expect(sidebar).to_be_visible(timeout=10000)

        lock_button = self.page.locator(
            DashboardLocators.LOCK_SIDEBAR_BUTTON
        )
        expect(lock_button).to_be_visible(timeout=10000)
        lock_button.click()

        unlock_button = self.page.locator(
            DashboardLocators.UNLOCK_SIDEBAR_BUTTON
        )
        expect(unlock_button).to_be_visible(timeout=10000)
        unlock_button.click()

        expect(lock_button).to_be_visible(timeout=10000)
        expect(sidebar).to_be_visible(timeout=10000)

        return True


    #admin button

    def verify_admin_button_working(self):
        self.page.locator(DashboardLocators.ADMIN_BUTTON).click()

        expect(
            self.page.locator("#account-menu-appbar")
        ).to_be_visible(timeout=10000)

        # Close dropdown
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(1000)

        return True

    def verify_my_profile(self):
        self.page.locator(DashboardLocators.ADMIN_BUTTON).click()
        self.page.wait_for_timeout(500)

        self.page.locator(DashboardLocators.MY_PROFILE).click()

        profile = self.page.locator("div.MuiDrawer-paperAnchorRight")
        expect(profile).to_be_visible(timeout=10000)

        expect(profile.get_by_text("EMPLOYEE ID", exact=True)).to_be_visible()
        expect(profile.get_by_text("ROLE", exact=True)).to_be_visible()
        expect(profile.get_by_text("ORGANIZATION", exact=True)).to_be_visible()
        expect(profile.get_by_text("EMAIL", exact=True)).to_be_visible()
        expect(profile.get_by_text("PHONE", exact=True)).to_be_visible()

        # Close profile drawer
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(1000)

        return True

    #change password
    def verify_change_password(self):
        # Open Admin menu
        self.page.locator(
            DashboardLocators.ADMIN_BUTTON
        ).click()

        # Click Change Password
        self.page.locator(
            DashboardLocators.CHANGE_PASSWORD
        ).click()

        # Verify popup
        dialog = self.page.locator(
            DashboardLocators.CHANGE_PASSWORD_DIALOG
        )

        expect(dialog).to_be_visible(timeout=10000)

        # Locate password fields
        current_password = self.page.locator(
            DashboardLocators.CURRENT_PASSWORD
        )

        new_password = self.page.locator(
            DashboardLocators.NEW_PASSWORD
        )

        confirm_password = self.page.locator(
            DashboardLocators.CONFIRM_PASSWORD
        )

        # Verify fields are visible
        expect(current_password).to_be_visible(timeout=10000)
        expect(new_password).to_be_visible(timeout=10000)
        expect(confirm_password).to_be_visible(timeout=10000)

        # Remove readonly attribute from all password fields
        self.page.evaluate("""
            () => {
                document.querySelectorAll(
                    'input[placeholder="Current Password"], \
                     input[placeholder="New Password"], \
                     input[placeholder="Confirm New Password"]'
                ).forEach(input => {
                    input.removeAttribute('readonly');
                });
            }
        """)

        # Enter passwords
        current_password.fill("tunez1234")
        new_password.fill("tunez123")
        confirm_password.fill("tunez123")

        # Click Change Password button inside dialog
        change_password_button = dialog.get_by_role(
            "button",
            name="Change Password"
        )

        expect(change_password_button).to_be_visible(timeout=10000)

        change_password_button.click()

        # Wait for response/update
        self.page.wait_for_timeout(2000)

        return True

    #logout

    def verify_logout_popup(self):
        # Click Admin
        self.page.locator(
            DashboardLocators.ADMIN_BUTTON
        ).click()

        self.page.wait_for_timeout(1000)

        # Click Logout
        self.page.locator(
            DashboardLocators.LOGOUT_BUTTON
        ).click()

        # Verify confirmation popup
        expect(
            self.page.locator(
                DashboardLocators.CONFIRM_LOGOUT_TITLE
            )
        ).to_be_visible()

        # Wait for 2 seconds (optional)
        self.page.wait_for_timeout(2000)

        # Click Cancel to close popup
        self.page.locator(
            DashboardLocators.CANCEL_BUTTON
        ).click()

        # Verify popup is closed
        expect(
            self.page.locator(
                DashboardLocators.CONFIRM_LOGOUT_TITLE
            )
        ).not_to_be_visible()

        return True

    def logout(self):
        """Log out, verify the public landing page, and open Login."""
        self.page.locator(
            DashboardLocators.ADMIN_BUTTON
        ).click()

        self.page.locator(
            DashboardLocators.LOGOUT_BUTTON
        ).click()

        dialog = self.page.get_by_role("dialog")
        expect(dialog).to_be_visible()
        expect(
            dialog.get_by_text("Confirm Logout", exact=True)
        ).to_be_visible()

        confirm_button = dialog.get_by_role(
            "button", name="Logout", exact=True
        )
        expect(confirm_button).to_be_visible()
        confirm_button.click()

        expect(self.page).to_have_url(re.compile(r"https?://[^/]+/?$"))
        expect(
            self.page.get_by_role(
                "heading",
                name=re.compile(
                    r"Try Running Your Field Team And Your Distributor Network",
                    re.IGNORECASE,
                ),
            )
        ).to_be_visible()

        public_login_button = self.page.get_by_role(
            "button", name="Login", exact=True
        )
        expect(public_login_button).to_be_visible()
        public_login_button.click()

        expect(self.page).to_have_url(re.compile(r".*/login/?$"))
        expect(
            self.page.get_by_role("heading", name="Welcome!", exact=True)
        ).to_be_visible()

    #account settings

    def verify_account_settings(self):
        # Open Admin menu
        self.page.locator(
            DashboardLocators.ADMIN_BUTTON
        ).click()

        self.page.wait_for_timeout(1000)

        # Click Account Settings
        self.page.locator(
            DashboardLocators.ACCOUNT_SETTINGS
        ).click()

        # Wait for Account Settings page
        self.page.wait_for_load_state("networkidle")

        # ============================
        # Configuration Hub
        # ============================

        expect(
            self.page.locator(
                DashboardLocators.CONFIGURATION_HUB
            )
        ).to_be_visible()

        # ============================
        # Search Box
        # ============================

        expect(
            self.page.locator(
                DashboardLocators.SEARCH_SETTINGS
            )
        ).to_be_visible()

        self.page.locator(
            DashboardLocators.SEARCH_SETTINGS
        ).fill("User Management")

        expect(
            self.page.locator(
                DashboardLocators.SEARCH_SETTINGS
            )
        ).to_have_value("User Management")

        expect(
            self.page.get_by_text(
                "Showing results matching",
                exact=False
            )
        ).to_be_visible()

        expect(
            self.page.get_by_role(
                "button",
                name="User Management: Manage users and their accounts for your tenant"
            )
        ).to_be_visible()

        # Clear Search
        self.page.locator(
            DashboardLocators.SEARCH_SETTINGS
        ).clear()

        self.page.wait_for_timeout(1000)

        # ============================
        # Organization & Access
        # ============================

        expect(
            self.page.get_by_role(
                "heading",
                name="Organization & Access"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "Feature Permission",
                exact=True
            ).first
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "User Management",
                exact=True
            ).first
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "Role Management",
                exact=True
            ).first
        ).to_be_visible()

        # ============================
        # Financial Configuration
        # ============================

        expect(
            self.page.get_by_role(
                "heading",
                name="Financial Configuration"
            )
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "Fare Configuration",
                exact=True
            ).first
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "Claim Eligibility Amount Management",
                exact=True
            ).first
        ).to_be_visible()

        expect(
            self.page.get_by_text(
                "Partner Benefits",
                exact=True
            ).first
        ).to_be_visible()
        # ============================
        # Branding & Templates
        # ============================

        # Scroll down to Branding & Templates
        self.page.locator(
            DashboardLocators.BRANDING_TEMPLATES
        ).scroll_into_view_if_needed()

        expect(
            self.page.locator(
                DashboardLocators.BRANDING_TEMPLATES
            )
        ).to_be_visible()

        # Verify Announcements card
        expect(
            self.page.locator(
                DashboardLocators.ANNOUNCEMENTS
            )
        ).to_be_visible()

        # ============================
        # Logos and Brand
        # ============================

        # Scroll to Logos and Brand section
        self.page.locator(
            DashboardLocators.LOGOS_AND_BRAND
        ).scroll_into_view_if_needed()

        # Verify Logos and Brand heading
        expect(
            self.page.locator(
                DashboardLocators.LOGOS_AND_BRAND
            )
        ).to_be_visible()

        # Verify Company Logo card
        expect(
            self.page.locator(
                DashboardLocators.COMPANY_LOGO
            )
        ).to_be_visible()

        # Verify Tenant Template Management card
        expect(
            self.page.locator(
                DashboardLocators.TENANT_TEMPLATE_MANAGEMENT
            )
        ).to_be_visible()
        # ============================
        # System & Operations
        # ============================

        # Verify System & Operations heading
        expect(
            self.page.get_by_role(
                "heading",
                name="System & Operations"
            )
        ).to_be_visible()

        # Verify PMS Configuration card
        expect(
            self.page.get_by_role(
                "button",
                name="PMS Configuration: Configure Performance Management System for your tenant"
            )
        ).to_be_visible()

        # ============================
        # Categories & Modules
        # ============================

        # Verify Categories chip
        # Verify Categories chip
        expect(
            self.page.locator(
                DashboardLocators.CATEGORIES_CHIP
            )
        ).to_be_visible()

        # Verify Modules chip
        modules = self.page.locator(DashboardLocators.MODULES_CHIP).first
        expect(modules).to_be_visible(timeout=10000)

        # Verify Expand All button
        expect(
            self.page.locator(
                DashboardLocators.EXPAND_ALL
            )
        ).to_be_visible()

        # Verify Collapse All button
        expect(
            self.page.locator(
                DashboardLocators.COLLAPSE_ALL
            )
        ).to_be_visible()

        # ============================
        # Verify Expand All works
        # ============================

        self.page.locator(
            DashboardLocators.EXPAND_ALL
        ).click()

        self.page.wait_for_timeout(1500)

        expect(
            self.page.locator(
                DashboardLocators.ORGANIZATION_ACCESS
            )
        ).to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.FINANCIAL_CONFIGURATION
            )
        ).to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.BRANDING_TEMPLATES
            )
        ).to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.LOGOS_AND_BRAND
            )
        ).to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.SYSTEM_OPERATIONS
            )
        ).to_be_visible()

        # ============================
        # Verify Collapse All works
        # ============================

        self.page.locator(
            DashboardLocators.COLLAPSE_ALL
        ).click()

        self.page.wait_for_timeout(1500)

        # Verify cards are collapsed by checking child cards disappear

        expect(
            self.page.locator(
                DashboardLocators.FEATURE_PERMISSION
            )
        ).not_to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.FARE_CONFIGURATION
            )
        ).not_to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.ANNOUNCEMENTS
            )
        ).not_to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.COMPANY_LOGO
            )
        ).not_to_be_visible()

        expect(
            self.page.locator(
                DashboardLocators.PMS_CONFIGURATION
            )
        ).not_to_be_visible()

        # Return to Dashboard
        self.page.go_back()

        self.page.wait_for_load_state("networkidle")

        return True
    #partnerverification

    def open_partner_verification(self):

        # Already on Partner Verification page
        if "partner-verification" in self.page.url:
            heading = self.page.get_by_role(
                "heading",
                name="Partner Verification",
                exact=True
            )

            expect(heading).to_be_visible(timeout=15000)

            return True

        # Open Partner Verification from sidebar
        partner = self.page.get_by_role(
            "button",
            name="Partner Verification",
            exact=True
        )

        expect(partner).to_be_visible(timeout=10000)

        partner.click()

        # Verify page heading
        heading = self.page.get_by_role(
            "heading",
            name="Partner Verification",
            exact=True
        )

        expect(heading).to_be_visible(timeout=15000)

        return True
    #field executive
    def open_field_executive_dashboard(self):

        field = self.page.locator(
            DashboardLocators.FIELD_EXECUTIVE
        ).first

        # Expand only if Dashboard submenu isn't visible
        if not self.page.locator(
                DashboardLocators.FIELD_EXECUTIVE_DASHBOARD
        ).first.is_visible():
            field.click()

        self.page.locator(
            DashboardLocators.FIELD_EXECUTIVE_DASHBOARD
        ).first.click()

    def verify_partner_user_management(self):
            # Go to Admin Dashboard
            self.page.goto(
                "https://ayksadev-adminportal.onrender.com/dashboard/admin-dashboard"
            )

            # Wait for DOM only
            self.page.wait_for_load_state("domcontentloaded")

            # Wait for Partner User Management menu
            partner_user = self.page.get_by_role(
                "button",
                name="Partner User Management"
            )

            partner_user.click()

            self.page.wait_for_timeout(2000)

            assert "partner-user-management" in self.page.url

            return True

    def open_hr_module(self):

        # If already expanded, don't click again
        if self.page.get_by_role("button", name="HR Dashboard").count() > 0:
            return True

        hr = self.page.get_by_role(
            "button",
            name="HR",
            exact=True
        ).first

        expect(hr).to_be_visible(timeout=10000)

        hr.click()

        expect(
            self.page.get_by_role(
                "button",
                name="HR Dashboard"
            )
        ).to_be_visible(timeout=10000)

        return True

    def open_employee_management(self):

        # Expand HR if Employee Management is not visible
        employee_menu = self.page.get_by_role(
            "button",
            name="Employee Management"
        )

        if employee_menu.count() == 0 or not employee_menu.first.is_visible():
            hr = self.page.get_by_role(
                "button",
                name="HR",
                exact=True
            ).first

            expect(hr).to_be_visible(timeout=10000)
            hr.click()

        employee_menu = self.page.get_by_role(
            "button",
            name="Employee Management"
        ).first

        expect(employee_menu).to_be_visible(timeout=10000)

        employee_menu.click()

        self.page.wait_for_load_state("networkidle")

        return True