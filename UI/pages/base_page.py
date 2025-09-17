from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UI.data import OVERLAY

class BasePage:

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver

    def visit(self, url: str):
        self.driver.get(url)

    def click(self, locator: tuple[By, str]):
        self.driver.find_element(*locator).click()

    def type(self, locator: tuple[By, str], text: str):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def text_of_element(self, locator: tuple[By, str]) -> str:
        return self.driver.find_element(*locator).text

    def element_is_visible(self, locator: tuple[By, str]) -> bool:
        return self.driver.find_element(*locator).is_displayed()

    def reload(self):
        self.driver.refresh()

    def find_all(self, locator):
        """Devuelve una lista de elementos que coinciden con el locator."""
        return self.driver.find_elements(*locator)

    def wait_for_overlay_to_disappear(self, timeout: int = 20):
        """Espera a que cualquier overlay desaparezca para poder interactuar con elementos."""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(OVERLAY)
        )
