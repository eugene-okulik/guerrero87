from playwright.sync_api import Page


def test_form_authentication(page: Page):
    page.goto('https://the-internet.herokuapp.com/')
    page.get_by_role("link", name="Form Authentication").click()
    page.get_by_role("textbox", name="Username").fill("admin")
    page.get_by_role("textbox", name="Password").fill("admin")
    page.get_by_role("button", name="Login").click()


def test_fill_automation_practice_form(page: Page):
    page.goto('https://demoqa.com/automation-practice-form')

    page.get_by_placeholder("First Name").fill("Alex")
    page.get_by_placeholder("Last Name").fill("Sakol")
    page.get_by_placeholder("name@example.com").fill("alex.sakol@example.com")
    page.get_by_placeholder("Mobile Number").fill("1234567890")
    page.get_by_placeholder("Current Address").fill("123 Lenina St., Minsk")

    page.get_by_text("Male", exact=True).click()

    page.locator("#dateOfBirthInput").click()
    page.locator(".react-datepicker__day--028").first.click()

    subjects_input = page.locator("#subjectsInput")
    subjects_input.type("Computer Science")
    page.locator(".subjects-auto-complete__menu").get_by_text(
        "Computer Science").click()

    page.get_by_text("Sports").click()
    page.get_by_text("Reading").click()
    page.get_by_text("Music", ).click()

    page.locator("#state").click()
    page.get_by_text("NCR", exact=True).click()

    page.locator("#city").click(force=True)
    page.get_by_text("Delhi", exact=True).click()

    page.locator("#submit").click()

    page.locator("#closeLargeModal").click()
