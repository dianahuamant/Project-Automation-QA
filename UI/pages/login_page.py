from UI.data import (
    LOGIN_INPUT_EMAIL,
    LOGIN_INPUT_PASSWORD,
    LOGIN_BUTTON_LOGIN,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_PAGE_TITLE,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from .base_page import BasePage

load_dotenv()

class LoginPage(BasePage):
    URL = os.getenv("UI_LOGIN_URL")

    INPUT_EMAIL = LOGIN_INPUT_EMAIL
    INPUT_PASSWORD = LOGIN_INPUT_PASSWORD
    BUTTON_LOGIN = LOGIN_BUTTON_LOGIN
    SUCCESS_MESSAGE = LOGIN_SUCCESS_MESSAGE
    PAGE_TITLE = LOGIN_PAGE_TITLE

    def load(self):
        self.visit(self.URL)

    def login_as_user(self, email, password):
        self.type(self.INPUT_EMAIL, email)
        self.type(self.INPUT_PASSWORD, password)
        self.click(self.BUTTON_LOGIN)

    def wait_for_login_success(self, timeout=5):
        """Espera explícita hasta que aparezca el mensaje Logged In"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except:
            return False

    def assert_login_title(self, timeout=5):
        """Valida que estemos en la página de Login (su título)"""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )
        assert self.driver.find_element(*self.PAGE_TITLE).text == "Login"
