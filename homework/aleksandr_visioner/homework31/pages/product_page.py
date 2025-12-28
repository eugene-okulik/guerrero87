from playwright.sync_api import expect
import allure
from pages.base_page import BasePage
from pages.locators.product_locators import ProductLocators as Loc
from pages.locators.cart_locators import CartLocators as CartLoc


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/shop/furn-9999-office-design-software-7'

    @allure.step('Add to cart')
    def add_to_cart(self):
        btn = self.find(Loc.PRODUCT_ADD_TO_CART_BUTTON).first
        btn.scroll_into_view_if_needed()
        btn.click(force=True)

        self.find(CartLoc.MODAL_CONTENT).first.wait_for(state="attached",
                                                        timeout=10000)

    def verify_image_is_present(self):
        expect(self.find(Loc.PRODUCT_IMAGE).first).to_be_visible()

    def change_quantity(self, increase: bool = True):
        selector = Loc.PRODUCT_INCREASE_QUANTITY if increase else (
            Loc.PRODUCT_DECREASE_QUANTITY)
        self.find(selector).first.click(force=True)

    def verify_quantity_is_one(self):
        expect(self.find(Loc.PRODUCT_QUANTITY_INPUT).first).to_have_value("1")

    def verify_quantity_is_two(self):
        expect(self.find(Loc.PRODUCT_QUANTITY_INPUT).first).to_have_value("2")

    @allure.step('Verify modal window present')
    def verify_modal_is_present(self):
        expect(self.find(CartLoc.MODAL_CONTENT).first).to_be_attached()
