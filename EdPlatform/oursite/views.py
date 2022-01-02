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
from .models import Course, Module, Homework
from orders.models import Order, OrderItem
from .models import Video, Subject
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VideoForm, HomeworkForm, CourseForm, ModuleForm
from .forms import CoursesForm
from .forms import CheckForm
from . import forms
from django.db.models import Q


# Create your views here.

def post_list(request):
    video = Video.objects.all()
    return render(request, 'oursite/index.html', {'Vid': video})


def show_course(request, slug):
    course = Course.objects.get(slug=slug)
    module = Module.objects.filter(course=course)
    form = HomeworkForm(request.POST, request.FILES)
    if form.is_valid():
        response = form.save(commit=False)
        response.user = request.user
        response.save()

    form = HomeworkForm()
    id = slug
    context = {
        'form': form,
        'id': id,
        'Cour': course,
        'Mod': module
    }
    return render(request, 'oursite/id.html', context)

def show_course_playlist(request, slug):
    course = Course.objects.get(slug=slug)
    module = Module.objects.filter(course=course)
    homework = Homework.objects.filter(course=course)

    form = HomeworkForm(request.POST, request.FILES)
    if form.is_valid():
        response = form.save(commit=False)
        response.user = request.user
        response.save()

    form = HomeworkForm()
    id = slug
    context = {
        'form': form,
        'id': id,
        'Cour': course,
        'Mod': module,
        'Home': Homework
    }
    return render(request, 'oursite/id_playlist.html', context)



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
    orders = Order.objects.all()
    item = OrderItem.objects.all()
    content = {
        'Ord': orders,
        'Item': item
    }
    if request.user.is_staff or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            form_homework = HomeworkForm(request.POST, request.FILES)
            form_module = ModuleForm(request.POST, request.FILES)
            if form.is_valid() and form_homework.is_valid() and form_module.is_valid():
                form.save()
                form_homework.save()
                form_module.save()
                return redirect('oursite:profile')
        else:
            form = CourseForm()
            form_homework = HomeworkForm()
            form_module = ModuleForm()

        form = CourseForm()
        form_homework = HomeworkForm()
        form_module = ModuleForm()

        data = {
            'form': form,
            'form_homework': form_homework,
            'form_module': form_module,
            'error': error,
            'Ord': orders,
            'Item': item
        }
        return render(request, 'oursite/profile_admin.html', data)
    else:

        return render(request, 'oursite/profile.html', content)


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
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('course')
    else:
        form = CourseForm()

    form = CourseForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'oursite/profile_admin.html', data)


def index(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except:
        form = UserCreationForm(request.POST)
        return render(request, 'registration/register.html', {'form': form})
        quit()

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

def razrab(request):
    error=""
    user = models.User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            newform = form.save(commit=False)
            form.instance.user = request.user
            newform.save()
            return redirect('oursite:profile')
    else:
        form = CheckForm()

    form = CheckForm()

    data = {
        'form': form,
        'error': error,
        'user': user
    }

    return render(request, 'oursite/razrab.html', data)



@login_required(login_url='/register')
def product_list(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'oursite/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


@login_required(login_url='/register')
def product_detail(request, id, slug):
    product = get_object_or_404(Course,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'oursite/detail.html', {'product': product,
                                                   'cart_product_form': cart_product_form})
