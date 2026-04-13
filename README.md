# AutoGuard

A scalable test automation framework designed to identify root causes of test flakiness and enforce strict code coverage requirements before deployment. Built with pytest and Selenium for comprehensive web application testing.

## Architecture Overview

AutoGuard implements a robust, scalable testing framework that combines:

- **Flakiness Detection**: Advanced algorithms to identify and root-cause intermittent test failures
- **Coverage Enforcement**: Strict code coverage requirements prevent deployment of untested code
- **Cross-Browser Testing**: Parallel execution across multiple browsers and versions
- **CI/CD Integration**: Seamless integration with GitHub Actions for automated testing

## Key Features

### Root Cause Analysis for Flakiness

AutoGuard employs multiple strategies to identify and eliminate test flakiness:

#### Timing-Based Analysis
- **Execution Time Tracking**: Monitors test execution times to detect performance-related flakiness
- **Retry Logic with Analysis**: Failed tests are retried with detailed logging to identify patterns
- **Network Latency Detection**: Identifies tests that fail due to network timing issues

#### Environment Stability Checks
- **Browser State Validation**: Ensures clean browser state between tests
- **Resource Cleanup Verification**: Confirms proper teardown of test resources
- **Concurrent Execution Analysis**: Detects race conditions in parallel test runs

#### Statistical Analysis
- **Failure Pattern Recognition**: Uses statistical methods to identify recurring failure patterns
- **Confidence Intervals**: Calculates reliability scores for each test
- **Trend Analysis**: Tracks test stability over time

### Strict Code Coverage Enforcement

#### Coverage Requirements
- **Minimum 80% Code Coverage**: Enforced before any deployment
- **Branch Coverage**: Ensures all conditional branches are tested
- **Line Coverage**: Validates execution of all code lines

#### Coverage Analysis
- **HTML Reports**: Detailed coverage reports with visual indicators
- **Missing Lines Identification**: Pinpoints untested code paths
- **Coverage Trends**: Tracks coverage improvements over time

## Project Structure

```
AutoGuard/
├── .gitignore                    # Ignores cache, logs, reports
├── requirements.txt              # pytest, selenium, coverage tools
├── pytest.ini                   # Test configuration with HTML reporting
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # GitHub Actions CI/CD pipeline
├── tests/
│   ├── conftest.py              # Selenium WebDriver fixtures
│   └── test_crm_login.py        # CRM login test suite
└── README.md
```

## Setup & Installation

### Prerequisites

- Python 3.8+
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (auto-managed in CI)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoGuard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install browser drivers**
   ```bash
   # For Chrome
   pip install webdriver-manager

   # Or manually download from:
   # Chrome: https://chromedriver.chromium.org/
   # Firefox: https://github.com/mozilla/geckodriver/releases
   ```

## Test Execution

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_crm_login.py
```

### Run Tests in Specific Browser

```bash
# Chrome (default)
pytest

# Firefox
BROWSER=firefox pytest
```

### Generate HTML Report

```bash
pytest --html=reports/report.html
```

## Test Configuration

### pytest.ini Configuration

```ini
[tool:pytest]
testpaths = tests
addopts =
    --html=reports/report.html
    --cov=.
    --cov-report=html:reports/coverage.html
    --cov-fail-under=80
```

### Custom Markers

- `@pytest.mark.slow`: Mark slow-running tests
- `@pytest.mark.integration`: Mark integration tests
- `@pytest.mark.smoke`: Mark smoke tests

## CI/CD Pipeline

### GitHub Actions Workflow

The framework includes a comprehensive CI/CD pipeline that:

1. **Matrix Testing**: Tests across multiple Python versions (3.8-3.11) and browsers
2. **Parallel Execution**: Runs tests in parallel for faster feedback
3. **Coverage Enforcement**: Fails builds with <80% coverage
4. **Artifact Upload**: Saves test reports and coverage data
5. **Staging Deployment**: Automatic deployment to staging on main branch pushes

### Pipeline Stages

#### Test Stage
- Multi-version Python testing
- Cross-browser validation
- Coverage analysis
- HTML report generation

#### Coverage Stage
- Consolidated coverage reporting
- Codecov integration
- Coverage threshold enforcement

#### Deploy Stage
- Staging environment deployment
- Smoke test execution
- Rollback capabilities

## Test Examples

### Basic Login Test

```python
def test_successful_login(self, setup_teardown):
    driver = setup_teardown
    driver.get("https://example-crm.com/login")

    # Enter credentials
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("test@example.com")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("password123")

    # Submit login
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # Verify success
    dashboard = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard"))
    )
    assert dashboard.is_displayed()
```

### Flakiness Detection

The framework automatically detects flaky tests by:

1. **Retry Logic**: Failed tests are retried up to 3 times
2. **Pattern Analysis**: Identifies tests that pass on retry
3. **Root Cause Logging**: Captures browser state, network conditions, and timing data

### Coverage Analysis

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Browser Support

- **Chrome**: Primary browser with headless support
- **Firefox**: Alternative browser for cross-browser validation
- **Headless Mode**: All browsers run in headless mode for CI compatibility

## Configuration

### Environment Variables

```bash
# Browser selection
BROWSER=chrome  # or firefox

# Test environment
TEST_ENV=staging  # or production

# Parallel execution
PYTEST_XDIST_AUTO_NUM_WORKERS=4
```

### Custom Fixtures

The `conftest.py` provides reusable fixtures:

- `browser`: WebDriver instance with automatic cleanup
- `setup_teardown`: Per-test setup and teardown
- `session_setup`: Session-wide configuration

## Best Practices

### Writing Reliable Tests

1. **Use Explicit Waits**: Avoid sleep() calls, use WebDriverWait
2. **Unique Selectors**: Use data-testid or unique IDs for elements
3. **Page Object Model**: Organize tests with page object patterns
4. **Data Isolation**: Use unique test data to avoid conflicts

### Flakiness Prevention

1. **Stable Selectors**: Prefer ID and data attributes over CSS/XPath
2. **Wait Strategies**: Use presence_of_element_located over visibility
3. **State Verification**: Always verify application state, not just UI
4. **Cleanup**: Ensure proper test isolation and cleanup

### Coverage Optimization

1. **Test Critical Paths**: Focus coverage on business-critical code
2. **Edge Cases**: Include tests for error conditions and edge cases
3. **Integration Tests**: Complement unit tests with integration coverage
4. **Regular Reviews**: Audit coverage reports regularly

## Troubleshooting

### Common Issues

#### WebDriver Errors
- Ensure browser drivers are installed and in PATH
- Check browser version compatibility
- Use webdriver-manager for automatic driver management

#### Flaky Tests
- Review timing issues and use explicit waits
- Check for race conditions in test setup
- Analyze browser console logs for JavaScript errors

#### Coverage Issues
- Run `pytest --cov-report=term-missing` to identify uncovered lines
- Add tests for conditional branches and error paths
- Exclude third-party code from coverage requirements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure coverage remains >80%
5. Run the full test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **pytest**: Comprehensive testing framework
- **Selenium**: Web browser automation
- **pytest-cov**: Code coverage reporting
- **pytest-html**: HTML test reporting
- **GitHub Actions**: CI/CD platform