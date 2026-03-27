from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/lec19activity.html"

def test_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL)

        assert "Secret Code Machine" in page.content()

        browser.close()


def test_correct_code():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL)

        page.fill("#code-input", "bao")
        page.click("#check-btn")

        page.wait_for_timeout(1500)

        assert "Correct!" in page.content()

        browser.close()

def test_incorrect_code():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL)

        page.fill("#code-input", "wrong")
        page.click("#check-btn")

        page.wait_for_timeout(1500)

        assert "Incorrect!" in page.content()

        browser.close()

def test_hint():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL)

        page.click("#hint-btn")

        page.wait_for_timeout(500)

        assert "Hint" in page.content()

        browser.close()