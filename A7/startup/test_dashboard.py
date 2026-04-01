from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000/restaurant/"


def test_dashboard_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        assert "Restaurant Dashboard" in page.locator("h1").inner_text(), \
            "Dashboard page should show 'Restaurant Dashboard' in the main heading."

        h2_texts = page.locator("h2").all_inner_texts()
        assert "Unassigned Orders" in h2_texts, \
            "Dashboard should contain an h2 with the text 'Unassigned Orders'."
        assert "My Orders" in h2_texts, \
            "Dashboard should contain an h2 with the text 'My Orders'."

        browser.close()


def test_notification_appears_and_disappears():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.locator("#simulate-order-btn").click()

        notification = page.locator("#notification")
        assert notification.is_visible(), \
            "Notification element should be visible after clicking the simulate order button."
        assert notification.inner_text().strip() != "", \
            "Notification should contain text after clicking the simulate order button."

        page.wait_for_timeout(2500)

        assert notification.inner_text().strip() == "", \
            "Notification text should disappear after a short delay."

        browser.close()


def test_move_order_to_my_orders():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        unassigned_orders = page.locator("#unassigned-orders li")
        my_orders = page.locator("#my-orders li")

        first_order = unassigned_orders.first
        first_order_text = first_order.inner_text()

        first_order.click()

        assert page.locator("#my-orders").inner_text().find(first_order_text) != -1, \
            "Clicked order should appear in the 'My Orders' list."

        assert page.locator("#unassigned-orders").inner_text().find(first_order_text) == -1, \
            "Clicked order should no longer appear in the 'Unassigned Orders' list."

        assert my_orders.count() == 1, \
            "My Orders should contain one order after moving the first unassigned order."

        browser.close()


def test_filter_hides_non_matching_cards_and_keeps_matching_cards():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.locator("#filter-text").fill("Bao")

        cards = page.locator(".order-card")
        count = cards.count()

        for i in range(count):
            card = cards.nth(i)
            item_name = card.locator(".item-name").inner_text()

            if item_name == "Bao":
                assert card.is_visible(), \
                    "The order card with item name 'Bao' should remain visible after filtering."
            else:
                assert not card.is_visible(), \
                    "Order cards that do not match the filter text should be hidden."

        browser.close()


def test_load_orders_adds_new_cards_and_filter_affects_them():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        fetched_orders = page.locator("#fetched-orders")
        before_text = fetched_orders.inner_text().strip()

        page.locator("#load-orders-btn").click()
        page.wait_for_timeout(1000)

        after_text = fetched_orders.inner_text().strip()

        assert before_text == "", \
            "Fetched orders area should start empty before loading orders."
        assert after_text != "", \
            "Fetched orders area should contain new order cards after clicking 'Load Orders'."

        page.locator("#filter-text").fill("zzzzzz")

        original_cards = page.locator("#card-area .order-card")
        for i in range(original_cards.count()):
            assert not original_cards.nth(i).is_visible(), \
                "Original order cards should be hidden when the filter text matches none of them."

        fetched_text_after_filter = fetched_orders.inner_text().strip().lower()
        assert "zzzzzz" not in fetched_text_after_filter, \
            "Fetched orders should also be affected by filtering and should not show non-matching item text."

        browser.close()