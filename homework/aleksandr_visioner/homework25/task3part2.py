from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def test_form(driver):
    driver.get('https://the-internet.herokuapp.com/dynamic_loading/2')

    wait = WebDriverWait(driver, 10)

    start_button = wait.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '#start button'))
    )

    print("Нажимаем кнопку Start...")
    start_button.click()

    hello_world_element = wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '#finish h4'))
    )

    result_text = hello_world_element.text
    print(f"Появившийся текст: {result_text}")

    assert result_text == 'Hello World!', (f"Ожидалось 'Hello World!',  "
                                           f"получено '{result_text}'")
