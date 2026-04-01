from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000/restaurant/dashboard/"


def test_dashboard_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        assert "Restaurant Dashboard" in page.locator("h1").inner_text(), \
            "Dashboard page should contain 'Restaurant Dashboard' in the main heading."

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
            "Notification should appear with text after clicking 'Simulate Order Alert'."

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
            "The first unassigned order should move to 'My Orders' after being clicked."
        assert first_order_text not in unassigned_text, \
            "The moved order should no longer appear in 'Unassigned Orders'."

        browser.close()


def test_filter_hides_non_matching_cards_and_keeps_matching_cards():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        page.locator("#filter-text").fill("Bao")
        page.wait_for_timeout(100)

        cards = page.locator("#card-area .order-card")
        count = cards.count()

        for i in range(count):
            card = cards.nth(i)
            item_name = card.locator(".item-name").inner_text()

            if "Bao" in item_name:
                assert card.is_visible(), \
                    "Cards whose item name matches the filter should remain visible."
            else:
                assert not card.is_visible(), \
                    "Cards whose item name does not match the filter should be hidden."

        browser.close()


def test_loaded_cards_participate_in_filtering():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        # Apply a filter first so newly loaded cards must obey the current filter.
        page.locator("#filter-text").fill("zzzzzz")
        page.wait_for_timeout(100)

        page.locator("#load-orders-btn").click()
        page.wait_for_timeout(1000)

        loaded_cards = page.locator("#fetched-orders .order-card")
        loaded_count = loaded_cards.count()

        assert loaded_count > 0, \
            "Clicking 'Load Orders' should create new order cards in the fetched orders area."

        for i in range(loaded_count):
            assert not loaded_cards.nth(i).is_visible(), \
                "Newly loaded cards should also be hidden when the active filter matches none of them."

        page.locator("#filter-text").fill("")
        page.wait_for_timeout(100)

        visible_loaded_cards = page.locator("#fetched-orders .order-card:visible").count()
        assert visible_loaded_cards == loaded_count, \
            "Loaded cards should become visible again after clearing the filter."

        browser.close()