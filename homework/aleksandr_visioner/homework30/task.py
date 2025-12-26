import re
from playwright.sync_api import Page, expect

URL = 'https://www.apple.com/shop/buy-iphone'
API_PATH = "**/shop/api/digital-mat**"
MOCK_NAME = "яблокофон 17 про"


def test_apple_title_mock(page: Page):
    def modify_api(route):
        response = route.fetch()
        data = response.json()
        data['body']['digitalMat'][0]['familyTypes'][0][
            'productName'] = MOCK_NAME
        route.fulfill(json=data)

    page.route(API_PATH, modify_api)

    page.goto(URL)
    page.locator("button[data-autom='DigitalMat-1']").click()

    header = page.locator('h2[data-autom="DigitalMat-overlay-header-0-0"]')
    expect(header).to_have_text(re.compile(MOCK_NAME))
