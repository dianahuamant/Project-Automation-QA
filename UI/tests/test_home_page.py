import pytest
from UI.pages.home_page import HomePage
import os

@pytest.mark.usefixtures("driver")
class TestHomePage:

    def test_go_to_signup(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_signup()
        home.wait_for_signup_page()
        assert driver.current_url == os.getenv("UI_SIGNUP_URL")

    def test_go_to_login(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_login()
        home.wait_for_login_page()
        assert driver.current_url == os.getenv("UI_LOGIN_URL")

    def test_go_to_cart(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_cart()
        home.wait_for_cart_page()
        assert driver.current_url == os.getenv("UI_CART_URL")

    def test_go_to_men_clothes(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_men_clothes()
        home.wait_for_men_clothes_page()
        assert driver.current_url == os.getenv("UI_MEN_CLOTHES_URL")

    def test_go_to_women_clothes(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_women_clothes()
        home.wait_for_women_clothes_page()
        assert driver.current_url == os.getenv("UI_WOMEN_CLOTHES_URL")

    def test_go_to_electronics(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_electronics()
        home.wait_for_electronics_page()
        assert driver.current_url == os.getenv("UI_ELECTRONICS_URL")

    def test_go_to_books(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_books()
        home.wait_for_books_page()
        assert driver.current_url == os.getenv("UI_BOOKS_URL")

    def test_go_to_groceries(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_groceries()
        home.wait_for_groceries_page()
        assert driver.current_url == os.getenv("UI_GROCERIES_URL")

    def test_go_to_special_deals(self, driver):
        home = HomePage(driver)
        home.load()
        home.go_to_special_deals()
        home.wait_for_special_deals_page()
        assert driver.current_url == os.getenv("UI_SPECIAL_DEALS_URL")
