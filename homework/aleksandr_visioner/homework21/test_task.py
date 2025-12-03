import requests
import pytest
import faker
import random
import allure

global_url = 'http://objapi.course.qa-practice.com'
headers = {'Content-Type': 'application/json'}
fake = faker.Faker()
possible_sizes = ['small', 'medium', 'big']


def create_fake_data():
    fake_size = random.choice(possible_sizes)
    fake_color = fake.color_name()
    fake_name = fake.name()

    nested_data = {
        "color": fake_color,
        "size": fake_size
    }

    return {
        "name": fake_name,
        "data": nested_data
    }


def api_create_object(data):
    full_url = f"{global_url}/object"
    return requests.post(full_url, json=data, headers=headers)


def api_get_object(object_id):
    full_url = f"{global_url}/object/{object_id}"
    return requests.get(full_url)


def api_update_object(object_id, data, method='PUT'):
    full_url = f"{global_url}/object/{object_id}"
    if method.upper() == 'PATCH':
        return requests.patch(full_url, json=data, headers=headers)
    else:
        return requests.put(full_url, json=data, headers=headers)


def api_delete_object(object_id):
    full_url = f"{global_url}/object/{object_id}"
    return requests.delete(full_url)


@pytest.fixture(scope="session", autouse=True)
def session_setup_teardown():
    print("\n\nStart testing")
    yield
    print("\nTesting completed")


@pytest.fixture(autouse=True)
def function_setup_teardown():
    print("\nbefore test")
    yield
    print("after test")


@pytest.fixture()
def object_id_fixture():
    request_body = create_fake_data()
    response = api_create_object(request_body)
    assert response.status_code == 200
    object_id = response.json().get('id')
    print(f"\n[Fixture Setup] Создан объект с ID: {object_id}")
    yield {
        'id': object_id,
        'request_body': request_body
    }
    api_delete_object(object_id)
    print(f"\n[Fixture Teardown] Удален объект с ID: {object_id}")


@allure.feature('Test POST')
@allure.story('Create New object')
@pytest.mark.critical
@pytest.mark.parametrize("object_name", [
    "my test 1",
    "my test 2",
    "my test 3"
])
def test_create_new_object(object_name):
    with allure.step("Генерация фейковых данных для нового объекта"):
        new_data = create_fake_data()
        allure.attach(str(new_data), name="Сгенерированные данные",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step(
            f"Отправка POST запроса на создание объекта с именем:"
            f" {object_name}"):
        response = api_create_object(new_data)

    with allure.step("Проверка статус кода создания (Status Code 200)"):
        assert response.status_code == 200
        print("Тест создания объекта пройден.")


@pytest.mark.medium
@allure.feature('Test GET')
@allure.story('Get new object')
@allure.severity('NORMAL')
def test_get_object_by_id(object_id_fixture):
    with allure.step(f"Получение объекта с ID: {object_id_fixture['id']}"):
        object_id = object_id_fixture['id']
        response = api_get_object(object_id)

    with allure.step("Проверка, что запрос успешен (Status Code 200)"):
        assert response.status_code == 200
        response_json = response.json()

    with allure.step("Валидация полученных данных объекта"):
        assert response_json['id'] == object_id
        assert response_json['name'] == object_id_fixture['request_body'][
            'name']
        assert response_json['data']['color'] == object_id_fixture[
            'request_body']['data']['color']

    print(f"Тест получения объекта {object_id} пройден.")


@pytest.mark.critical
@allure.feature('Test POST')
@allure.story('Update an object')
@allure.description('Обновление методом PUT')
def test_update_object_put(object_id_fixture):
    object_id = object_id_fixture['id']
    new_data = create_fake_data()
    response = api_update_object(object_id, new_data, method='PUT')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['name'] == new_data['name']
    assert response_json['data']['color'] == new_data['data']['color']
    assert response_json['data']['size'] == new_data['data']['size']
    print(f"Тест обновления объекта {object_id} через PUT пройден.")


@pytest.mark.medium
@allure.feature('Test POST')
@allure.story('Update an object')
@allure.description('Обновление методом PATCH')
@allure.issue('JIRA-123', 'JIRA-123')
def test_update_object_patch(object_id_fixture):
    object_id = object_id_fixture['id']
    new_data = create_fake_data()
    response = api_update_object(object_id, new_data, method='PATCH')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['name'] == new_data['name'].join('a')
    assert response_json['data']['color'] == new_data['data']['color']
    assert response_json['data']['size'] == new_data['data']['size']
    print(f"Тест обновления объекта {object_id} через PUT пройден.")


@pytest.mark.critical
@allure.feature('Test DELETE')
@allure.story('Delete an object')
@allure.title('Удаление объекта')
def test_delete_object(object_id_fixture):
    object_id = object_id_fixture['id']

    with allure.step(f"Удаление объекта с ID: {object_id}"):
        response = api_delete_object(object_id)

    with allure.step("Проверка статус кода удаления (Status Code 200)"):
        assert response.status_code == 200

    with allure.step(f"Повторная попытка получить объект {object_id} для "
                     f"проверки его отсутствия"):
        get_response = api_get_object(object_id)
        assert get_response.status_code == 404
        print("Повторный GET запрос вернул 404 (Not Found) как ожидалось.")
