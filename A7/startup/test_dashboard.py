from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000/restaurant/dashboard/"


def test_dashboard_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        assert "Restaurant Dashboard" in page.locator("h1").inner_text(), \
            "Dashboard page should show 'Restaurant Dashboard' in the main heading."

        h2_texts = page.locator("h2").all_inner_texts()
        assert "Unassigned Orders" in h2_texts, \
            "Dashboard should contain the heading 'Unassigned Orders'."
        assert "My Orders" in h2_texts, \
            "Dashboard should contain the heading 'My Orders'."

        browser.close()


def test_notification_appears_and_disappears():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.locator("#simulate-order-btn").click()

        notification = page.locator("#notification")
        page.wait_for_timeout(100)

        assert notification.inner_text().strip() != "", \
            "Notification should contain text after clicking 'Simulate Order Alert'."

        page.wait_for_timeout(2500)

        assert notification.inner_text().strip() == "", \
            "Notification should disappear after a short delay."

        browser.close()


def test_move_order_to_my_orders():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        first_order = page.locator("#unassigned-orders li").first
        first_order_text = first_order.inner_text()

        first_order.click()
        page.wait_for_timeout(100)

        my_orders_text = page.locator("#my-orders").inner_text()
        unassigned_text = page.locator("#unassigned-orders").inner_text()

        assert first_order_text in my_orders_text, \
            "Clicked order should appear in the 'My Orders' list."
        assert first_order_text not in unassigned_text, \
            "Clicked order should no longer appear in the 'Unassigned Orders' list."

        browser.close()


def test_filter_hides_non_matching_cards_and_keeps_matching_cards():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.locator("#filter-text").fill("Bao")
        page.wait_for_timeout(100)

        cards = page.locator(".order-card")
        count = cards.count()

        for i in range(count):
            card = cards.nth(i)
            item_name = card.locator(".item-name").inner_text()

            if "Bao" in item_name:
                assert card.is_visible(), \
                    "Matching order cards should remain visible after filtering."
            else:
                assert not card.is_visible(), \
                    "Non-matching order cards should be hidden after filtering."

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
            "Fetched orders area should contain loaded order cards after clicking 'Load Orders'."

        page.locator("#filter-text").fill("zzzzzz")
        page.wait_for_timeout(100)

        visible_cards = page.locator(".order-card:visible").count()
        assert visible_cards == 0, \
            "All visible order cards should be hidden when the filter does not match any item."

        browser.close()