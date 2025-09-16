from .base_page import BasePage
from UI.data import (
    SIGNUP_INPUT_FIRST_NAME,
    SIGNUP_INPUT_LAST_NAME,
    SIGNUP_INPUT_EMAIL,
    SIGNUP_INPUT_ZIP_CODE,
    SIGNUP_INPUT_PASSWORD,
    SIGNUP_BUTTON_SIGN_UP,
    SIGNUP_SUCCESS_MESSAGE,
    SIGNUP_PAGE_TITLE
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()

class SignUpPage(BasePage):
    URL = os.getenv("UI_SIGNUP_URL")

    INPUT_FIRST_NAME = SIGNUP_INPUT_FIRST_NAME
    INPUT_LAST_NAME = SIGNUP_INPUT_LAST_NAME
    INPUT_EMAIL = SIGNUP_INPUT_EMAIL
    INPUT_ZIP_CODE = SIGNUP_INPUT_ZIP_CODE
    INPUT_PASSWORD = SIGNUP_INPUT_PASSWORD
    BUTTON_SIGN_UP = SIGNUP_BUTTON_SIGN_UP
    SUCCESS_MESSAGE = SIGNUP_SUCCESS_MESSAGE
    PAGE_TITLE = SIGNUP_PAGE_TITLE

    def load(self):
        self.visit(self.URL)

    def register_user(self, first_name, last_name, email, zip_code, password):
        self.type(self.INPUT_FIRST_NAME, first_name)
        self.type(self.INPUT_LAST_NAME, last_name)
        self.type(self.INPUT_EMAIL, email)
        self.type(self.INPUT_ZIP_CODE, zip_code)
        self.type(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_SIGN_UP)

    def wait_for_signup_success(self, timeout=5):
        """Espera explícita hasta que aparezca el mensaje de Signup Successful"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except:
            return False

    def assert_signup_title(self, timeout=5):
        """Valida que estemos en la página de Sign Up (título)"""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )
        assert self.driver.find_element(*self.PAGE_TITLE).text == "Sign Up"
