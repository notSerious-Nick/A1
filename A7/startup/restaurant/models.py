from django.db import models
from django.conf import settings


class Customer(models.Model):
    display_name = models.CharField(max_length=200)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.display_name


class Waiter(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.account.username


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    customer_name = models.CharField(max_length=200)

    waiter = models.ForeignKey(
        Waiter,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    table_number = models.IntegerField()
    item = models.CharField(max_length=200)

    placed_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="PLACED")  # "PLACED" or "DELIVERED"

    def __str__(self):
        return f"Order(table={self.table_number}, item={self.item}, status={self.status})"
