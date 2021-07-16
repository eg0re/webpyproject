from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

from Shoebox.models import Shoebox
from Useradmin.models import MyUser


class ShoppingCart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(MyUser, on_delete=models.CASCADE,)

    def add_item(myuser, box):
        # Get existing shopping cart, or create a new one if none exists
        shopping_carts = ShoppingCart.objects.filter(myuser=myuser)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
        else:
            shopping_cart = ShoppingCart.objects.create(myuser=myuser)

        # Add box to shopping cart
        ShoppingCartItem.objects.create(box=box,
                                        quantity=1,
                                        shopping_cart=shopping_cart,
                                        )

    def get_number_of_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        return len(shopping_cart_items)

    def get_total(self):
        total = Decimal(0.0)  # Default without Decimal() would be type float!
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            total += item.box.price * item.quantity
        return total


class ShoppingCartItem(models.Model):
    box = models.ForeignKey(Shoebox, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    def add_quantity(self):
        quantity = ShoppingCartItem.objects.get(box=self.box).quantity
        temp = quantity + 1
        self.quantity = temp
        print(quantity)
        return self.save()


class Payment(models.Model):
    credit_card_number = models.CharField(max_length=19)  # Format: 1234 5678 1234 5678
    expiry_date = models.CharField(max_length=7)  # Format: 10/2022
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               )