from django.db import IntegrityError
from rest_framework import serializers
from pizzeria.models import Category, OrderItem, Pizza, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ("name", "description", "price", "price_currency")


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("name", "price", "price_currency")


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ("id",)

    def validate(self, data):
        customization = data.get('customization')
        items_count_dictionary = dict()
        
        for item in customization:
            items_count_dictionary[item.category] = items_count_dictionary.get(item.category, 0) + 1

        categories = Category.objects.all()
        for category in categories:
            if (items_count_dictionary[category] != category.required_amount):
                raise serializers.ValidationError(f"Customization Validation not satisfied, {category.required_amount} {category}(s) must be selected")
        return super().validate(data)

    def create(self, validated_data):
        try:
            orderItem = OrderItem.objects.create(
                quantity=validated_data["quantity"],
                order_session=validated_data["order_session"],
                pizza=validated_data["pizza"],
            )
            orderItem.customization.set(validated_data["customization"])
            orderItem.save()
            return orderItem
        except IntegrityError:
            raise serializers.ValidationError("This pizza already added.")
        


class OrderItemResponseSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    pizza = PizzaSerializer(many=False)
    customization = ItemSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_total_price(self, obj: OrderItem):
        total = obj.pizza.price.amount
        for item in obj.customization.all():
            total = total + item.price.amount
        return total
