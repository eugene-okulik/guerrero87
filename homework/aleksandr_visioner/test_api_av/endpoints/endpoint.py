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

    @allure.step('Проверка статус кода 404')
    def check_that_status_is_404(self):
        assert self.response.status_code == 404

    @allure.step('Check that id is returned')
    def check_response_id_is_correct(self):
        assert self.response.json().get('id') is not None

    @allure.step('Check that name is the same as sent')
    def check_response_name_is_correct(self, request_data):
        assert self.response.json()['name'] == request_data['name']

    @allure.step('Check that size is the same as sent')
    def check_response_size_is_correct(self, request_data):
        assert self.response.json()['data']['size'] == request_data['data'][
            'size']

    @allure.step('Check that color is the same as sent')
    def check_response_color_is_correct(self, request_data):
        assert self.response.json()['data']['color'] == request_data['data'][
            'color']
