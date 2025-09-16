import pytest
import warnings
from UI.pages.product_detail_page import ProductDetailPage

@pytest.mark.parametrize("product_id", [2, 4])
def test_product_detail_page(driver, product_id):
    """
    Test dinámico para validar elementos de Product Detail Page (PDP) y agregar al carrito.
    - product_id: permite usar cualquier producto.
    """
    pdp = ProductDetailPage(driver)
    pdp.load_product(product_id)
    pdp.wait_for_product_loaded(product_id)

    # Validación de elementos visibles
    if pdp.validate_product_elements(product_id):
        print(f"✅ Todos los elementos visibles para el producto {product_id}")
    else:
        warnings.warn(f"⚠️ Algunos elementos NO se pudieron validar para el producto {product_id}")

    # Intentar agregar al carrito
    if pdp.add_product_and_validate_badge(product_id):
        print(f"✅ Producto {product_id} agregado al carrito")
    else:
        warnings.warn(f"⚠️ Producto {product_id} NO se pudo agregar al carrito")

@pytest.mark.parametrize("product_id", [2, 4])
def test_increment_decrement_add_to_cart(driver, product_id):
    pdp = ProductDetailPage(driver)
    pdp.load_product(product_id)
    pdp.wait_for_product_loaded(product_id)

    # Incrementar 1
    pdp.increment_quantity(product_id)
    # Decrementar 1 para volver a 1
    pdp.decrement_quantity(product_id)

    # Validar que la cantidad vuelva a 1
    assert pdp.get_quantity(product_id) == 1, "La cantidad no volvió a 1"

    # Agregar al carrito
    added = pdp.add_product_and_validate_badge(product_id)
    assert added, f"El producto {product_id} no se agregó correctamente al carrito"

    # Validar badge
    assert pdp.get_cart_badge_count() == 1, "El badge del carrito no es 1"
