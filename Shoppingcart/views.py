from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

import Shoppingcart
from Shoebox.models import Shoebox
from Useradmin.models import MyUser
from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem


def basket(request, **kwargs):
    box_id = kwargs['bpk']
    shoebox = Shoebox.objects.get(id=box_id)
    user = MyUser.objects.get(user=request.user)
    usershoppingcart = ShoppingCart.objects.get(myuser_id=user.id)
    ShoppingCart.add_item(myuser=user, box=shoebox)
    cart = ShoppingCartItem.objects.filter(shopping_cart_id=usershoppingcart.id)

    total = 0
    for item in cart:
        total += item.box.price

    context = {
        'shopping_cart': cart,
        'total': total,
    }

    return render(request, 'shopping-cart.html', context)


def show_shopping_cart(request):
    user = MyUser.objects.get(user=request.user)
    # Get existing shopping cart, or create a new one if none exists
    shopping_carts = ShoppingCart.objects.filter(myuser=user)
    if shopping_carts:
        usershoppingcart = shopping_carts.first()
    else:
        usershoppingcart = ShoppingCart.objects.create(myuser=user)

    cart = ShoppingCartItem.objects.filter(shopping_cart_id=usershoppingcart.id)

    total = 0
    for item in cart:
        total += item.box.price

    context = {
        'shopping_cart': cart,
        'total': total,
    }

    return render(request, 'shopping-cart.html', context)


@login_required(login_url='/useradmin/login/')
def pay(request):
    shopping_cart_is_empty = True
    paid = False
    form = None

    if request.method == 'POST':
        myuser = request.user
        form = PaymentForm(request.POST)
        form.instance.myuser = myuser
        if form.is_valid():
            form.save()
            paid = True

            # Empty the shopping cart
            ShoppingCart.objects.get(myuser=myuser).delete()
        else:
            print(form.errors)

    else:  # request.method == 'GET'
        shopping_carts = ShoppingCart.objects.filter(myuser=request.user)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
            shopping_cart_is_empty = False
            form = PaymentForm(initial={'amount': shopping_cart.get_total()})

    context = {'shopping_cart_is_empty': shopping_cart_is_empty,
               'payment_form': form,
               'paid': paid, }
    return render(request, 'pay.html', context)
