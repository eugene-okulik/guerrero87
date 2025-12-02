import requests
import faker
import random

global_url = "http://objapi.course.qa-practice.com"
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


def get_response_id():
    request_body = create_fake_data()
    endpoint = "/object"
    full_url = f"{global_url}{endpoint}"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        full_url,
        json=request_body,
        headers=headers
    )

    try:
        return response.json()['id']
    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode response as JSON.")
        print(f"Raw response text: {response.text}")


def get_object_by_id(object_id):
    endpoint = "/object"
    full_url = f"{global_url}{endpoint}/{id}"
    response = requests.get(full_url)

    try:
        if response.status_code == 200:
            print(f"GET ответ JSON: {response.json()}")
        return response
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Could not decode response as JSON for ID {object_id}.")
        print(f"Raw response text: {response.text}")
        return response


def create_new_object():
    request_body = create_fake_data()
    print("--- POST: информация об объекте ---\r\n")
    print(f"JSON BODY: {request_body}")

    endpoint = "/object"
    full_url = f"{global_url}{endpoint}"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        full_url,
        json=request_body,
        headers=headers
    )
    print(f"API URL: {full_url}")

    try:
        response_json = response.json()
        print(f"JSON Response: {response_json}")
        print("\r\n--- ПРОВЕРКИ ПО СОЗДАНИЮ ОБЪЕКТА ---")

        # Проверка 1: Код статуса 200
        assert response.status_code == 200, \
            f"FAILED: Ожидался статус 200, получен {response.status_code}"
        print("Проверка 1: Код статуса 200 - PASSED")

        # Проверка 2: Размер находится в списке допустимых
        assert response_json["data"]["size"] in possible_sizes, \
            (f"FAILED: Ожидался размер из списка {possible_sizes}, получен "
             f"'{response_json['data']['size']}'")
        print("Проверка 2: Размер корректен - PASSED")

        # Проверка 3: Имя в ответе соответствует отправленному
        assert response_json["name"] == request_body["name"], \
            (f"FAILED: Ожидалось имя '{request_body['name']}', получено "
             f"'{response_json['name']}'")
        print("Проверка 3: Имя соответствует отправленному - PASSED")

        # Проверка 4: Тест должен упасть
        assert response_json["data"]["color"] == "OMG123", \
            (f"Проверка 4: Ожидался цвет '"
             f"{request_body['data']['color']}', получено OMG123 - FAILED")

        print("--- Все проверки завершены успешно ---\r\n")

    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode response as JSON.")
        print(f"Raw response text: {response.text}")
    except AssertionError as e:
        print("\n--- ОБНАРУЖЕНА ОШИБКА ПРОВЕРКИ ---")
        print(e)
        print("--- Проверки завершены с ошибками ---\r\n")


def update_object():
    object_id = get_response_id()
    print("--- PUT: информация об объекте ---\r\n")
    if not object_id:
        print("Не удалось получить ID нового объекта, отмена удаления.")
        return

    request_body = create_fake_data()
    print(f"JSON BODY: {request_body}")

    endpoint = f"/object/{object_id}"
    full_url = f"{global_url}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    print(f"API URL: {full_url}")
    response = requests.put(
        full_url,
        json=request_body,
        headers=headers
    )

    try:
        response_json = response.json()
        print(f"JSON Response: {response_json}")
        print("\r\n--- ПРОВЕРКИ ПО ОБНОВЛЕНИЮ ОБЪЕКТА (PUT) ---")

        # Проверка 1: Код статуса 200
        assert response.status_code == 200, \
            f"FAILED: Ожидался статус 200, получен {response.status_code}"
        print("Проверка 1: Код статуса 200 - PASSED")

        # Проверка 2: Цвет в ответе соответствует отправленному
        assert response_json["data"]["color"] == request_body["data"][
            "color"], \
            (
                f"FAILED: Ожидался цвет '{request_body['data']['color']}', "
                f"получено '{response_json['data']['color']}'")
        print("Проверка 2: Цвет соответствует отправленному - PASSED")

        print("--- Все проверки завершены успешно ---\r\n")

    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode response as JSON.")
        print(f"Raw response text: {response.text}")
    except AssertionError as e:
        print("\n--- ОБНАРУЖЕНА ОШИБКА ПРОВЕРКИ ---")
        print(e)
        print("--- Проверки завершены с ошибками ---\r\n")


def patch_object():
    object_id = get_response_id()
    print("--- PATCH: информация об объекте ---\r\n")
    if not object_id:
        print("Не удалось получить ID нового объекта, отмена удаления.")
        return

    request_body = create_fake_data()
    print(f"JSON BODY: {request_body}")

    endpoint = f"/object/{object_id}"
    full_url = f"{global_url}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    print(f"API URL: {full_url}")
    response = requests.patch(
        full_url,
        json=request_body,
        headers=headers
    )

    try:
        response_json = response.json()
        print(f"JSON Response: {response_json}")
        print("\r\n--- ПРОВЕРКИ ПО ОБНОВЛЕНИЮ ОБЪЕКТА (PATCH) ---")

        # Проверка 1: Код статуса 200
        assert response.status_code == 200, \
            f"FAILED: Ожидался статус 200, получен {response.status_code}"
        print("Проверка 1: Код статуса 200 - PASSED")

        # Проверка 2: Размер в ответе соответствует отправленному
        assert response_json["data"]["size"] == request_body["data"][
            "size"], \
            (
                f"FAILED: Ожидался цвет '{request_body['data']['size']}', "
                f"получено '{response_json['data']['size']}'")
        print("Проверка 2: Размер соответствует отправленному - PASSED")

        print("--- Все проверки завершены успешно ---\r\n")

    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode response as JSON.")
        print(f"Raw response text: {response.text}")
    except AssertionError as e:
        print("\n--- ОБНАРУЖЕНА ОШИБКА ПРОВЕРКИ ---")
        print(e)
        print("--- Проверки завершены с ошибками ---\r\n")


def delete_object():
    object_id = get_response_id()
    print("--- DELETE: информация об объекте ---\r\n")
    if not object_id:
        print("Не удалось получить ID нового объекта, отмена удаления.")
        return

    print(f"\n--- Начинаем процесс удаления объекта с ID: {object_id} ---")

    endpoint = f"/object/{object_id}"
    full_url = f"{global_url}{endpoint}"
    print(f"API URL: {full_url}")
    response = requests.delete(full_url)
    # print (response)

    try:
        print("\r\n--- ПРОВЕРКИ ПО УДАЛЕНИЮ ОБЪЕКТА ---")

        # Проверка 1: Код статуса 200
        assert response.status_code == 200, \
            f"FAILED: Ожидался статус 200, получен {response.status_code}"
        print("Проверка 1: Код статуса 200 - PASSED")

        # Проверка 2: Проверка, что объект действительно удалился
        get_response = get_object_by_id(object_id)
        # print (get_response.text)

        assert get_response.status_code == 404, \
            (f"FAILED: Ожидался статус 404 после удаления, получен"
             f" {get_response.status_code}")
        print("Проверка 2 (GET 404 Not Found): PASSED")

        print("--- Все проверки завершены успешно ---\r\n")

    except requests.exceptions.JSONDecodeError:
        print("Error: Could not decode response as JSON.")
        print(f"Raw response text: {response.text}")
    except AssertionError as e:
        print("\n--- ОБНАРУЖЕНА ОШИБКА ПРОВЕРКИ ---")
        print(e)
        print("--- Проверки завершены с ошибками ---\r\n")


if __name__ == "__main__":
    create_new_object()
    update_object()
    patch_object()
    delete_object()
