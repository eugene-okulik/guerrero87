import pytest
from playwright.sync_api import BrowserContext
from pages.cart_page import CartPage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage


@pytest.fixture()
def page(context: BrowserContext):
    page = context.new_page()
    page.set_viewport_size({'width': 1920, 'height': 1080})
    page.set_default_timeout(10000)
    return page


@pytest.fixture()
def cart_page(page):
    return CartPage(page)


@pytest.fixture()
def category_page(page):
    return CategoryPage(page)


@pytest.fixture()
def product_page(page):
    return ProductPage(page)
