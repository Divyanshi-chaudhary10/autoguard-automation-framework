import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

@pytest.fixture(scope="session")
def browser():
    """Fixture to provide WebDriver instance."""
    browser_name = os.getenv("BROWSER", "chrome").lower()

    if browser_name == "chrome":
        options = Options()
        options.add_argument("--headless")  # Run in headless mode for CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver

    # Teardown
    driver.quit()

@pytest.fixture(scope="function")
def setup_teardown(browser):
    """Fixture for test setup and teardown."""
    # Setup - could include navigation to base URL, login, etc.
    yield browser
    # Teardown - cleanup after each test
    # browser.delete_all_cookies()  # Example cleanup

@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """Session-wide setup and teardown."""
    # Setup - could include database setup, test data preparation
    yield
    # Teardown - cleanup after all tests
    pass