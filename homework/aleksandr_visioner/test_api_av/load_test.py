import random
from locust import task, tag, HttpUser

from utils import create_fake_data


class ObjectsPerforming(HttpUser):
    object_id = None
    test_object_data = None

    host = 'http://objapi.course.qa-practice.com'

    def on_start(self):
        new_data = create_fake_data()

        response = self.client.post(
            '/object',
            json=new_data,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            response_json = response.json()
            self.object_id = response_json.get('id')
            self.test_object_data = {
                'id': self.object_id,
                'request_body': new_data
            }

    @tag('Create Object')
    @task(3)
    def test_create_new_object(self):
        new_data = create_fake_data()
        object_names = ["my test 1", "my test 2", "my test 3"]
        new_data['name'] = random.choice(object_names)

        self.client.post(
            '/object',
            json=new_data,
            headers={'Content-Type': 'application/json'}
        )

    @tag('Get Object')
    @task(10)
    def test_get_object_by_id(self):
        if self.object_id:
            self.client.get(f'/object/{self.object_id}')

    @tag('Update Object PUT')
    @task(4)
    def test_update_object_put(self):
        if self.object_id:
            new_data = create_fake_data()
            self.client.put(
                f'/object/{self.object_id}',
                json=new_data,
                headers={'Content-Type': 'application/json'}
            )

    @tag('Update Object PATCH')
    @task(6)
    def test_update_object_patch(self):
        if self.object_id:
            new_data = create_fake_data()
            self.client.patch(
                f'/object/{self.object_id}',
                json=new_data,
                headers={'Content-Type': 'application/json'}
            )

    @tag('Delete Object')
    @task(1)
    def test_delete_object(self):
        if self.object_id:
            self.client.delete(f'/object/{self.object_id}')

            new_data = create_fake_data()
            create_response = self.client.post(
                '/object',
                json=new_data,
                headers={'Content-Type': 'application/json'}
            )

            if create_response.status_code == 200:
                self.object_id = create_response.json().get('id')
                self.test_object_data = {
                    'id': self.object_id,
                    'request_body': new_data
                }
