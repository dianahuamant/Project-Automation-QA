from .base_page import BasePage
from UI.data import (
    HOME_MAIN_AD_SECTION,
    HOME_SHOP_BY_CATEGORY_TITLE,
    HOME_SPECIAL_DEALS_TITLE,
    HOME_VIEW_ALL_DEALS_BUTTON,
    HOME_CATEGORY_MEN_CLOTHES,
    HOME_CATEGORY_WOMEN_CLOTHES,
    HOME_CATEGORY_ELECTRONICS,
    HOME_CATEGORY_BOOKS,
    HOME_CATEGORY_GROCERIES,
    HOME_CART_ICON,
    HOME_SIGNUP_BUTTON,
    HOME_LOGIN_BUTTON,
    HOME_CATEGORIES_DROPDOWN,
    HOME_SEARCH_INPUT,
    CART_TITLE_EMPTY,
    CATEGORY_TITLE_MEN_CLOTHES,
    CATEGORY_TITLE_WOMEN_CLOTHES,
    CATEGORY_TITLE_ELECTRONICS,
    CATEGORY_TITLE_BOOKS,
    CATEGORY_TITLE_GROCERIES,
    SPECIAL_DEALS_TITLE,
    SIGNUP_PAGE_TITLE,
    LOGIN_PAGE_TITLE
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()


class HomePage(BasePage):
    URL = os.getenv("UI_BASE_URL")

    # ------------------------------
    # NAVBAR / HEADER
    # ------------------------------
    CART_ICON = HOME_CART_ICON
    SIGNUP_BUTTON = HOME_SIGNUP_BUTTON
    LOGIN_BUTTON = HOME_LOGIN_BUTTON
    CATEGORIES_DROPDOWN = HOME_CATEGORIES_DROPDOWN
    SEARCH_INPUT = HOME_SEARCH_INPUT

    # ------------------------------
    # SECCIONES HOME
    # ------------------------------
    MAIN_AD_SECTION = HOME_MAIN_AD_SECTION
    SHOP_BY_CATEGORY_TITLE = HOME_SHOP_BY_CATEGORY_TITLE
    SPECIAL_DEALS_TITLE = HOME_SPECIAL_DEALS_TITLE
    VIEW_ALL_DEALS_BUTTON = HOME_VIEW_ALL_DEALS_BUTTON

    # ------------------------------
    # CATEGORÍAS
    # ------------------------------
    CATEGORY_MEN_CLOTHES = HOME_CATEGORY_MEN_CLOTHES
    CATEGORY_WOMEN_CLOTHES = HOME_CATEGORY_WOMEN_CLOTHES
    CATEGORY_ELECTRONICS = HOME_CATEGORY_ELECTRONICS
    CATEGORY_BOOKS = HOME_CATEGORY_BOOKS
    CATEGORY_GROCERIES = HOME_CATEGORY_GROCERIES

    # ------------------------------
    # TÍTULOS DE PÁGINA
    # ------------------------------
    CART_TITLE_EMPTY = CART_TITLE_EMPTY
    CATEGORY_TITLE_MEN_CLOTHES = CATEGORY_TITLE_MEN_CLOTHES
    CATEGORY_TITLE_WOMEN_CLOTHES = CATEGORY_TITLE_WOMEN_CLOTHES
    CATEGORY_TITLE_ELECTRONICS = CATEGORY_TITLE_ELECTRONICS
    CATEGORY_TITLE_BOOKS = CATEGORY_TITLE_BOOKS
    CATEGORY_TITLE_GROCERIES = CATEGORY_TITLE_GROCERIES
    SPECIAL_DEALS_TITLE = SPECIAL_DEALS_TITLE
    SIGNUP_PAGE_TITLE = SIGNUP_PAGE_TITLE
    LOGIN_PAGE_TITLE = LOGIN_PAGE_TITLE

    # ------------------------------
    # MÉTODOS
    # ------------------------------

    def load(self):
        """Carga la página principal"""
        self.visit(self.URL)

    # -------- REDIRECCIONES --------
    def go_to_signup(self):
        self.click(self.SIGNUP_BUTTON)

    def go_to_login(self):
        self.click(self.LOGIN_BUTTON)

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def go_to_men_clothes(self):
        self.click(self.CATEGORY_MEN_CLOTHES)

    def go_to_women_clothes(self):
        self.click(self.CATEGORY_WOMEN_CLOTHES)

    def go_to_electronics(self):
        self.click(self.CATEGORY_ELECTRONICS)

    def go_to_books(self):
        self.click(self.CATEGORY_BOOKS)

    def go_to_groceries(self):
        self.click(self.CATEGORY_GROCERIES)

    def go_to_special_deals(self):
        self.click(self.VIEW_ALL_DEALS_BUTTON)

    # -------- ESPERAS EXPLÍCITAS --------
    def wait_for_signup_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(SIGNUP_PAGE_TITLE)
        )

    def wait_for_login_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LOGIN_PAGE_TITLE)
        )

    def wait_for_cart_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_TITLE_EMPTY)
        )

    def wait_for_men_clothes_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE_MEN_CLOTHES)
        )

    def wait_for_women_clothes_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE_WOMEN_CLOTHES)
        )

    def wait_for_electronics_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE_ELECTRONICS)
        )

    def wait_for_books_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE_BOOKS)
        )

    def wait_for_groceries_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CATEGORY_TITLE_GROCERIES)
        )

    def wait_for_special_deals_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(os.getenv("UI_SPECIAL_DEALS_URL"))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(SPECIAL_DEALS_TITLE)
        )