import pytest
import allure


@allure.feature('Product Page')
class TestProductPage:

    @pytest.mark.product
    @allure.story('Verify product image visibility')
    def test_image_visible(self, product_page):
        product_page.open_page()
        product_page.verify_image_is_present()

    @pytest.mark.product
    @allure.story('Verify quantity lower limit (minimum 1)')
    def test_quantity_limits(self, product_page):
        product_page.open_page()
        product_page.verify_quantity_is_one()
        product_page.change_quantity(increase=False)
        product_page.verify_quantity_is_one()

    @pytest.mark.product
    @allure.story('Verify quantity increase control')
    def test_quantity_control(self, product_page):
        product_page.open_page()
        product_page.change_quantity(increase=True)
        product_page.verify_quantity_is_two()

    @pytest.mark.product
    @allure.story('Add product to cart from details page')
    def test_add_from_details(self, product_page):
        product_page.open_page()
        product_page.add_to_cart()
        product_page.verify_modal_is_present()
