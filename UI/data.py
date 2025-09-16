from selenium.webdriver.common.by import By

OVERLAY=(By.CSS_SELECTOR, "div.fixed.inset-0.z-50")

#LOCATORS DE SIGNUP
SIGNUP_INPUT_FIRST_NAME = (By.ID, "firstName")
SIGNUP_INPUT_LAST_NAME = (By.ID, "lastName")
SIGNUP_INPUT_EMAIL = (By.ID, "email")
SIGNUP_INPUT_ZIP_CODE = (By.ID, "zipCode")
SIGNUP_INPUT_PASSWORD = (By.ID, "password")
SIGNUP_BUTTON_SIGN_UP = (By.CSS_SELECTOR, "button[type='submit']")
SIGNUP_SUCCESS_MESSAGE  = (By.XPATH, "//h1[text()='Signup Successful']")
SIGNUP_PAGE_TITLE = (By.XPATH, "//div[text()='Sign Up']")

#LOCATORS DE LOGIN
LOGIN_INPUT_EMAIL = (By.ID, "email")
LOGIN_INPUT_PASSWORD = (By.ID, "password")
LOGIN_BUTTON_LOGIN = (By.CSS_SELECTOR, "button[type='submit']")
LOGIN_SUCCESS_MESSAGE  = (By.XPATH, "//h1[text()='Logged In']")
LOGIN_PAGE_TITLE = (By.XPATH, "//div[text()='Login']")

#LOCATOR DE HOME PAGE
# Navbar / Header
HOME_CART_ICON = (By.CSS_SELECTOR, "a[href='/cart']")
HOME_SIGNUP_BUTTON = (By.CSS_SELECTOR, "a[href='/signup']")
HOME_LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href='/login']")
HOME_CATEGORIES_DROPDOWN = (By.XPATH, "//button[contains(., 'Categories')]")
HOME_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")
# Categorías
HOME_SHOP_BY_CATEGORY_TITLE = (By.XPATH, "//h2[text()='Shop by Category']")
HOME_CATEGORY_MEN_CLOTHES = (By.CSS_SELECTOR, "a[href='/categories/men-clothes'] .rounded-lg")
HOME_CATEGORY_WOMEN_CLOTHES = (By.CSS_SELECTOR, "a[href='/categories/women-clothes'] .rounded-lg")
HOME_CATEGORY_ELECTRONICS = (By.CSS_SELECTOR, 'a[href="/categories/electronics"] .rounded-lg')
HOME_CATEGORY_BOOKS = (By.CSS_SELECTOR, "a[href='/categories/books'] .rounded-lg")
HOME_CATEGORY_GROCERIES = (By.CSS_SELECTOR, "a[href='/categories/groceries'] .rounded-lg")
# Special Deals
HOME_SPECIAL_DEALS_TITLE = (By.XPATH, "//h2[text()='Special Deals']")
HOME_VIEW_ALL_DEALS_BUTTON = (By.LINK_TEXT, "View All Deals")
# Anuncio
HOME_MAIN_AD_SECTION = (By.CSS_SELECTOR, "div.absolute.inset-0.bg-black\\/40.flex.items-center.justify-center")

#LOCATOR DE PÁGINA DE LA CATEGORÍA
CATEGORY_TITLE_MEN_CLOTHES = (By.XPATH, "//h1[@id='category-title' and text()=\"Men's Clothes\"]")
CATEGORY_TITLE_WOMEN_CLOTHES = (By.XPATH, "//h1[@id='category-title' and text()=\"Women's Clothes\"]")
CATEGORY_TITLE_ELECTRONICS = (By.XPATH, "//h1[@id='category-title' and text()='Electronics']")
CATEGORY_TITLE_BOOKS = (By.XPATH, "//h1[@id='category-title' and text()='Books']")
CATEGORY_TITLE_GROCERIES = (By.XPATH, "//h1[@id='category-title' and text()='Groceries']")

#LOCATOR DE SPECIAL DEALS
SPECIAL_DEALS_TITLE = (By.XPATH, "//h1[@id='category-title' and text()='Special Deals']")

# LOCATORS DE CATEGORY PAGE
CATEGORY_DESCRIPTION = (By.ID, "category-description")
CATEGORY_PRODUCT_CONTAINER = (By.CSS_SELECTOR, "div[id^='product-content-']")
CART_BADGE = (By.CSS_SELECTOR, "div.text-xs")

# Locators dinámicos por ID de producto
def product_image(product_id: int):
    return (By.ID, f"product-image-{product_id}")

def product_name(product_id: int):
    return (By.ID, f"product-name-{product_id}")

def product_desc(product_id: int):
    return (By.ID, f"product-desc-{product_id}")

def product_price(product_id: int):
    return (By.ID, f"product-price-{product_id}")

def product_view_details(product_id: int):
    return (By.ID, f"view-details-{product_id}")

def product_add_to_cart(product_id: int):
    return (By.ID, f"add-to-cart-{product_id}")

# ======================
# LOCATORS PRODUCT DETAIL PAGE (PDP)
# ======================
def product_image_product_detail(product_id: int):
    return By.ID, f"product-main-image-{product_id}"

def product_title_product_detail(product_id: int):
    return By.ID, f"product-main-title-{product_id}"

def product_category_product_detail(product_id: int):
    return By.ID, f"product-category-{product_id}"

def product_price_product_detail(product_id: int):
    return By.ID, f"product-main-price-{product_id}"

def product_desc_title_product_detail(product_id: int):
    return By.ID, f"product-desc-title-{product_id}"

def product_desc_text_product_detail(product_id: int):
    return By.ID, f"product-desc-text-{product_id}"

def quantity_label_product_detail(product_id: int):
    return By.CSS_SELECTOR, f"label[for='quantity-{product_id}']"

def quantity_decrease_product_detail(product_id: int):
    return By.ID, f"quantity-decrease-{product_id}"

def quantity_increase_product_detail(product_id: int):
    return By.ID, f"quantity-increase-{product_id}"

def quantity_display_product_detail(product_id: int):
    return By.ID, f"quantity-display-{product_id}"

def add_to_cart_button_product_detail(product_id: int):
    return By.ID, f"add-to-cart-main-{product_id}"

def free_shipping_text_product_detail(product_id: int):
    return By.ID, f"feature-shipping-{product_id}"

def return_policy_text_product_detail(product_id: int):
    return By.ID, f"feature-returns-{product_id}"

def secure_payment_text_product_detail(product_id: int):
    return By.ID, f"feature-payment-{product_id}"

from selenium.webdriver.common.by import By

# ======================
# CART PAGE
# ======================

# Page Titles

# Carrito con productos
CART_TITLE = (By.XPATH, "//h1[text()='Shopping Cart']")
# Carrito vacío
CART_TITLE_EMPTY = (By.XPATH, "//h1[text()='Your Cart is Empty']")

CART_ORDER_SUMMARY_TITLE = (By.XPATH, "//div[text()='Order Summary']")


# Buttons
CART_BUTTON_CHECKOUT = (By.XPATH, "//button[text()='Proceed to Checkout']")
CART_BUTTON_CONTINUE_SHOPPING = (By.XPATH, "//button[text()='Continue Shopping']")

# Order Summary Fields
CART_SUBTOTAL = (By.XPATH, "//span[preceding-sibling::span[text()='Subtotal']]")
CART_SHIPPING = (By.XPATH, "//span[preceding-sibling::span[text()='Shipping']]")
CART_TAX = (By.XPATH, "//span[preceding-sibling::span[text()='Tax']]")
CART_TOTAL = (By.XPATH, "//span[preceding-sibling::span[text()='Total']]")

# ======================
# PRODUCTOS EN CARRITO
# ======================

def CART_PRODUCT_CONTAINER_BY_NAME(product_name: str):
    """Contenedor principal del producto en carrito por nombre"""
    return (
        By.XPATH,
        "//main[contains(@class,'min-h-screen')]"
        "//div[contains(@class,'container mx-auto px-4 py-8')]"
        "//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        "//div[contains(@class,'lg:col-span-2 space-y-4')]"
        "//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        "//div[contains(@class,'p-6')]"
        "//div[contains(@class,'flex items-center space-x-4')]"
        "//div[contains(@class,'flex-1')]"
        f"//h3[contains(@class,'font-semibold') and normalize-space()='{product_name}']"
        "/ancestor::div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
    )

def CART_PRODUCT_QUANTITY(product_name: str):
    return (By.XPATH,
        "//main[contains(@class,'min-h-screen')]"
        "//div[contains(@class,'container mx-auto px-4 py-8')]"
        "//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        "//div[contains(@class,'lg:col-span-2 space-y-4')]"
        "//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        "//div[contains(@class,'p-6')]"
        "//div[contains(@class,'flex items-center space-x-4')]"
        "//div[contains(@class,'flex-1')]"
        f"//h3[contains(@class,'font-semibold') and normalize-space()='{product_name}']"
        "/../following-sibling::div[contains(@class,'flex items-center space-x-2')]"
        "//span[contains(@class,'text-center') and contains(@class,'font-medium')]"
    )

def CART_PRODUCT_PRICE(product_name: str):
    """Precio numérico del producto en el carrito por nombre (ignora el $)."""
    return (
        By.XPATH,
        f"//main[contains(@class,'min-h-screen')]"
        f"//div[contains(@class,'container mx-auto px-4 py-8')]"
        f"//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        f"//div[contains(@class,'lg:col-span-2 space-y-4')]"
        f"//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        f"//div[contains(@class,'p-6')]"
        f"//div[contains(@class,'flex items-center space-x-4')]"
        f"//div[contains(@class,'flex-1')]"
        f"//h3[normalize-space()='{product_name}']/../following-sibling::div[contains(@class,'text-right')]/p[contains(@class,'font-bold')]"
    )

def CART_PRODUCT_INCREMENT(product_name: str):
    return (By.XPATH,
        "//main[contains(@class,'min-h-screen')]"
        "//div[contains(@class,'container mx-auto px-4 py-8')]"
        "//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        "//div[contains(@class,'lg:col-span-2 space-y-4')]"
        "//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        "//div[contains(@class,'p-6')]"
        "//div[contains(@class,'flex items-center space-x-4')]"
        "//div[contains(@class,'flex-1')]"
        f"//h3[contains(@class,'font-semibold') and normalize-space()='{product_name}']"
        "/../following-sibling::div[contains(@class,'flex items-center space-x-2')]"
        "//button[contains(@class,'inline-flex') and .//*[contains(@class,'lucide-plus')]]"
    )

def CART_PRODUCT_DECREMENT(product_name: str):
    return (By.XPATH,
        "//main[contains(@class,'min-h-screen')]"
        "//div[contains(@class,'container mx-auto px-4 py-8')]"
        "//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        "//div[contains(@class,'lg:col-span-2 space-y-4')]"
        "//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        "//div[contains(@class,'p-6')]"
        "//div[contains(@class,'flex items-center space-x-4')]"
        "//div[contains(@class,'flex-1')]"
        f"//h3[contains(@class,'font-semibold') and normalize-space()='{product_name}']"
        "/../following-sibling::div[contains(@class,'flex items-center space-x-2')]"
        "//button[contains(@class,'inline-flex') and .//*[contains(@class,'lucide-minus')]]"
    )

def CART_PRODUCT_REMOVE(product_name: str):
    return (By.XPATH,
        "//main[contains(@class,'min-h-screen')]"
        "//div[contains(@class,'container mx-auto px-4 py-8')]"
        "//div[contains(@class,'grid lg:grid-cols-3 gap-8')]"
        "//div[contains(@class,'lg:col-span-2 space-y-4')]"
        "//div[contains(@class,'rounded-lg border bg-card text-card-foreground shadow-sm')]"
        "//div[contains(@class,'p-6')]"
        "//div[contains(@class,'flex items-center space-x-4')]"
        "//div[contains(@class,'flex-1')]"
        f"//h3[contains(@class,'font-semibold') and normalize-space()='{product_name}']"
        "/../following-sibling::div[contains(@class,'text-right')]"
        "//button[contains(@class,'inline-flex') and normalize-space(text())='Remove']"
    )

# ======================
# CHECKOUT PAGE
# ======================
CHECKOUT_TITLE = (By.XPATH, "//h1[text()='Checkout']")
CHECKOUT_COMPLETE_TITLE = (By.ID, "customer-info-title")

# --- Checkout input fields ---
CHECKOUT_COMPLETE_INPUT_FIRST_NAME = (By.ID, "firstName")
CHECKOUT_COMPLETE_INPUT_LAST_NAME = (By.ID, "lastName")
CHECKOUT_COMPLETE_INPUT_EMAIL = (By.ID, "email")
CHECKOUT_COMPLETE_INPUT_PHONE = (By.ID, "phone")
CHECKOUT_COMPLETE_INPUT_ADDRESS = (By.ID, "address")
CHECKOUT_COMPLETE_INPUT_CITY = (By.ID, "city")
CHECKOUT_COMPLETE_INPUT_ZIP_CODE = (By.ID, "zipCode")
CHECKOUT_COMPLETE_INPUT_COUNTRY = (By.ID, "country")

CHECKOUT_COMPLETE_BUTTON_PLACE_ORDER = (By.ID, "place-order-button")

# --- Checkout field labels ---
CHECKOUT_COMPLETE_FIELD_FIRST_NAME = (By.ID, "first-name-field")
CHECKOUT_COMPLETE_FIELD_LAST_NAME = (By.ID, "last-name-field")
CHECKOUT_COMPLETE_FIELD_EMAIL = (By.ID, "email-field")
CHECKOUT_COMPLETE_FIELD_PHONE = (By.ID, "phone-field")
CHECKOUT_COMPLETE_FIELD_ADDRESS = (By.ID, "address-field")
CHECKOUT_COMPLETE_FIELD_CITY = (By.ID, "city-field")
CHECKOUT_COMPLETE_FIELD_ZIP_CODE = (By.ID, "zip-field")
CHECKOUT_COMPLETE_FIELD_COUNTRY = (By.ID, "country-field")

# --- Expected labels texts ---
CHECKOUT_COMPLETE_EXPECTED_LABELS = {
    CHECKOUT_COMPLETE_FIELD_FIRST_NAME: "First Name *",
    CHECKOUT_COMPLETE_FIELD_LAST_NAME: "Last Name *",
    CHECKOUT_COMPLETE_FIELD_EMAIL: "Email *",
    CHECKOUT_COMPLETE_FIELD_PHONE: "Phone *",
    CHECKOUT_COMPLETE_FIELD_ADDRESS: "Address *",
    CHECKOUT_COMPLETE_FIELD_CITY: "City *",
    CHECKOUT_COMPLETE_FIELD_ZIP_CODE: "ZIP Code *",
    CHECKOUT_COMPLETE_FIELD_COUNTRY: "Country *",
}
