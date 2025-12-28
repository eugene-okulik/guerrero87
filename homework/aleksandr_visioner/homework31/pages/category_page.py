from playwright.sync_api import expect
import allure, re
from pages.base_page import BasePage
from pages.locators.category_locators import CategoryLocators as Loc
from pages.locators.cart_locators import CartLocators as CartLoc


class CategoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/shop/category/desks-1'

    @allure.step('Search product: {text}')
    def search_product(self, text: str):
        search_field = self.page.locator("input.search-query:visible").first
        search_field.fill(text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_url(lambda url: "search=" in url, timeout=10000)

    @allure.step('Add product via hover')
    def add_first_product_via_hover(self):
        product = self.find(Loc.CATEGORY_PRODUCTS).first
        product.scroll_into_view_if_needed()
        name = product.locator(
            Loc.CATEGORY_PRODUCT_NAMES).first.inner_text().strip()
        product.locator(Loc.CATEGORY_PRODUCT_IMAGE).first.hover(force=True)
        product.locator(Loc.CATEGORY_ADD_TO_CART_BTN).first.dispatch_event(
            "click")
        self.find(CartLoc.MODAL_CONTENT).first.wait_for(state="attached")
        return name

    def verify_products_count_greater_than_zero(self):
        expect(self.find(Loc.CATEGORY_PRODUCTS).first).to_be_visible()

    def verify_search_results_contain_text(self, text: str):
        expect(self.find(Loc.CATEGORY_PRODUCT_NAMES).first).to_contain_text(
            re.compile(text, re.IGNORECASE))

    def verify_search_results_are_empty(self):
        expect(self.find(Loc.CATEGORY_PRODUCTS)).to_have_count(0)

    @allure.step('Verify empty search message')
    def verify_search_empty_message(self, query: str):
        msg_container = self.find(Loc.SEARCH_EMPTY_MESSAGE).first
        expect(msg_container).to_contain_text(query)

    def verify_modal_product_name_matches(self, name: str):
        expect(self.find(CartLoc.MODAL_PRODUCT_NAME).first).to_contain_text(
            name, ignore_case=True)
