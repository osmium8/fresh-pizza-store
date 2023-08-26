from rest_framework import serializers
from audit.models import OrderedPizza, OrderHistory, OrderTrackHistory

class OrderedPizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPizza
        fields = ("pizza", "quantity", "total_price", "customization")

class OrderTrackHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTrackHistory
        fields = ("status", "created_at", "accepted_at", "started_preparing_at", "dispatched_at", "delivered_at", "updated_at")

class OrderedHistoryDetailSerializer(serializers.ModelSerializer):
    order_items = OrderedPizzaSerializer(many=True)

    class Meta:
        model = OrderHistory
        fields = "__all__"

class OrderStatusSerializer(serializers.ModelSerializer):
    track = OrderTrackHistorySerializer(many=False)

    class Meta:
        model = OrderHistory
        fields = ("id", "track", "final_amount_currency", "final_amount")

