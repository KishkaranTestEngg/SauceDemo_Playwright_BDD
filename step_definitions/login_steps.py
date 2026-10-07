import os
from pytest_bdd import given, when, then, parsers



@given("I am on the SauceDemo login page")
def open_login_page(page):
    page.goto("https://www.saucedemo.com/")


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login_with_credentials(page, username, password):
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


@then(parsers.parse('I should see the expected login behavior "{expected_behavior}"'))
def verify_login_behavior(page, expected_behavior):
    if expected_behavior == "successful_login":
        assert page.url == "https://www.saucedemo.com/inventory.html"

    elif expected_behavior == "locked_out":
        error_message = page.locator('[data-test="error"]').inner_text()
        assert "locked out" in error_message.lower()

@then("access should be denied")
def verify_access_denied(page):
    assert page.url != "https://www.saucedemo.com/inventory.html"
    assert page.locator('[data-test="error"]').is_visible()

@then("I should be logged in successfully")
def verify_successful_login(page):
    assert page.url == "https://www.saucedemo.com/inventory.html"

@when("I click the Logout button")
def click_logout(page):
    page.click("#react-burger-menu-btn")
    page.click("#logout_sidebar_link")

@then("I should be redirected to the login screen")
def verify_logout(page):
    assert page.url == "https://www.saucedemo.com/"
    assert page.locator("#login-button").is_visible()

# =========================
# TC004 - Cart Icon Visibility
# =========================

@given('I am logged in as "standard_user"')
def logged_in_as_standard_user(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")


@when("I am on the product listing page")
def product_listing_page(page):
    page.wait_for_selector('[data-test="inventory-container"]')


@then("the cart icon should be visible")
def cart_icon_should_be_visible(page):
    cart_icon = page.locator('[data-test="shopping-cart-link"]')
    assert cart_icon.is_visible(), "Cart icon is not visible"

# =========================
# TC005 - Random Product Selection and Data Extraction
# =========================

import random


@when("I randomly select 4 products from the product listing")
def randomly_select_four_products(page):
    products = page.locator(".inventory_item")

    # Verify there are 6 products available
    assert products.count() == 6, "Expected 6 products on the listing page"

    # Randomly select 4 products
    selected_indexes = random.sample(range(products.count()), 4)

    selected_products = []

    for index in selected_indexes:
        product = products.nth(index)

        name = product.locator(".inventory_item_name").inner_text()
        price = product.locator(".inventory_item_price").inner_text()

        selected_products.append((name, price))

    # Store selected products for the Then step
    page.selected_products = selected_products


@then("the selected product names and prices should be displayed correctly")
def verify_selected_product_data(page):
    selected_products = page.selected_products

    # Verify exactly 4 products were selected
    assert len(selected_products) == 4, "Expected 4 randomly selected products"

    print("\nSelected Products:")
    for name, price in selected_products:
        print(f"Product Name: {name} | Price: {price}")

        # Basic validation
        assert name.strip() != "", "Product name should not be empty"
        assert price.strip().startswith("$"), "Product price should start with $"

# =========================
# TC006 - Add Selected Products to Cart
# =========================

@when("I randomly select 4 products and add them to the cart")
def randomly_select_four_products_and_add_to_cart(page):
    products = page.locator(".inventory_item")

    # Verify 6 products are available
    assert products.count() == 6, "Expected 6 products on the listing page"

    # Randomly select 4 different products
    selected_indexes = random.sample(range(products.count()), 4)

    selected_products = []

    for index in selected_indexes:
        product = products.nth(index)

        name = product.locator(".inventory_item_name").inner_text()

        # Save the selected product name
        selected_products.append(name)

        # Click Add to Cart for this product
        product.locator("button").click()

    # Store selected products for the Then step
    page.selected_products = selected_products


@then("the cart icon should show a count of 4")
def verify_cart_count_is_four(page):
    cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    assert cart_badge.is_visible(), "Cart count is not visible"
    assert cart_badge.inner_text() == "4", "Cart count should be 4"


@then("the 4 selected products should be listed in the cart")
def verify_four_selected_products_in_cart(page):
    # Open the cart
    page.locator('[data-test="shopping-cart-link"]').click()

    cart_items = page.locator(".cart_item")

    # Verify exactly 4 items are present
    assert cart_items.count() == 4, "Expected 4 items in the cart"

    # Verify the selected product names are present
    for product_name in page.selected_products:
        assert cart_items.filter(has_text=product_name).count() == 1, (
            f"{product_name} was not found in the cart"
        )

# =========================
# TC007 - Validate Product Details Inside Cart
# =========================

@when("I navigate to the cart page")
def navigate_to_cart_page(page):
    page.locator('[data-test="shopping-cart-link"]').click()


@then("the cart product details should match the selected products")
def verify_cart_product_details(page):
    cart_items = page.locator(".cart_item")

    # Verify exactly 4 products are in the cart
    assert cart_items.count() == 4, "Expected 4 products in the cart"

    # Verify each selected product
    for product_name in page.selected_products:
        cart_product = cart_items.filter(has_text=product_name)

        assert cart_product.count() == 1, (
            f"{product_name} was not found in the cart"
        )

        # Fetch product name from cart
        cart_name = cart_product.locator(".inventory_item_name").inner_text()

        # Fetch product price from cart
        cart_price = cart_product.locator(".inventory_item_price").inner_text()

        # Validate product name
        assert cart_name.strip() == product_name.strip(), (
            f"Product name mismatch: Expected {product_name}, "
            f"but found {cart_name}"
        )

        # Validate price is displayed
        assert cart_price.strip().startswith("$"), (
            f"Invalid price for {cart_name}: {cart_price}"
        )

        print(f"Cart Product: {cart_name} | Price: {cart_price}")
@given("I am logged in as a standard user for checkout")
def login_as_standard_user_for_checkout(page):
    page.goto("https://www.saucedemo.com/")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    page.wait_for_url("**/inventory.html")


@given("I have a product added to the cart for checkout")
def add_product_for_checkout(page):
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    cart_badge = page.locator('[data-test="shopping-cart-badge"]')
    assert cart_badge.inner_text() == "1"


@when("I proceed to checkout")
def proceed_to_checkout(page):
    page.locator('[data-test="shopping-cart-link"]').click()

    page.locator('[data-test="checkout"]').click()

    page.wait_for_url("**/checkout-step-one.html")


@when("I enter the checkout user details")
def enter_checkout_user_details(page):
    page.locator('[data-test="firstName"]').fill("Venkat")
    page.locator('[data-test="lastName"]').fill("Kishore")
    page.locator('[data-test="postalCode"]').fill("600001")

    page.locator('[data-test="continue"]').click()

    page.wait_for_url("**/checkout-step-two.html")


@then("I should see the order summary")
def verify_order_summary(page):
    summary_title = page.locator(".title")

    assert summary_title.is_visible()
    assert summary_title.inner_text() == "Checkout: Overview"

    product = page.locator('[data-test="inventory-item"]')

    assert product.count() > 0


@then("the order summary should contain the correct product")
def verify_correct_product(page):
    product = page.locator('[data-test="inventory-item-name"]')

    assert product.inner_text() == "Sauce Labs Backpack"


@then("I capture the order summary screenshot")
def capture_order_summary_screenshot(page):
    screenshot_dir = "screenshots"

    os.makedirs(screenshot_dir, exist_ok=True)

    screenshot_path = os.path.join(
        screenshot_dir,
        "TC008_Order_Summary.png"
    )

    page.screenshot(
        path=screenshot_path,
        full_page=True
    )

    assert os.path.exists(screenshot_path)


@when("I finalize the order")
def finalize_order(page):
    page.locator('[data-test="finish"]').click()

    page.wait_for_url("**/checkout-complete.html")


@then("I should see the order confirmation message")
def verify_order_confirmation(page):
    confirmation = page.locator('[data-test="complete-header"]')

    assert confirmation.is_visible()

    assert confirmation.inner_text() == "Thank you for your order!"

@given("I am logged in as a standard user for sorting")
def login_as_standard_user_for_sorting(page):
    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    page.wait_for_url("**/inventory.html")


@when('I select "Price (low to high)" from the sort dropdown')
def select_price_low_to_high(page):
    page.locator('[data-test="product-sort-container"]').select_option("lohi")


@then("the products should be displayed in ascending price order")
def verify_products_sorted_by_price(page):
    price_elements = page.locator('[data-test="inventory-item-price"]')

    displayed_prices = []

    for i in range(price_elements.count()):
        price_text = price_elements.nth(i).inner_text()
        price_value = float(price_text.replace("$", ""))
        displayed_prices.append(price_value)

    expected_prices = sorted(displayed_prices)

    assert displayed_prices == expected_prices


@when('I select "Name (Z to A)" from the sort dropdown')
def select_name_z_to_a(page):
    page.locator('[data-test="product-sort-container"]').select_option("za")


@then("the products should be displayed in descending name order")
def verify_products_sorted_by_name(page):
    product_elements = page.locator('[data-test="inventory-item-name"]')

    displayed_names = []

    for i in range(product_elements.count()):
        product_name = product_elements.nth(i).inner_text()
        displayed_names.append(product_name)

    expected_names = sorted(displayed_names, reverse=True)

    assert displayed_names == expected_names

@given("I am logged in as a standard user for reset app state")
def login_as_standard_user_for_reset(page):
    page.goto("https://www.saucedemo.com/")

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    page.wait_for_url("**/inventory.html")


@given("I have products added to the cart for reset")
def add_products_for_reset(page):
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()

    cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    assert cart_badge.is_visible()
    assert cart_badge.inner_text() == "2"


@when("I open the menu and select Reset App State")
def reset_app_state(page):
    page.locator("#react-burger-menu-btn").click()

    reset_link = page.locator("#reset_sidebar_link")
    reset_link.click()


@then("the cart should be empty")
def verify_cart_is_empty(page):
    cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    assert not cart_badge.is_visible()


@then("the application should be in its default state")
def verify_default_app_state(page):
    cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    # Cart badge should not exist after Reset App State
    assert cart_badge.count() == 0

    # Verify we are back on the products page
    assert page.url.endswith("/inventory.html")

    # Verify products are displayed again
    products = page.locator('[data-test="inventory-item"]')

    assert products.count() > 0