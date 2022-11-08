from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from oursite.models import Course, Module, ImageForUser
from .cart import Cart
from .forms import CartAddProductForm
from orders.models import Order, OrderItem
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

#import to use iframe
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Course, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Course, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required(login_url='/register')
@xframe_options_sameorigin

def cart_detail(request):
    image = ImageForUser.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'image': image,
                                                'user': user})

