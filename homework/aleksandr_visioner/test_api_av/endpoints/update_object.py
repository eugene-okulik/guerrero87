import requests
import allure
from .endpoint import Endpoint


class UpdateObject(Endpoint):
    def __init__(self):
        super().__init__()

    @allure.step('Обновление объекта')
    def update_object(self, object_id, payload, method='PUT'):
        if method.upper() == 'PATCH':
            self.response = requests.patch(
                f'{self.url}/object/{object_id}',
                json=payload,
                headers=self.headers
            )
        else:
            self.response = requests.put(
                f'{self.url}/object/{object_id}',
                json=payload,
                headers=self.headers
            )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response
