# class MyAttendanceLocators:
#
#     # Left Menu
#     FIELD_EXECUTIVE = "//span[normalize-space()='Field Executive']"
#     MY_ATTENDANCE = "//span[normalize-space()='My Attendance']"
#
#     # Attendance Page
#     ATTENDANCE_RECORDS = "//h4[contains(text(),'My Attendance Records')]"
#     # Ready to Clock In
#     READY_TO_CLOCK_IN = "h4:text('Ready to Clock In?')"
#
#     READY_TO_CLOCK_IN_TEXT = (
#         "text=Start your day with purpose and make every moment count."
#     )
#
#     # Date
#     DATE_LABEL = "//p[normalize-space()='Date']"
#     DATE_VALUE = "//p[normalize-space()='Date']/following-sibling::p"
#
#     # Time
#     TIME_LABEL = "//p[normalize-space()='Time']"
#     TIME_VALUE = "//p[normalize-space()='Time']/following-sibling::p"
#     CHOOSE_TRANSPORT_BUTTON = "button:has-text('Choose transport')"
#
#     TRANSPORT_DIALOG = "div[role='dialog']"
#
#     # Replace "Car" with any option available in your dropdown
#     TRANSPORT_OPTION = "//li[normalize-space()='Car']"
#     TRANSPORT_DROPDOWN = "div[role='combobox']"
#     CAR_OPTION = "text=Car"
#     CONFIRM_SELECTION = "button:has-text('Confirm Selection')"
#     TODAY_STATUS = "//h6[normalize-space()=\"Today's Status\"]"
#
#     TRANSPORT_MODE = "//span[contains(text(),'Car')]"
#
#     SESSIONS_TODAY = "//span[contains(normalize-space(),'Sessions Today')]"
#
#     CURRENT_TIME = "//span[contains(normalize-space(),'Current Time')]"
#
#     CHECK_IN_TIME = "//span[contains(normalize-space(),'Check-In Time')]"
#
#     CHECK_OUT_TIME = "//span[contains(normalize-space(),'Check-Out Time')]"
#
#     TOTAL_WORKING_HOURS = "//div[contains(.,'Total Working Hours')]"
#
#     CHECK_IN_BUTTON = "//button[contains(.,'Check In')]"
#     CURRENT_TIME_VALUE = (
#         "//span[contains(text(),'Current Time')]/preceding-sibling::h6"
#     )