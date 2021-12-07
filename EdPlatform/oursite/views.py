from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from django.shortcuts import render
from taggit.models import Tag
from django.http import request
from cart.forms import CartAddProductForm
from oursite.models import Course
from .models  import  vid

# Create your views here.

def post_list(request):
    Vid = vid.objects.get()
    context = {
        'Vid': Vid,
    }
    return render(request, 'oursite/index.html', context)

def upload(request):

    return render(request, 'oursite/upload.html')

def courses(request):
    Vid = vid.objects.get()
    context = {
        'Vid': Vid,
    }
    return render(request, 'oursite/courses.html', context)

def index(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except:
        form = UserCreationForm(request.POST)
        return render(request, 'registration/register.html', {'form': form})
        quit()
    maincycle = models.MainCycle.objects.get(user=request.user)

    return render(request, 'oursite/index.html', {
        'maincycle': maincycle,
        'boosts': boosts,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def index_(request):
    return render(request, 'index.html')


def product_detail(request, id, slug):
    product = get_object_or_404(Course,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'OurSite/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})

