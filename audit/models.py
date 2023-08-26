from django.db import models
from djmoney.models.fields import MoneyField
from moneyed import Money

from pizzeria.serializers import ItemSerializer

# Create your models here.
"""
CRUD Pizza
CRUD Item
CRUD Category

POST /pizzeria/order              {pizza_code}
GET /pizzeria/order               {order_item[]} filter by request.user

HTTP /pizzeria/orderitem        {ViewSet}

POST /pizzeria/place_order   {create entiry in OrderHistory, start celery task}

GET /order/status     {id}
GET /order            {user_id}
"""


class OrderTrackHistory(models.Model):
    class Status(models.TextChoices):
        PLACED = "PLACED", "PLACED"
        ACCEPTED = "ACCEPTED", "ACCEPTED"
        PREPARING = "PREPARING", "PREPARING"
        DISPATCHED = "DISPATCHED", "DISPATCHED"
        DELIVERED = "DELIVERED", "DELIVERED"

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.PLACED
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    accepted_at = models.DateTimeField(editable=False, null=True)
    started_preparing_at = models.DateTimeField(editable=False, null=True)
    dispatched_at = models.DateTimeField(editable=False, null=True)
    delivered_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class OrderHistoryManager(models.Manager):
    def create_order_history(self, user, order_items):
        order_track_history = OrderTrackHistory.objects.create(
            status=OrderTrackHistory.Status.PLACED
        )
        order_history = OrderHistory.objects.create(
            user=user,
            track=order_track_history,
            final_amount=Money(0.00, "INR"),
        )

        final_amount = 0

        for order_item in order_items:
            total = order_item.pizza.price.amount
            customization_json = []
            for item in order_item.customization.all():
                total = total + item.price.amount
                customization_json.append(ItemSerializer(item).data)
            final_amount = final_amount + total

            ordered_pizza_obj = OrderedPizza.objects.create(
                order=order_history,
                pizza=order_item.pizza,
                quantity=order_item.quantity,
                total_price=total,
                customization=customization_json,
            )

            ordered_pizza_obj.save()

        order_history.final_amount = Money(final_amount, "INR")
        order_history.save()
        return order_history


class OrderHistory(models.Model):
    objects = OrderHistoryManager()
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    final_amount = MoneyField(max_digits=6, decimal_places=2, default_currency="INR")
    track = models.OneToOneField(OrderTrackHistory, on_delete=models.SET_NULL, null=True)


class OrderedPizza(models.Model):
    order = models.ForeignKey(
        "audit.OrderHistory", on_delete=models.CASCADE, related_name="order_items"
    )
    pizza = models.ForeignKey("pizzeria.Pizza", on_delete=models.SET_NULL, null=True)
    quantity = models.SmallIntegerField(null=False)
    customization = models.JSONField()
    total_price = MoneyField(max_digits=6, decimal_places=2, default_currency="INR")
