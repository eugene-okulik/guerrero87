from playwright.sync_api import Page, Locator, expect
import allure
import re


class BasePage:
    base_url = 'http://testshop.qa-practice.com'
    page_url = ""

    def __init__(self, page: Page):
        self.page = page

    def find(self, selector: str) -> Locator:
        return self.page.locator(selector)

    @allure.step('Open the page')
    def open_page(self):
        self.page.goto(f"{self.base_url}{self.page_url}", wait_until="load",
                       timeout=15000)

    def get_text(self, selector: str) -> str:
        return self.find(selector).first.inner_text().strip()

    @allure.step('Verify current URL contains {substring}')
    def verify_url_contains(self, substring: str):
        expect(self.page).to_have_url(re.compile(f".*{substring}.*"),
                                      timeout=10000)
