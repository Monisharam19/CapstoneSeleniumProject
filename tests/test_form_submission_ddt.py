from pages.form_page import FormPage
import time
import pytest
from selenium.common.exceptions import JavascriptException


def remove_ads_and_footer(driver):
    """Helper function to remove elements that can block interactions."""
    try:
        driver.execute_script("document.querySelector('footer').remove();")
        driver.execute_script("document.getElementById('fixedban').remove();")
    except JavascriptException:
        pass  # Ignore errors if elements don't exist
    time.sleep(0.5)


# --- Data for the parameterized test ---
test_data = [
    ("Jane", "Doe", "jane.doe@example.com", "9876543210"),
    ("Peter", "Jones", "peter.jones@example.net", "1122334455")
]


@pytest.mark.parametrize("first_name, last_name, email, mobile", test_data)
def test_form_submission(driver, first_name, last_name, email, mobile):
    """
    Tests a simple form submission using the Page Object Model with multiple data sets.
    """
    form_page = FormPage(driver)

    # --- Test Steps ---
    form_page.load()
    remove_ads_and_footer(driver)

    form_page.enter_first_name(first_name)
    form_page.enter_last_name(last_name)
    form_page.enter_email(email)
    form_page.select_gender()
    form_page.enter_mobile_number(mobile)
    form_page.submit_form()

    # --- Assertion ---
    confirmation_text = form_page.get_confirmation_text()
    assert "Thanks for submitting the form" in confirmation_text
    print(f"Successfully verified form submission for {first_name} {last_name} with message: '{confirmation_text}'")

