import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestCRMLogin:
    """Test suite for CRM login functionality."""

    def test_successful_login(self, setup_teardown):
        """Test successful login with valid credentials."""
        driver = setup_teardown

        # Navigate to login page (mock URL for demonstration)
        driver.get("https://example-crm.com/login")

        # Wait for login form to load
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Enter credentials
        username_field.send_keys("testuser@example.com")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("securepassword123")

        # Click login button
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Verify successful login - check for dashboard element
        try:
            dashboard_element = wait.until(
                EC.presence_of_element_located((By.ID, "dashboard"))
            )
            assert dashboard_element.is_displayed(), "Dashboard should be visible after login"
        except TimeoutException:
            pytest.fail("Login failed - dashboard not found within timeout")

    def test_invalid_credentials_login(self, setup_teardown):
        """Test login with invalid credentials."""
        driver = setup_teardown

        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Enter invalid credentials
        username_field.send_keys("invalid@example.com")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("wrongpassword")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Verify error message appears
        try:
            error_message = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            assert "invalid" in error_message.text.lower(), "Error message should mention invalid credentials"
        except TimeoutException:
            pytest.fail("Error message not displayed for invalid credentials")

    def test_empty_credentials_login(self, setup_teardown):
        """Test login with empty credentials."""
        driver = setup_teardown

        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )

        # Click login without entering credentials
        login_button.click()

        # Verify validation messages
        try:
            username_error = driver.find_element(By.ID, "username-error")
            assert username_error.is_displayed(), "Username validation error should be shown"
        except NoSuchElementException:
            pytest.fail("Username validation error not found")

    def test_password_visibility_toggle(self, setup_teardown):
        """Test password visibility toggle functionality."""
        driver = setup_teardown

        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        # Enter password
        password_field.send_keys("testpassword")

        # Find and click password visibility toggle
        toggle_button = driver.find_element(By.ID, "password-toggle")
        initial_type = password_field.get_attribute("type")

        toggle_button.click()
        time.sleep(0.5)  # Wait for toggle animation

        final_type = password_field.get_attribute("type")

        # Verify password field type changed
        assert initial_type != final_type, "Password field type should change when toggle is clicked"

    def test_remember_me_functionality(self, setup_teardown):
        """Test remember me checkbox functionality."""
        driver = setup_teardown

        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        remember_checkbox = wait.until(
            EC.presence_of_element_located((By.ID, "remember-me"))
        )

        # Verify checkbox is not selected by default
        assert not remember_checkbox.is_selected(), "Remember me should not be selected by default"

        # Click checkbox
        remember_checkbox.click()

        # Verify checkbox is now selected
        assert remember_checkbox.is_selected(), "Remember me should be selected after clicking"

    def test_forgot_password_link(self, setup_teardown):
        """Test forgot password link navigation."""
        driver = setup_teardown

        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        forgot_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot Password?"))
        )

        # Click forgot password link
        forgot_link.click()

        # Verify navigation to forgot password page
        wait.until(EC.url_contains("forgot-password"))
        assert "forgot-password" in driver.current_url, "Should navigate to forgot password page"

    @pytest.mark.slow
    def test_login_performance(self, setup_teardown):
        """Test login performance - should complete within 3 seconds."""
        driver = setup_teardown

        start_time = time.time()
        driver.get("https://example-crm.com/login")

        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        username_field.send_keys("perfuser@example.com")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("password123")

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Wait for dashboard
        wait.until(EC.presence_of_element_located((By.ID, "dashboard")))

        end_time = time.time()
        login_time = end_time - start_time

        assert login_time < 3.0, f"Login took {login_time:.2f} seconds, should be under 3 seconds"