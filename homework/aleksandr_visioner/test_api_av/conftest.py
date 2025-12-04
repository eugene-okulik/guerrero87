import pytest
from .utils import create_fake_data


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
def create_object_endpoint():
    from endpoints.create_object import CreateObject
    return CreateObject()


@pytest.fixture()
def get_object_endpoint():
    from endpoints.get_object import GetObject
    return GetObject()


@pytest.fixture()
def update_object_endpoint():
    from endpoints.update_object import UpdateObject
    return UpdateObject()


@pytest.fixture()
def delete_object_endpoint():
    from endpoints.delete_object import DeleteObject
    return DeleteObject()


@pytest.fixture()
def test_object_fixture(create_object_endpoint, delete_object_endpoint):
    request_body = create_fake_data()

    create_object_endpoint.create_new_object(request_body)
    create_object_endpoint.check_that_status_is_200()

    object_id = create_object_endpoint.json.get('id')

    print(f"\nСоздан объект с ID: {object_id}")

    yield {
        'id': object_id,
        'request_body': request_body
    }

    delete_object_endpoint.delete_object(object_id)
    print(f"\nУдален объект с ID: {object_id}")
