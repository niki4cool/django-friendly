from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from django.shortcuts import render, redirect
from taggit.models import Tag
from django.http import request, HttpResponse
from cart.forms import CartAddProductForm
from oursite.models import Course, Module
from .models  import  Video
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VideoForm
from .forms import CoursesForm

# Create your views here.

def post_list(request):
    video = Video.objects.all()
    return render(request, 'oursite/index.html', {'Vid': video})


def show_course(request, course_id):
    video = Video.objects.get(pk=course_id)
    id = course_id
    context = {
        'id':id,
        'Vid': video
    }
    return render(request, 'oursite/id.html', context)


def upload(request):

    return render(request, 'oursite/upload.html')

@login_required(login_url='/register')
def courses(request):
    video = Video.objects.all()
    return render(request, 'oursite/courses.html', {'Vid': video})

@login_required(login_url='/register')
def profile(request):
    user = User.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect('register')
    if request.user.is_staff or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('course')
        else:
            form = VideoForm()

        form = VideoForm()

        data = {
            'form': form,
            'error': error
        }
        return render(request, 'oursite/profile_admin.html', data)
    else:
        return render(request, 'oursite/profile.html')

@login_required(login_url='/register')
def newCourses(request):
    user = User.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect('register')
    if request.user.is_staff or request.user.is_superuser:
        error = ''

        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course')
        else:
            form = CoursesForm()

        form = CoursesForm()

        data = {
            'form': form,
            'error': error
        }
        return render(request, 'oursite/test.html', data)
    else:
        return render(request, 'oursite/test.html')

@login_required(login_url='/register')
def profile_admin(request):
    error = ''
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course')
    else:
        form = VideoForm()

    form = VideoForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'oursite/profile_admin.html', data)


def index(request):
    user = User.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect('login')

    return render(request, 'oursite/index.html')
    raise_exception = True


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


def product_list(request, category_slug=None):
    category = None
    categories = Module.objects.all()
    products = Course.objects.all()
    if category_slug:
        category = get_object_or_404(Module, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'oursite/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Course,
                                id=id,
                                slug=slug,
                                )
    cart_product_form = CartAddProductForm()
    return render(request, 'OurSite/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})

