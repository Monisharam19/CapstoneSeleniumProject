import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def remove_ads_and_footer(driver):
    """Helper function to remove elements that can block interactions."""
    try:
        driver.execute_script("document.querySelector('footer').remove();")
        driver.execute_script("document.getElementById('fixedban').remove();")
    except Exception:
        pass  # Ignore errors if elements don't exist
    time.sleep(0.5)


@pytest.mark.elements
def test_checkboxes(driver):
    """
    Covers:
    - CHECK BOX
    """
    wait = WebDriverWait(driver, 20)

    driver.get("https://demoqa.com/checkbox")
    remove_ads_and_footer(driver)

    # Expand the folder tree to make the checkbox visible
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rct-option-expand-all"))).click()

    # Click the 'Documents' checkbox
    documents_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='tree-node-documents']")))
    documents_checkbox.click()

    # Verify the success message
    result_text = wait.until(EC.visibility_of_element_located((By.ID, "result"))).text
    assert "documents" in result_text
    print("Successfully verified checkbox selection.")


@pytest.mark.elements
def test_dropdown(driver):
    """
    Covers:
    - DROP DOWN
    """
    wait = WebDriverWait(driver, 20)
    driver.get("https://demoqa.com/select-menu")
    remove_ads_and_footer(driver)

    # Use the Select class for traditional <select> dropdowns
    old_style_select = Select(wait.until(EC.visibility_of_element_located((By.ID, "oldSelectMenu"))))

    # Select the "Green" option
    old_style_select.select_by_visible_text("Green")

    # Verify the selection by checking the selected option's text
    selected_option = old_style_select.first_selected_option
    assert selected_option.text == "Green"
    print("Successfully verified dropdown selection.")


@pytest.mark.elements
def test_web_table(driver):
    """
    Covers:
    - WEB TABLE
    """
    driver.get("https://demoqa.com/webtables")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    # XPath to locate the email cell in the row containing "Cierra"
    email_cell = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='rt-tr-group'][.//div[text()='Cierra']]//div[@class='rt-td'][4]")
    ))

    assert "cierra@example.com" in email_cell.text
    print(f"Successfully verified Cierra's email in the web table: {email_cell.text}")


# FIX 1: Mark this test as 'flaky' to automatically retry it on intermittent failures.
@pytest.mark.flaky(reruns=2, reruns_delay=3)
@pytest.mark.navigation
def test_window_handling(driver):
    """
    Covers:
    - WINDOW HANDLING
    """
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 20)

    driver.get("https://demoqa.com/browser-windows")
    remove_ads_and_footer(driver)

    # Store the handle of the original window
    original_window = driver.current_window_handle

    # Click the button to open a new tab
    wait.until(EC.element_to_be_clickable((By.ID, "tabButton"))).click()

    # Wait for the new window/tab to open and switch to it
    wait.until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    # FIX 2: Remove ads on the *new* tab as well, as this can cause crashes
    remove_ads_and_footer(driver)

    # Verify content in the new tab
    new_tab_text = wait.until(EC.visibility_of_element_located((By.ID, "sampleHeading"))).text
    assert "This is a sample page" in new_tab_text
    print("Successfully switched to new tab and verified content.")

    # Close the new tab and switch back to the original
    driver.close()
    driver.switch_to.window(original_window)

    # Verify we are back on the original page
    original_page_text = wait.until(EC.visibility_of_element_located((By.ID, "tabButton"))).text
    assert "New Tab" in original_page_text
    print("Successfully closed new tab and returned to original window.")

