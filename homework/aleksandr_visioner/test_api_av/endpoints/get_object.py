import requests
import allure
from .endpoint import Endpoint


class GetObject(Endpoint):
    def __init__(self):
        super().__init__()

    @allure.step('Получение объекта по ID')
    def get_object_by_id(self, object_id):
        self.response = requests.get(
            f'{self.url}/object/{object_id}'
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response
