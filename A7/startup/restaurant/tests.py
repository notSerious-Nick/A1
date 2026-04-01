from django.test import TestCase


class RestaurantDashboardTests(TestCase):
    def test_dashboard_page_loads_successfully(self):
        response = self.client.get("/restaurant/")
        self.assertEqual(
            response.status_code,
            200,
            "Dashboard page should return status code 200."
        )

    def test_dashboard_contains_expected_h2_headers(self):
        response = self.client.get("/restaurant/")
        content = response.content.decode()

        self.assertIn(
            "<h2>Unassigned Orders</h2>",
            content,
            "Dashboard page should contain the exact h2 text 'Unassigned Orders'."
        )
        self.assertIn(
            "<h2>My Orders</h2>",
            content,
            "Dashboard page should contain the exact h2 text 'My Orders'."
        )

    def test_orders_json_endpoint_loads_successfully(self):
        response = self.client.get("/restaurant/orders-json/")
        self.assertEqual(
            response.status_code,
            200,
            "Orders JSON endpoint should return status code 200."
        )

    def test_orders_json_has_expected_structure(self):
        response = self.client.get("/restaurant/orders-json/")
        data = response.json()

        self.assertIn(
            "orders",
            data,
            "Orders JSON response should contain an 'orders' field."
        )
        self.assertIsInstance(
            data["orders"],
            list,
            "The 'orders' field should be a list."
        )