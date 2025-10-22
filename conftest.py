import pytest
import os
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Create a 'screenshots' directory if it doesn't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Create an 'allure-results' directory if it doesn't exist
if not os.path.exists('allure-results'):
    os.makedirs('allure-results')

# Create a 'downloads' directory if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')


@pytest.fixture(scope="function")
def driver():
    """
    Main fixture to set up and tear down the WebDriver instance for each test.
    """
    download_dir = os.path.abspath('downloads')
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run tests in headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")

    # Configure download preferences
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    web_driver = webdriver.Chrome(options=chrome_options)

    yield web_driver

    # Teardown: This code runs after each test
    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot and attach to Allure report on test failure.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        try:
            # Try to get the driver from the test's 'driver' fixture
            web_driver = item.funcargs['driver']

            # Define screenshot path
            screenshot_name = f"{item.name}.png"
            screenshot_path = os.path.join('screenshots', screenshot_name)

            # FIX: Wrap screenshot in a try/except block.
            # This prevents a new ERROR if the browser has already crashed.
            try:
                web_driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")

                # Attach screenshot to Allure report
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot on failure",
                    attachment_type=AttachmentType.PNG
                )
            except Exception as e:
                print(f"Could not take screenshot. Browser may have crashed: {e}")

        except Exception as e:
            print(f"Error in screenshot/Allure hook: {e}")

