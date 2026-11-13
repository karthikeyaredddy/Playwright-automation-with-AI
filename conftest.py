import os
import re

import pytest
from playwright.sync_api import sync_playwright

from config.config import BASE_URL
from pages.login_page import LoginPage
from utils.logger import get_logger
logger = get_logger("Pytest")


# ============================================================
# Playwright Fixture
# ============================================================

@pytest.fixture(scope="session")
def playwright():
    """
    Starts Playwright once for the entire test session.
    """
    with sync_playwright() as p:
        yield p


# ============================================================
# Browser Fixture
# ============================================================

@pytest.fixture(scope="session")
def browser(playwright):
    """
    Launches Chromium once for the entire test session.
    """
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=300,
        args=["--start-maximized"]
    )

    yield browser

    browser.close()


# ============================================================
# Page Fixture
# ============================================================

@pytest.fixture(scope="function")
def page(browser):
    """
    Creates a fresh browser context and page for each test.

    Use this fixture for tests that perform login themselves.
    """
    context = browser.new_context(
        viewport=None
    )

    page = context.new_page()

    page.set_default_timeout(120000)
    page.set_default_navigation_timeout(120000)

    yield page

    context.close()


# ============================================================
# Logged-In Page Fixture
# ============================================================

@pytest.fixture(scope="session")
def logged_in_page(browser):
    """
    Logs in once using Chromium for all authenticated tests.
    """

    context = browser.new_context(
        viewport=None
    )

    page = context.new_page()

    page.set_default_timeout(120000)
    page.set_default_navigation_timeout(120000)

    # Open Login Page
    page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=120000
    )

    # Login
    login = LoginPage(page)
    login.login("admin")

    # Wait until dashboard fully loads
    page.wait_for_load_state("networkidle")

    yield page

    context.close()


# ============================================================
# Automatic Screenshot on Test Failure
# ============================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically takes a screenshot whenever a test fails.
    """

    # Execute the test and get the result
    outcome = yield
    report = outcome.get_result()

    # Take screenshot only when the actual test fails
    if report.when == "call" and report.failed:

        # Check normal page fixture
        page = item.funcargs.get("page")

        # Check logged-in page fixture
        if page is None:
            page = item.funcargs.get("logged_in_page")

        # If a Playwright page exists
        if page is not None:

            # Create screenshots/failed directory
            screenshot_dir = os.path.join(
                os.path.dirname(__file__),
                "screenshots",
                "failed"
            )

            os.makedirs(
                screenshot_dir,
                exist_ok=True
            )

            # Convert test name into a safe filename
            test_name = re.sub(
                r"[^a-zA-Z0-9_-]",
                "_",
                item.nodeid
            )

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{test_name}.png"
            )

            # Take screenshot
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            print(
                f"\n❌ Test failed."
                f"\n📸 Screenshot saved at:"
                f"\n{os.path.abspath(screenshot_path)}"
            )
# ============================================================
# Automatic Screenshot + Logging on Test Failure
# ============================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call":

        test_name = item.nodeid

        # ====================================================
        # PASSED
        # ====================================================

        if report.passed:

            logger.info(
                f"PASSED | {test_name}"
            )

        # ====================================================
        # FAILED
        # ====================================================

        elif report.failed:

            logger.error(
                f"FAILED | {test_name}"
            )

            # Get page fixture
            page = item.funcargs.get("page")

            # Get logged-in page fixture
            if page is None:
                page = item.funcargs.get("logged_in_page")

            if page is not None:

                screenshot_dir = os.path.join(
                    os.path.dirname(__file__),
                    "reports",
                    "screenshots",
                    "failed"
                )

                os.makedirs(
                    screenshot_dir,
                    exist_ok=True
                )

                test_name_safe = re.sub(
                    r"[^a-zA-Z0-9_-]",
                    "_",
                    item.nodeid
                )

                screenshot_path = os.path.join(
                    screenshot_dir,
                    f"{test_name_safe}.png"
                )

                try:

                    page.screenshot(
                        path=screenshot_path,
                        full_page=True
                    )

                    logger.error(
                        f"Screenshot saved | {screenshot_path}"
                    )

                    print(
                        f"\n❌ Test failed"
                        f"\n📸 Screenshot saved at:"
                        f"\n{screenshot_path}"
                    )

                except Exception as e:

                    logger.error(
                        f"Could not capture screenshot | {str(e)}"
                    )

        # ====================================================
        # SKIPPED
        # ====================================================

        elif report.skipped:

            logger.warning(
                f"SKIPPED | {test_name}"
            )