import allure


class Endpoint:
    def __init__(self):
        self.url = 'http://objapi.course.qa-practice.com'
        self.response = None
        self.json = None
        self.headers = {'Content-Type': 'application/json'}

    @allure.step('Проверка статус кода 200')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200
        return self
