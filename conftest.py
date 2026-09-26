import pytest
from playwright.sync_api import sync_playwright

from config.config import BASE_URL
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright():
    """
    Starts Playwright once for the entire test session.
    """
    with sync_playwright() as p:
        yield p


@pytest.fixture(
    scope="session",
    params=["chromium", "firefox", "webkit"]
)
def browser(playwright, request):
    """
    Launches Chromium, Firefox, and WebKit.

    Each test will run once in:
        1. Chromium
        2. Firefox
        3. WebKit
    """

    browser_type = getattr(playwright, request.param)

    # Browser-specific launch arguments
    launch_args = []

    if request.param == "chromium":
        launch_args = ["--start-maximized"]

    browser = browser_type.launch(
        headless=False,
        slow_mo=300,
        args=launch_args
    )

    yield browser

    browser.close()


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


@pytest.fixture(scope="session")
def logged_in_page(browser):
    """
    Logs in once for each browser.

    Chromium:
        Login once -> run all authenticated tests

    Firefox:
        Login once -> run all authenticated tests

    WebKit:
        Login once -> run all authenticated tests
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