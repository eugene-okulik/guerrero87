from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
import pytest


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def test_form(driver):
    driver.get('https://www.qa-practice.com/elements/select/single_select')

    wait = WebDriverWait(driver, 10)

    select_element = wait.until(
        ec.presence_of_element_located((By.ID, 'id_choose_language'))
    )

    select = Select(select_element)

    select.select_by_visible_text('Python')

    selected_value = select.first_selected_option.text
    print(f"Выбрано: {selected_value}")

    submit_button = driver.find_element(By.ID, 'submit-id-submit')
    submit_button.click()

    result_element = wait.until(
        ec.visibility_of_element_located((By.ID, 'result-text'))
    )

    result_text = result_element.text
    print(f"Результат: {result_text}")

    assert selected_value in result_text, (f"Ожидалось '{selected_value}', "
                                           f"получено '{result_text}'")
