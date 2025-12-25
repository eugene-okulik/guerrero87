import re
from playwright.sync_api import Page, expect, BrowserContext


def test_task_1(page: Page):
    page.goto('https://www.qa-practice.com/elements/alert/confirm')
    page.once('dialog', lambda dialog: dialog.accept())
    page.get_by_role('link', name='Click').click()
    expect(page.locator('#result-text')).to_have_text('Ok')


def test_task_2(page: Page, context: BrowserContext):
    page.goto('https://www.qa-practice.com/elements/new_tab/button')
    button = page.locator('#new-page-button')

    with context.expect_page() as new_page_event:
        button.click()

    new_page = new_page_event.value
    expect(new_page.locator('#result-text')).to_have_text(
        'I am a new page in a new tab')
    expect(button).to_be_enabled()
    new_page.close()


def test_task_3(page: Page):
    page.goto('https://demoqa.com/dynamic-properties')
    color_button = page.locator('#colorChange')
    expect(color_button).to_have_class(re.compile(r'text-danger'),
                                       timeout=6000)
    color_button.click()
