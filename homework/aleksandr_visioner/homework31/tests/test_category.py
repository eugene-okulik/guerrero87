import pytest
import allure


@allure.feature('Category Page')
class TestCategoryPage:

    @pytest.mark.category
    @allure.story('Verify products visibility')
    def test_products_count(self, category_page):
        category_page.open_page()
        category_page.verify_products_count_greater_than_zero()

    @pytest.mark.category
    @allure.story('Search functionality with results')
    def test_search_desk(self, category_page):
        category_page.open_page()
        category_page.search_product("Desk")
        category_page.verify_search_results_contain_text("desk")

    @pytest.mark.category
    @allure.story('Add product to cart via hover action')
    def test_hover_add_to_cart(self, category_page):
        category_page.open_page()
        p_name = category_page.add_first_product_via_hover()
        category_page.verify_modal_product_name_matches(p_name)

    @pytest.mark.category
    @allure.story('Search with no results')
    def test_search_empty_results(self, category_page):
        category_page.open_page()
        search_query = "NonExistentItem123"
        category_page.search_product(search_query)
        category_page.verify_search_empty_message(search_query)
        category_page.verify_search_results_are_empty()
