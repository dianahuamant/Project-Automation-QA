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
    subprocess.run(["pkill", "-9", "-f", "chromedriver"], check=False)
    subprocess.run(["pkill", "-9", "-f", "chrome"], check=False)

    headless = request.config.getoption("--headless")

    driver = create_driver(headless=headless)

    yield driver

    # Espera breve antes de cerrar (para que se guarden logs/screenshots si aplicara)
    sleep(2)
    driver.quit()
