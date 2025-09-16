from time import sleep
import pytest
from UI.utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )


@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")

    driver = create_driver(headless=headless)

    yield driver

    # Espera breve antes de cerrar (para que se guarden logs/screenshots si aplica)
    sleep(2)
    driver.quit()
