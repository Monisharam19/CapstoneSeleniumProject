import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_explicit_wait(driver):
    """
    Covers:
    - WAIT (Explicit Wait)
    """
    driver.get("https://demoqa.com/dynamic-properties")

    # Wait for the button to be enabled
    print("Waiting for the 'Enable After 5 Seconds' button to be enabled...")
    enable_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "enableAfter"))
    )
    assert enable_button.is_enabled()
    print("Button is now enabled.")

    # Wait for the 'Visible After 5 Seconds' button to appear
    print("Waiting for the 'Visible After 5 Seconds' button to appear...")
    visible_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "visibleAfter"))
    )
    assert visible_button.is_displayed()
    print("Button is now visible.")

#
# def test_file_upload_send_keys(driver):
#     """
#     Covers:
#     - FILE UPLOADING USING SENDKEYS
#     Note: For this to work, you need a file named 'sample.txt' in the project's root directory.
#     PyAutoGUI is not used here as it's less reliable in automated/headless environments.
#     `send_keys` on an `<input type="file">` element is the standard, preferred method.
#     """
#     driver.get("https://demoqa.com/upload-download")
#
#     # Create a dummy file for uploading
#     file_name = "sample.txt"
#     file_path = os.path.join(os.getcwd(), file_name)
#     with open(file_path, "w") as f:
#         f.write("This is a test file for selenium upload.")
#
#     # Find the input element and send the file path
#     upload_element = driver.find_element(By.ID, "uploadFile")
#     upload_element.send_keys(file_path)
#
#     # Verify the file path is displayed
#     uploaded_path_text = driver.find_element(By.ID, "uploadedFilePath").text
#     assert file_name in uploaded_path_text
#     print(f"File upload successful. Path displayed: '{uploaded_path_text}'")
#
#     # Clean up the dummy file
#     os.remove(file_path)
