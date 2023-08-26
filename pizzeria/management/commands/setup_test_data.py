from django.db import transaction
from django.core.management.base import BaseCommand
from moneyed import Money

from pizzeria.models import Pizza, Item, Category

NUM_CATEGORY = 3
NUM_PIZZA = 1
NUM_TOPPINGS = 5
NUM_BASE = 1
NUM_CHEESE = 1


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Pizza, Category, Item]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Create all the pizzas
        pizza = Pizza.objects.create(
            name="Classic",
            description="Our most loved Pizza",
            price=Money(100.00, "INR"),
        )
        pizza.save()

        # Create all the categories
        cheese = Category.objects.create(name="Cheese", required_amount=1)
        cheese.save()

        base = Category.objects.create(name="Base", required_amount=1)
        base.save()

        topping = Category.objects.create(name="Topping", required_amount=5)
        topping.save()

        # Create all the items
        mozzerella = Item.objects.create(
            name="Mozzerella", price=Money(100.00, "INR"), category=cheese
        )
        mozzerella.save()
        wheat = Item.objects.create(
            name="Wheat", price=Money(100.00, "INR"), category=base
        )
        wheat.save()
        onion = Item.objects.create(
            name="Onion", price=Money(100.00, "INR"), category=topping
        )
        onion.save()
        capcicum = Item.objects.create(
            name="Capcicum", price=Money(100.00, "INR"), category=topping
        )
        capcicum.save()
        pineapple = Item.objects.create(
            name="Pineapple", price=Money(100.00, "INR"), category=topping
        )
        pineapple.save()
        mushroom = Item.objects.create(
            name="Mushroom", price=Money(100.00, "INR"), category=topping
        )
        mushroom.save()
        paneer = Item.objects.create(
            name="Paneer", price=Money(100.00, "INR"), category=topping
        )
        paneer.save()

        self.stdout.write("Success")
