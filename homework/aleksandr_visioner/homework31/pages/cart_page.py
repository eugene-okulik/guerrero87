from playwright.sync_api import expect
import allure
from pages.base_page import BasePage
from pages.locators.cart_locators import CartLocators as Loc


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/shop/cart'

    def verify_cart_is_empty(self):
        expect(self.find(Loc.CART_EMPTY_MESSAGE).first).to_be_visible()

    @allure.step('Navigate to cart from modal')
    def navigate_to_cart_from_modal_and_handle_cookies(self):
        btn = self.find(Loc.CART_VIEW_CART_BUTTON).first
        btn.wait_for(state="attached")

        with self.page.expect_navigation(timeout=10000):
            btn.click(force=True)

        self.verify_url_contains("/shop/cart")

    def click_continue_shopping(self):
        self.find(Loc.CART_CONTINUE_SHOPPING_PAGE_BTN).first.click(force=True)

    def verify_item_in_cart_by_name(self, name: str):
        first_item = self.find(Loc.CART_ITEM_NAMES).first
        expect(first_item).to_contain_text(name, ignore_case=True)
