class PartnerVerificationLocators:

    PARTNER_VERIFICATION_HEADING = "h1"
    SEARCH_BOX = "input[placeholder='Search name or phone…']"
    BASIC_DETAILS = "button:has-text('BASIC DETAILS')"

    BUSINESS_GST = "button:has-text('BUSINESS + GST')"

    DOCUMENTS = "button:has-text('DOCUMENTS')"


    STATE_FILTER = '[role="combobox"][aria-label="State"]'
    # Description
    PARTNER_VERIFICATION_DESCRIPTION = (
        "text=Review and verify partner applications before they move to the next stage."
    )
    PENDING_CHIP = "span:has-text('Pending')"
    VERIFIED_TODAY_CHIP = "span:has-text('Verified Today')"
    # State
    STATE_DROPDOWN = "input[placeholder='All States']"
    # Dropdown options
    DROPDOWN_OPTIONS = "[role='option']"
    INFO_MESSAGE = "div.MuiAlert-message"
    BASIC_DETAILS_TAB = "button:has-text('BASIC DETAILS')"
    BUSINESS_GST_TAB = "button:has-text('BUSINESS + GST')"
    DOCUMENTS_TAB = "button:has-text('DOCUMENTS')"
    INVALID_PARTNERS_TAB = "button:has-text('INVALID PARTNERS')"
    COMBOBOX = "[role='combobox']"
    ACTIVE_INVALID_BUTTON = "button:has-text('Active Invalid')"
    DEACTIVATED_BUTTON = "button:has-text('Deactivated')"

    SELECT_ALL_BUTTON = "button:has-text('Select All')"
    DEACTIVATE_SELECTED_BUTTON = "button:has-text('Deactivate Selected')"
    DEACTIVATE_ALL_BUTTON = "button:has-text('Deactivate All')"



    CLOSE_BUTTON = "button:has-text('Close')"
    # Basic Details
    NEEDS_ATTENTION = "text=Needs Attention"
    PHONE_NUMBER = "text=9876565646"
    APPROVE_BUTTON = "button:has-text('Approve')"
    REJECT_BUTTON = "button:has-text('Reject')"
    DECISION_SUMMARY = "text=Decision Summary"
    SAFE_TO_APPROVE = "text=Safe to approve"
    BASIC_DETAILS_POPUP = "//h6[normalize-space()='Basic Details']"
    NAME_INPUT = "input[type='text']"
    PHONE_TEXT = "text=9876565646"
    COPY_BUTTON = "button:has-text('Copy')"
    MARK_VERIFIED_BUTTON = "button:has-text('Mark Verified')"
    EMAIL_INPUT = "input[placeholder='Optional']"
    SAVE_BUTTON = "button:has-text('Save')"
    NEEDS_ATTENTION_BADGE = "text=Needs Attention"
    # Phone Section
    PHONE_LABEL = "text=PHONE"
    # Email
    EMAIL_LABEL = "text=EMAIL"
    # Additional Details
    ADDITIONAL_DETAILS = "text=Additional Details"
    # ==========================================================
    # Invalid Partners
    # ==========================================================

    INVALID_PARTNERS = "button:has-text('INVALID PARTNERS')"

    ALL_BUTTON = "button:text-is('All')"

    RESET_BUTTON = "button:has-text('Reset')"

    PARTNER_CARD = "div.MuiCard-root"

    PARTNER_NAME_HEADING = "p"

    # ==========================================================
    # Partner Audit Details
    # ==========================================================

    PARTNER_AUDIT_DETAILS = "h2:has-text('Partner Audit Details')"

    PARTNER_NAME = "text=Partner:"

    PHONE = "text=Phone:"

    CREATED_BY = "text=Created By:"

    CREATED_AT = "text=Created At:"

    REJECTED_BY = "text=Rejected By:"

    REJECTION_REASON = "text=Rejection Reason:"

    DEACTIVATED_BY = "text=Deactivated By:"

    DEACTIVATED_AT = "text=Deactivated At:"



    # ==========================================================
    # Basic Details - Partner Card
    # ==========================================================

    VIEW_DETAILS_BUTTON = "button:has-text('View Details')"



    # ==========================================================
    # Basic Details Modal
    # ==========================================================

    BASIC_DETAILS_MODAL_CLOSE = (
        "button[aria-label='Close basic verification modal']"
    )


    BASIC_DETAILS_SECTION = "text=Basic Details"



    # ==========================================================
    # Reject Partner Modal
    # ==========================================================

    REJECT_PARTNER_HEADING = "text=Reject Partner (Basic Details)"

    REJECTION_REMARK = (
        "textarea[placeholder='Enter reason for marking this partner as invalid']"
    )

    CANCEL_BUTTON = "button:has-text('CANCEL')"

    REJECT_PARTNER_BUTTON = "button:has-text('REJECT PARTNER')"


    # ==========================================================
    # Basic Details Popup
    # ==========================================================

    BASIC_DETAILS_CLOSE_BUTTON = (
        "button[aria-label='Close basic verification modal']"
    )



    CANCEL_REJECT_BUTTON = (
        "button:has-text('CANCEL')"
    )

    REJECT_PARTNER_CONFIRM_BUTTON = (
        "button:has-text('REJECT PARTNER')"
    )

