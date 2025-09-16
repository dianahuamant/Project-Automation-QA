from time import sleep
import pytest
import subprocess
from UI.utils.driver_factory import create_driver  

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )

@pytest.fixture
def driver(request):
    # Evitar procesos colgados de Chrome/Driver
    subprocess.run(["pkill", "-f", "chromedriver"], check=False)

    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    sleep(3)
    driver.quit()
