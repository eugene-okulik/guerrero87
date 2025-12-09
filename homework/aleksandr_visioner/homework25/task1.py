from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
import faker


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()


def test_form(driver):
    driver.get('https://www.qa-practice.com/elements/input/simple')
    wait = WebDriverWait(driver, 10)
    input_text = faker.Faker().word()

    text_field = wait.until(
        ec.element_to_be_clickable((By.ID, 'id_text_string'))
    )
    text_field.send_keys(input_text)
    text_field.send_keys(Keys.ENTER)

    wait.until(
        ec.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '[id="result-text"], .result-text'),
            input_text
        )
    )

    result_element = driver.find_element(By.CSS_SELECTOR,
                                         '[id="result-text"], .result-text')

    print("Результат:", result_element.text)

    assert result_element.text == input_text
