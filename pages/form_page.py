from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormPage:
    """Page Object for the DemoQA Practice Form page."""

    # --- Locators ---
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "userEmail")
    GENDER_RADIO = (By.XPATH, "//label[text()='Male']")
    MOBILE_INPUT = (By.ID, "userNumber")
    SUBMIT_BUTTON = (By.ID, "submit")
    CONFIRMATION_HEADER = (By.ID, "example-modal-sizes-title-lg")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def load(self):
        """Loads the practice form page."""
        self.driver.get("https://demoqa.com/automation-practice-form")

    def enter_first_name(self, first_name):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def select_gender(self):
        self.driver.find_element(*self.GENDER_RADIO).click()

    def enter_mobile_number(self, mobile):
        self.driver.find_element(*self.MOBILE_INPUT).send_keys(mobile)

    def submit_form(self):
        # We need to scroll the submit button into view before clicking
        submit_btn = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()

    def get_confirmation_text(self):
        """Waits for and returns the text from the confirmation modal header."""
        return self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_HEADER)).text
