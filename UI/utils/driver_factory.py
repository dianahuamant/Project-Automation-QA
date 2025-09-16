from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def create_driver(headless: bool = False):
    options = webdriver.ChromeOptions()

    # Configs necesarias en Linux CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # evita errores en headless en Linux
    options.add_argument("--disable-software-rasterizer")

    # Forzar tamaño de ventana
    options.add_argument("--window-size=1920,1080")

    # Si es headless
    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    driver.implicitly_wait(5)
    return driver
