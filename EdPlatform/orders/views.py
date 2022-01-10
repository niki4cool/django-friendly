from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.first_name = str(User.objects.filter(id=request.user.id).first())
            order.address = 'EKB'
            order.postal_code = '623070'
            order.city = 'EKB'
            for item in cart:
                OrderItem.objects.create(first_name=User.objects.filter(id=request.user.id).first(),
                                         order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            order = form.save()
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        order = OrderCreateForm
    order = OrderCreateForm()

    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': order})
