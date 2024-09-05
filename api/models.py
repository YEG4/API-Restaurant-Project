from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + f" -  Price: {self.price}"

    @property
    def get_price(self):
        return self.price


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts')
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"ID: {{{self.id}}} - User: {{{self.user.username}}} - MenuItem: {{{self.menu_item.name}}} - Price: {{{self.unit_price}}} - Quantity: {{{self.quantity}}}"

    class Meta:
        unique_together = ('user', 'menu_item')

    @property
    def get_total(self):
        return (self.unit_price * self.quantity)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='delivery_crew', blank=True, null=True)
    status = models.BooleanField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order Id: " + f"{{{self.id}}}" + " - User: " + self.user.username + f" - Total : {{{self.total}}}"


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{{{self.order.user.username}}}" + " - " + self.menu_item.name + f" - Price: {{{self.unit_price}}}"

    class Meta:
        unique_together = ('order', 'menu_item')

    @property
    def get_total(self):
        return (self.unit_price * self.quantity)
