import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import JavascriptException

def remove_ads_and_footer(driver):
    """Helper function to remove footer and ad elements that can block interactions."""
    try:
        driver.execute_script("document.querySelector('footer').remove();")
        driver.execute_script("document.getElementById('fixedban').remove();")
    except JavascriptException:
        pass
    time.sleep(0.5)

def test_file_upload(driver):
    """
    Covers:
    - FILE UPLOAD
    """
    driver.get("https://demoqa.com/upload-download")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    # Create a dummy file to upload
    file_path = os.path.abspath("test_upload.txt")
    with open(file_path, "w") as f:
        f.write("This is a test file for Selenium upload.")

    # Use send_keys on the file input element
    upload_input = driver.find_element(By.ID, "uploadFile")
    upload_input.send_keys(file_path)

    # Verify the upload was successful
    uploaded_message = wait.until(EC.visibility_of_element_located((By.ID, "uploadedFilePath"))).text
    assert "test_upload.txt" in uploaded_message
    print(f"Successfully uploaded file and verified message: '{uploaded_message}'")

    # Clean up the dummy file
    os.remove(file_path)

def test_file_download(driver):
    """
    Covers:
    - FILE DOWNLOAD
    """
    driver.get("https://demoqa.com/upload-download")
    wait = WebDriverWait(driver, 20)
    remove_ads_and_footer(driver)

    # The download directory is configured in conftest.py
    download_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "downloads")
    downloaded_file_path = os.path.join(download_dir, "sampleFile.jpeg")

    # Ensure the file doesn't exist before we start
    if os.path.exists(downloaded_file_path):
        os.remove(downloaded_file_path)

    # Click the download button
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "downloadButton")))
    download_button.click()

    # Wait for the file to be downloaded
    # Note: This is a simple wait. For large files, a more robust polling mechanism is better.
    time.sleep(5)

    # Verify the file exists in the download directory
    assert os.path.exists(downloaded_file_path), "File was not downloaded successfully."
    print(f"Successfully downloaded file to: {downloaded_file_path}")

    # Clean up the downloaded file
    os.remove(downloaded_file_path)
