from django.db import models
from djmoney.models.fields import MoneyField

class Pizza(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=280)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='INR')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(null=False, max_length=30)
    required_amount = models.SmallIntegerField(null=True) #TODO
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(null=False, max_length=30)
    price = MoneyField(max_digits=6, decimal_places=2, default_currency='INR')
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name


class OrderSessionManager(models.Manager):
    def clear(self, user_id):
        OrderItem.objects.filter(order_session__user__id=user_id).delete()

class OrderSession(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    delivery_address = models.CharField(null=True, max_length=140)
    objects = OrderSessionManager()

class OrderItem(models.Model):
    order_session = models.ForeignKey(OrderSession, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    customization = models.ManyToManyField(Item)
    quantity = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order_session', 'pizza'], name='unique pizza')
        ]

    

