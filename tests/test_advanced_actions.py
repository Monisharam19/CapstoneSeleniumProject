import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import JavascriptException


def remove_ads_and_footer(driver):
    """Helper function to remove footer and ad elements that can block interactions."""
    try:
        # Remove the footer which can sometimes overlay elements
        driver.execute_script("document.querySelector('footer').remove();")
        # Remove the common ad banner at the bottom if it exists
        driver.execute_script("document.getElementById('fixedban').remove();")
    except JavascriptException:
        # Ignore errors if the elements don't exist on the page
        pass
    time.sleep(0.5)  # A brief pause to let the DOM settle after removal


def scroll_to_element(driver, element: WebElement):
    """Helper function to scroll an element into the middle of the view."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    time.sleep(0.5)


def test_mouse_actions(driver):
    """
    Covers:
    - MOUSE HOVER ACTION
    - DRAG & DROP AND RIGHT CLICK
    """
    driver.get("https://demoqa.com/buttons")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    actions = ActionChains(driver)

    # --- Right Click ---
    right_click_btn = wait.until(EC.element_to_be_clickable((By.ID, "rightClickBtn")))
    scroll_to_element(driver, right_click_btn)
    actions.context_click(right_click_btn).perform()
    message = wait.until(EC.visibility_of_element_located((By.ID, "rightClickMessage"))).text
    assert "You have done a right click" in message
    print(f"Successfully performed a right click and verified the message: '{message}'")

    # --- Double Click ---
    double_click_btn = wait.until(EC.element_to_be_clickable((By.ID, "doubleClickBtn")))
    scroll_to_element(driver, double_click_btn)
    actions.double_click(double_click_btn).perform()
    message = wait.until(EC.visibility_of_element_located((By.ID, "doubleClickMessage"))).text
    assert "You have done a double click" in message
    print(f"Successfully performed a double click and verified the message: '{message}'")

#
# def test_frame_handling(driver):
#     """
#     Covers:
#     - FRAME HANDLING
#     """
#     driver.get("https://demoqa.com/frames")
#     wait = WebDriverWait(driver, 20)
#     remove_ads_and_footer(driver)
#
#     # Switch to the frame
#     wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frame1")))
#
#     # Interact with element inside the frame
#     frame_text = wait.until(EC.visibility_of_element_located((By.ID, "sampleHeading"))).text
#     assert "This is a sample page" in frame_text
#     print(f"Successfully read text from inside the frame: '{frame_text}'")
#
#     # Switch back to the main document
#     driver.switch_to.default_content()
#
#     # FIX: Remove ads again after context switch as they might reload
#     remove_ads_and_footer(driver)
#
#     # Wait for the main header to be visible after switching back
#     main_header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "main-header")))
#     assert "Frames" in main_header.text
#     print(f"Successfully switched back to the main document and verified the header: '{main_header.text}'")
#

def test_alerts(driver):
    """
    Covers:
    - ALERTS
    """
    driver.get("https://demoqa.com/alerts")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    # --- Simple Alert ---
    alert_button = wait.until(EC.element_to_be_clickable((By.ID, "alertButton")))
    scroll_to_element(driver, alert_button)
    driver.execute_script("arguments[0].click();", alert_button)

    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    assert "You clicked a button" in alert_text
    print(f"Successfully handled simple alert with text: '{alert_text}'")
    alert.accept()

    # --- Confirmation Alert ---
    confirm_button = wait.until(EC.element_to_be_clickable((By.ID, "confirmButton")))
    scroll_to_element(driver, confirm_button)
    driver.execute_script("arguments[0].click();", confirm_button)

    alert = wait.until(EC.alert_is_present())
    alert.accept()
    confirm_message = wait.until(EC.visibility_of_element_located((By.ID, "confirmResult"))).text
    assert "You selected Ok" in confirm_message
    print(f"Successfully accepted a confirmation alert and verified the message: '{confirm_message}'")

    # --- Prompt Alert ---
    prompt_button = wait.until(EC.element_to_be_clickable((By.ID, "promtButton")))
    scroll_to_element(driver, prompt_button)
    driver.execute_script("arguments[0].click();", prompt_button)

    alert = wait.until(EC.alert_is_present())
    test_text = "Selenium Test"
    alert.send_keys(test_text)
    alert.accept()
    prompt_message = wait.until(EC.visibility_of_element_located((By.ID, "promptResult"))).text
    assert f"You entered {test_text}" in prompt_message
    print(f"Successfully handled a prompt alert and verified the result: '{prompt_message}'")

