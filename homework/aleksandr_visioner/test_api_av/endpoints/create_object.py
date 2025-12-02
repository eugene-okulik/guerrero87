import requests
import allure
from .endpoint import Endpoint


class CreateObject(Endpoint):
    def __init__(self):
        super().__init__()

    @allure.step('Создание нового объекта')
    def create_new_object(self, payload):
        self.response = requests.post(
            f'{self.url}/object',
            json=payload,
            headers=self.headers
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response
