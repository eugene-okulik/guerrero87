import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = 'http://testshop.qa-practice.com'

LOCATOR_PRODUCT_CONTAINER = (By.CSS_SELECTOR, "td.oe_product")
LOCATOR_PRODUCT_TITLE_LINK = (By.CSS_SELECTOR,
                              "h6.o_wsale_products_item_title a")
LOCATOR_ADD_TO_CART_BUTTON = (By.CSS_SELECTOR,
                              "td.oe_product .btn.btn-primary.a-submit")
LOCATOR_CONTINUE_SHOPPING_BUTTON = (By.XPATH,
                                    "//button[contains(@class, "
                                    "'btn-secondary')]//span[text("
                                    ")='Continue Shopping']")
LOCATOR_CART_LINK = (By.CSS_SELECTOR,
                     "a.o_navlink_background[href='/shop/cart']")
LOCATOR_MODAL_CONTENT = (By.CSS_SELECTOR, "div.modal-content")
LOCATOR_MODAL_PRODUCT_NAME = (By.CSS_SELECTOR, "strong.product-name")
LOCATOR_PRODUCT_DETAIL_PAGE_CART_BUTTON = (By.CSS_SELECTOR,
                                           "form[action='/shop/cart/update'] "
                                           ".btn.btn-primary")
LOCATOR_CART_ITEM_NAME = (By.CSS_SELECTOR, "h6.fw-bold")
LOCATOR_PRODUCT_IMAGE = (By.CSS_SELECTOR,
                         "td.oe_product .oe_product_image_img_wrapper img")


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def get_product_details(driver, wait):
    wait.until(ec.presence_of_all_elements_located(LOCATOR_PRODUCT_CONTAINER))
    first_product_container = driver.find_elements(*LOCATOR_PRODUCT_CONTAINER)[
        0]
    product_name_element = first_product_container.find_element(
        *LOCATOR_PRODUCT_TITLE_LINK)
    product_name = product_name_element.text.strip()

    return first_product_container, product_name, product_name_element


def test_add_to_cart_from_product_page(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    _, product_name, product_link_element = get_product_details(driver, wait)

    product_link_element.click()
    wait.until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, "form[action='/shop/cart/update']")))
    add_button = wait.until(
        ec.element_to_be_clickable(LOCATOR_PRODUCT_DETAIL_PAGE_CART_BUTTON))
    add_button.click()
    wait.until(ec.presence_of_element_located(LOCATOR_MODAL_CONTENT))
    continue_button = wait.until(
        ec.element_to_be_clickable(LOCATOR_CONTINUE_SHOPPING_BUTTON))
    continue_button.click()
    driver.get(BASE_URL)
    cart_link = wait.until(ec.element_to_be_clickable(LOCATOR_CART_LINK))
    cart_link.click()
    wait.until(ec.url_contains("cart"))

    cart_item_name = wait.until(
        ec.presence_of_element_located(LOCATOR_CART_ITEM_NAME)).text
    assert product_name.lower() in cart_item_name.lower()


def test_add_to_cart_with_hover(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    product_container, product_name, _ = get_product_details(driver, wait)
    product_image = product_container.find_element(*LOCATOR_PRODUCT_IMAGE)
    driver.execute_script("arguments[0].scrollIntoView(true);", product_image)
    ActionChains(driver).move_to_element(product_image).pause(1).perform()
    cart_button = product_container.find_element(*LOCATOR_ADD_TO_CART_BUTTON)
    wait.until(ec.element_to_be_clickable(cart_button))
    cart_button.click()
    wait.until(ec.presence_of_element_located(LOCATOR_MODAL_CONTENT))
    wait.until(ec.presence_of_element_located(LOCATOR_MODAL_PRODUCT_NAME))

    modal_product_name = driver.find_element(*LOCATOR_MODAL_PRODUCT_NAME).text
    assert product_name.lower() in modal_product_name.lower()
