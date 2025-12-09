from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from faker import Faker
import pytest
import random
from datetime import date, timedelta


def random_date_in_range(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randrange(
        days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    return random_date.strftime("%d %B %Y")


def generate_form_data():
    fake = Faker()

    states_cities = {
        'NCR': ['Delhi', 'Gurgaon', 'Noida'],
        'Uttar Pradesh': ['Agra', 'Lucknow', 'Merrut'],
        'Haryana': ['Karnal', 'Panipat'],
        'Rajasthan': ['Jaipur', 'Jaiselmer']
    }

    state = random.choice(list(states_cities.keys()))
    city = random.choice(states_cities[state])

    subjects_count = random.randint(1, 3)
    subjects = [fake.word().capitalize() for _ in range(subjects_count)]

    date_str = random_date_in_range(1960, 2005)

    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'mobile': fake.numerify('##########'),
        'address': fake.address().replace('\n', ', '),
        'gender': random.choice(['Male', 'Female', 'Other']),
        'subjects': subjects,
        'hobbies': random.sample(['Sports', 'Reading', 'Music'],
                                 random.randint(1, 3)),
        'state': state,
        'city': city,
        'date_str': date_str
    }


@pytest.fixture()
def driver():
    chrome_driver = webdriver.Chrome()
    chrome_driver.set_window_size(1024, 768)
    yield chrome_driver
    chrome_driver.quit()


def test_form(driver):
    form_data = generate_form_data()
    print("Сгенерированные данные:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    driver.get('https://demoqa.com/automation-practice-form')

    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.ID, 'firstName')))

    driver.find_element(By.CSS_SELECTOR, '#firstName').send_keys(
        form_data['first_name'])
    driver.find_element(By.CSS_SELECTOR, '#lastName').send_keys(
        form_data['last_name'])
    driver.find_element(By.CSS_SELECTOR, '#userEmail').send_keys(
        form_data['email'])

    gender_mapping = {
        'Male': '[for="gender-radio-1"]',
        'Female': '[for="gender-radio-2"]',
        'Other': '[for="gender-radio-3"]'
    }
    gender_selector = gender_mapping[form_data['gender']]
    gender_label = driver.find_element(By.CSS_SELECTOR, gender_selector)
    gender_label.click()

    driver.find_element(By.CSS_SELECTOR, '#userNumber').send_keys(
        form_data['mobile'])

    date_input = driver.find_element(By.CSS_SELECTOR, '#dateOfBirthInput')
    driver.execute_script(f"arguments[0].value = '{form_data['date_str']}';",
                          date_input)

    subjects_input = driver.find_element(By.CSS_SELECTOR, '#subjectsInput')
    for subject in form_data['subjects']:
        subjects_input.send_keys(subject)
        subjects_input.send_keys(Keys.ENTER)

    hobbies_mapping = {
        'Sports': '[for="hobbies-checkbox-1"]',
        'Reading': '[for="hobbies-checkbox-2"]',
        'Music': '[for="hobbies-checkbox-3"]'
    }
    for hobby in form_data['hobbies']:
        hobby_selector = hobbies_mapping[hobby]
        hobby_label = driver.find_element(By.CSS_SELECTOR, hobby_selector)
        driver.execute_script("arguments[0].click();", hobby_label)

    address_input = driver.find_element(By.CSS_SELECTOR, '#currentAddress')
    driver.execute_script("arguments[0].scrollIntoView(true);", address_input)
    address_input.send_keys(form_data['address'])

    state_input_container = driver.find_element(By.CSS_SELECTOR, '#state')
    driver.execute_script(f"arguments[0].innerText = '{form_data['state']}';",
                          state_input_container)

    driver.execute_script(
        "var event = new Event('change', { bubbles: true }); arguments["
        "0].dispatchEvent(event);",
        state_input_container)

    city_input_container = driver.find_element(By.CSS_SELECTOR, '#city')
    driver.execute_script("arguments[0].scrollIntoView(true);",
                          city_input_container)

    driver.execute_script(f"arguments[0].innerText = '{form_data['city']}';",
                          city_input_container)
    driver.execute_script(
        "var event = new Event('change', { bubbles: true }); arguments["
        "0].dispatchEvent(event);",
        city_input_container)

    submit_button = driver.find_element(By.CSS_SELECTOR, '#submit')
    driver.execute_script("arguments[0].click();", submit_button)

    wait.until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, '.modal-content')))

    modal_body = driver.find_element(By.CSS_SELECTOR, '.modal-body')

    print("\n" + "=" * 50)
    print("СОДЕРЖИМОЕ МОДАЛЬНОГО ОКНА:")
    print("=" * 50)
    print(modal_body.text)

    close_button = driver.find_element(By.CSS_SELECTOR, '#closeLargeModal')
    close_button.click()
