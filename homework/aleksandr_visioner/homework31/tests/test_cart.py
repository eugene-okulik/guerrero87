import pytest
import allure
from pages.locators.product_locators import ProductLocators as Loc


@allure.feature('Cart Operations')
class TestCartPage:

    @pytest.mark.cart
    @allure.story('Empty Cart Verification')
    def test_empty_cart(self, cart_page):
        cart_page.open_page()
        cart_page.verify_cart_is_empty()

    @pytest.mark.cart
    @allure.story('Adding Item and Verifying Cart Content')
    def test_item_in_cart(self, product_page, cart_page):
        product_page.open_page()
        expected_name = product_page.get_text(Loc.PRODUCT_NAME)
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal_and_handle_cookies()
        cart_page.verify_item_in_cart_by_name(expected_name)

    @pytest.mark.cart
    @allure.story('Continue Shopping Flow')
    def test_continue_shopping(self, product_page, cart_page):
        product_page.open_page()
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal_and_handle_cookies()
        cart_page.click_continue_shopping()
        cart_page.verify_url_contains("/shop")

    @pytest.mark.cart
    @allure.story('Full Navigation via Modal Window')
    def test_cart_navigation_via_modal(self, product_page, cart_page):
        product_page.open_page()
        expected_name = product_page.get_text(Loc.PRODUCT_NAME)
        product_page.add_to_cart()
        cart_page.navigate_to_cart_from_modal_and_handle_cookies()
        cart_page.verify_url_contains("/shop/cart")
        cart_page.verify_item_in_cart_by_name(expected_name)
