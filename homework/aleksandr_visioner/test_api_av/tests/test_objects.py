import pytest
import allure
from ..utils import create_fake_data


@allure.feature('Объекты API')
@allure.story('CRUD операции с объектами')
class TestObjectCRUD:
    @allure.feature('Test POST')
    @allure.story('Создание нового объекта')
    @allure.title('Создание объекта с различными именами')
    @pytest.mark.critical
    @pytest.mark.parametrize("object_name", [
        "my test 1",
        "my test 2",
        "my test 3"
    ])
    def test_create_new_object(self, create_object_endpoint, object_name):
        new_data = create_fake_data()
        new_data['name'] = object_name
        create_object_endpoint.create_new_object(new_data)

        allure.attach(str(new_data),
                      name="Сгенерированные данные",
                      attachment_type=allure.attachment_type.JSON)

        create_object_endpoint.check_that_status_is_200()
        create_object_endpoint.check_response_id_is_correct()
        create_object_endpoint.check_response_name_is_correct(
            request_data=new_data)
        create_object_endpoint.check_response_size_is_correct(
            request_data=new_data)
        create_object_endpoint.check_response_color_is_correct(
            request_data=new_data)

    @allure.feature('Test GET')
    @allure.story('Получение объекта по ID')
    @allure.title('Получение созданного объекта')
    @pytest.mark.medium
    @allure.severity('NORMAL')
    def test_get_object_by_id(self, test_object_fixture, get_object_endpoint):
        object_id = test_object_fixture['id']
        get_object_endpoint.get_object_by_id(object_id)

        get_object_endpoint.check_that_status_is_200()
        get_object_endpoint.check_response_name_is_correct(
            test_object_fixture['request_body'])
        get_object_endpoint.check_response_size_is_correct(
            test_object_fixture['request_body'])
        get_object_endpoint.check_response_color_is_correct(
            test_object_fixture['request_body'])

    @allure.feature('Test PUT')
    @allure.story('Обновление объекта методом PUT')
    @allure.title('Полное обновление объекта')
    @pytest.mark.critical
    def test_update_object_put(self, test_object_fixture,
                               update_object_endpoint):
        object_id = test_object_fixture['id']
        new_data = create_fake_data()
        update_object_endpoint.update_object(object_id, new_data, method='PUT')

        allure.attach(str(new_data),
                      name="Новые данные для обновления",
                      attachment_type=allure.attachment_type.JSON)

        update_object_endpoint.check_that_status_is_200()
        update_object_endpoint.check_response_id_is_correct()
        update_object_endpoint.check_response_name_is_correct(
            request_data=new_data)
        update_object_endpoint.check_response_size_is_correct(
            request_data=new_data)
        update_object_endpoint.check_response_color_is_correct(
            request_data=new_data)

    @allure.feature('Test PATCH')
    @allure.story('Обновление объекта методом PATCH')
    @allure.title('Частичное обновление объекта')
    @pytest.mark.medium
    @allure.description('Обновление методом PATCH с проверкой изменений')
    @allure.issue('JIRA-123', 'JIRA-123: Исправление проверки имени')
    def test_update_object_patch(self, test_object_fixture,
                                 update_object_endpoint):
        object_id = test_object_fixture['id']
        new_data = create_fake_data()
        update_object_endpoint.update_object(object_id, new_data,
                                             method='PATCH')

        update_object_endpoint.check_that_status_is_200()
        update_object_endpoint.check_response_id_is_correct()
        update_object_endpoint.check_response_name_is_correct(
            request_data=new_data)
        update_object_endpoint.check_response_size_is_correct(
            request_data=new_data)
        update_object_endpoint.check_response_color_is_correct(
            request_data=new_data)

    @allure.feature('Test DELETE')
    @allure.story('Удаление объекта')
    @allure.title('Удаление и проверка отсутствия объекта')
    @pytest.mark.critical
    def test_delete_object(self, test_object_fixture,
                           delete_object_endpoint):
        object_id = test_object_fixture['id']

        allure.attach(f"Создан объект для удаления: {object_id}",
                      name="ID объекта",
                      attachment_type=allure.attachment_type.TEXT)

        delete_object_endpoint.delete_object(object_id)
        delete_object_endpoint.check_that_status_is_200()
