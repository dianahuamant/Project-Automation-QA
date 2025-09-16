from time import sleep
import pytest
from ..utils.driver_factory import create_driver
import subprocess

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )

@pytest.fixture
def driver(request):
    subprocess.run(["pkill", "-f", "chromedriver"])
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    sleep(3)
    driver.quit()

