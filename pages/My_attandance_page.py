# import re
#
# from playwright.sync_api import expect
# from locators.My_attendance_locators import MyAttendanceLocators
#
#
# class MyAttendancePage:
#
#     def __init__(self, page):
#         self.page = page
#
#     def open_my_attendance(self):
#         field_executive = self.page.get_by_role(
#             "button",
#             name="Field Executive"
#         ).first
#
#         expect(field_executive).to_be_visible()
#         field_executive.click()
#
#         my_attendance = self.page.get_by_role(
#             "button",
#             name="My Attendance"
#         ).first
#
#         expect(my_attendance).to_be_visible()
#         my_attendance.click()
#
#     def verify_my_attendance_page(self):
#         expect(
#             self.page.get_by_role(
#                 "heading",
#                 name="My Attendance Records"
#             )
#         ).to_be_visible(timeout=10000)
#
#         return True
#
#     def __init__(self, page):
#         self.page = page
#
#     def verify_clock_in_heading(self):
#         heading = self.page.get_by_role(
#             "heading",
#             name="Hey ADMIN, Let's Clock-In!"
#         )
#
#         expect(heading).to_be_visible()
#
#         return True
#
#     def verify_clock_in_sub_heading(self):
#         sub_heading = self.page.get_by_role(
#             "heading",
#             name="Don't miss your clock in schedule"
#         )
#
#         expect(sub_heading).to_be_visible()
#
#         return True
#
#     def verify_clock_in_section(self):
#         expect(
#             self.page.get_by_role(
#                 "heading",
#                 name="Hey ADMIN, Let's Clock-In!"
#             )
#         ).to_be_visible()
#
#         expect(
#             self.page.get_by_role(
#                 "heading",
#                 name="Don't miss your clock in schedule"
#             )
#         ).to_be_visible()
#
#         return True
#
#     def verify_ready_to_clock_in_section(self):
#         # Heading
#         expect(
#             self.page.get_by_role(
#                 "heading",
#                 name="Ready to Clock In?"
#             )
#         ).to_be_visible()
#
#         # Description
#         expect(
#             self.page.get_by_text(
#                 "Start your day with purpose and make every moment count."
#             )
#         ).to_be_visible()
#
#         return True
#
#     def verify_date_and_time(self):
#         # Date label
#         expect(
#             self.page.get_by_text("Date", exact=True)
#         ).to_be_visible()
#
#         # Date value
#         date_value = self.page.locator(
#             "//p[text()='Date']/following-sibling::p"
#         )
#
#         expect(date_value).to_be_visible()
#
#         # Time label
#         expect(
#             self.page.get_by_text("Time", exact=True)
#         ).to_be_visible()
#
#         # Time value
#         time_value = self.page.locator(
#             "//p[text()='Time']/following-sibling::p"
#         )
#
#         expect(time_value).to_be_visible()
#
#         # Validate Date is not empty
#         assert date_value.inner_text().strip() != ""
#
#         # Validate Time format (e.g. 10:47:24 AM)
#         assert re.match(
#             r"\d{1,2}:\d{2}:\d{2}\s?(AM|PM)",
#             time_value.inner_text().strip()
#         )
#
#         return True
#
#     def click_choose_transport(self):
#         self.page.locator(
#             MyAttendanceLocators.CHOOSE_TRANSPORT_BUTTON
#         ).click()
#
#     def select_transport_and_confirm(self):
#         # Open popup
#         self.page.locator(
#             MyAttendanceLocators.CHOOSE_TRANSPORT_BUTTON
#         ).click()
#
#         # Open dropdown
#         self.page.locator(
#             MyAttendanceLocators.TRANSPORT_DROPDOWN
#         ).click()
#
#         # Wait for popup options
#         self.page.wait_for_timeout(1000)
#
#         # Select Car
#         self.page.get_by_text("Car", exact=True).click()
#
#         # Confirm button becomes enabled
#         confirm = self.page.get_by_role(
#             "button",
#             name="Confirm Selection"
#         )
#
#         expect(confirm).to_be_enabled()
#
#         confirm.click()
#
#         return True
#
#     def verify_today_status_card(self):
#         expect(
#             self.page.locator(MyAttendanceLocators.TODAY_STATUS)
#         ).to_be_visible()
#
#         expect(
#             self.page.locator(MyAttendanceLocators.TRANSPORT_MODE)
#         ).to_be_visible()
#
#         expect(
#             self.page.locator(MyAttendanceLocators.SESSIONS_TODAY)
#         ).to_be_visible()
#
#         expect(
#             self.page.locator(MyAttendanceLocators.CURRENT_TIME)
#         ).to_be_visible()
#
#         return True
#
#     def verify_check_in_button(self):
#         button = self.page.locator(
#             MyAttendanceLocators.CHECK_IN_BUTTON
#         )
#
#         expect(button).to_be_visible()
#
#         expect(button).to_be_enabled()
#
#         return True
#
#     def verify_current_time_running(self):
#         current_time = self.page.locator(
#             MyAttendanceLocators.CURRENT_TIME_VALUE
#         )
#
#         time1 = current_time.inner_text()
#
#         self.page.wait_for_timeout(3000)
#
#         time2 = current_time.inner_text()
#
#         print("Time 1:", time1)
#         print("Time 2:", time2)
#
#         return time1 != time2