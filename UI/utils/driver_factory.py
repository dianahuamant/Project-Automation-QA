from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import tempfile


def create_driver(headless: bool = False):
    options = webdriver.ChromeOptions()

    # Configs necesarias en Linux CI/CD
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # evita errores gráficos
    options.add_argument("--disable-software-rasterizer")

    # Perfil temporal único (evita error "user data directory in use")
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

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
