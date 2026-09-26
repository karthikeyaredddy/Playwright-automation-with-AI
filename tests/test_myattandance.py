# from pages.My_attandance_page import MyAttendancePage
#
#
# class TestMyAttendance:
#
#     def test_open_my_attendance(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         attendance.open_my_attendance()
#
#         assert attendance.verify_my_attendance_page()
#
#     def test_clock_in_heading(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_clock_in_heading()
#
#     def test_ready_to_clock_in_section(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_ready_to_clock_in_section()
#
#     def test_date_and_time(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_date_and_time()
#
#     def test_select_transport(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.select_transport_and_confirm()
#
#     def test_today_status_card(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_today_status_card()
#
#     def test_check_in_button(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_check_in_button()
#
#     def test_current_time_running(self, logged_in_page):
#         attendance = MyAttendancePage(logged_in_page)
#
#         assert attendance.verify_current_time_running()
