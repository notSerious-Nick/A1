import time
from django.http import JsonResponse
from django.shortcuts import render
from .models import Order


def dashboard(request):
    return render(request, "restaurant/dashboard.html")


def orders_json(request):
    time.sleep(2)  # simulate slow server
    orders = Order.objects.order_by("table_number", "item")

    data = {
        "orders": [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "table_number": order.table_number,
                "item": order.item,
                "status": order.status,
            }
            for order in orders
        ]
    }

    return JsonResponse(data)
