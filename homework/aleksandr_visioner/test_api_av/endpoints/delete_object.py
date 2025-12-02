import requests
import allure
from .endpoint import Endpoint


class DeleteObject(Endpoint):
    def __init__(self):
        super().__init__()

    @allure.step('Удаление объекта по ID')
    def delete_object(self, object_id):
        self.response = requests.delete(
            f'{self.url}/object/{object_id}',
            headers=self.headers
        )
        return self.response
