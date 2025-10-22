import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import JavascriptException


def remove_ads_and_footer(driver):
    """Helper function to remove footer and ad elements that can block interactions."""
    try:
        driver.execute_script("document.querySelector('footer').remove();")
        driver.execute_script("document.getElementById('fixedban').remove();")
    except JavascriptException:
        pass
    time.sleep(0.5)


def test_slider(driver):
    """
    Covers:
    - SLIDER WIDGET
    """
    driver.get("https://demoqa.com/slider")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    slider = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "range-slider")))

    # Get the initial value
    slider_value = driver.find_element(By.ID, "sliderValue")
    print(f"Initial slider value: {slider_value.get_attribute('value')}")

    actions = ActionChains(driver)
    # Move the slider. The move_by_offset x value is pixels.
    actions.click_and_hold(slider).move_by_offset(50, 0).release().perform()

    # Verify the value has changed
    new_value = slider_value.get_attribute('value')
    print(f"New slider value: {new_value}")
    assert new_value != "25", "Slider value did not change."


def test_date_picker(driver):
    """
    Covers:
    - DATE PICKER WIDGET
    """
    driver.get("https://demoqa.com/date-picker")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    date_input = wait.until(EC.element_to_be_clickable((By.ID, "datePickerMonthYearInput")))
    date_input.click()

    # Select a month and year
    month_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-select")))
    month_dropdown.click()
    driver.find_element(By.XPATH, "//option[@value='2']").click()  # March

    year_dropdown = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_dropdown.click()
    driver.find_element(By.XPATH, "//option[@value='2025']").click()  # 2025

    # Select a day
    driver.find_element(By.CLASS_NAME, "react-datepicker__day--015").click()  # 15th

    # Verify the date
    selected_date = date_input.get_attribute("value")
    assert "03/15/2025" in selected_date
    print(f"Successfully selected date: {selected_date}")


def test_autocomplete(driver):
    """
    Covers:
    - AUTOCOMPLETE WIDGET
    """
    driver.get("https://demoqa.com/auto-complete")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    autocomplete_input = wait.until(EC.visibility_of_element_located((By.ID, "autoCompleteMultipleInput")))

    # Type into the input to trigger options
    autocomplete_input.send_keys("r")
    time.sleep(1)  # Wait for options to appear

    # Navigate and select an option using keyboard
    autocomplete_input.send_keys(Keys.DOWN)
    autocomplete_input.send_keys(Keys.ENTER)

    # Verify the selected color chip appeared
    selected_value = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "auto-complete__multi-value__label"))).text
    # FIX: The first option when typing "r" is "Green", not "Red".
    assert "Green" in selected_value
    print(f"Successfully selected autocomplete value: {selected_value}")

