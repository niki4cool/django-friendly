import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlquote
from requests import Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from django.shortcuts import render, redirect
from taggit.models import Tag
from django.http import request, HttpResponse, Http404
from cart.forms import CartAddProductForm
from .models import Course, Module, Homework, UrlCheck, Constructor
from orders.models import Order, OrderItem
from .models import Video, Subject, VideoForConstructor
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VideoForm, HomeworkForm, CourseForm, ModuleForm, CategoryForm
from .forms import CoursesForm
from .forms import CheckForm
from pytils.translit import slugify
from . import forms
from django.db.models import Q


# Create your views here.
def Search(request):
    query = request.GET.get('q')
    object_list = Course.objects.filter(title__icontains=query)
    return render(request, 'oursite/search.html', {"list":object_list})

def post_list(request):
    return render(request, 'oursite/index.html')

def show_course(request, slug):
    orders = Order.objects.filter(first_name=request.user, paid=True)
    item = OrderItem.objects.filter(order__in=orders)
    course = Course.objects.get(slug=slug)
    module = Module.objects.filter(course=course)
    dz = course.work
    t = OrderItem.objects.filter(order__in=orders, product=course.id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.course = course
            homework.user = User.objects.filter(id=request.user.id).first()
            homework.slug = slug
            course.save()
            homework.save()
            return redirect('oursite:show', slug)
        else:
            homework = HomeworkForm()

    homework = HomeworkForm()
    form = HomeworkForm()
    id = slug
    context = {
        'dz': dz,
        'form': form,
        'id': id,
        'Cour': course,
        'Mod': module
    }
    if t:
        return render(request, 'oursite/id.html', context)
    else:
        return redirect('oursite:profile')
def show_course_playlist(request, slug):
    orders = Order.objects.filter(first_name=request.user, paid=True)
    item = OrderItem.objects.filter(order__in=orders)
    course = Course.objects.get(slug=slug)
    module = Module.objects.filter(course=course)
    dz = course.work
    t = OrderItem.objects.filter(order__in=orders, product=course.id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.course = course
            homework.user = User.objects.filter(id=request.user.id).first()
            homework.slug = slug
            course.save()
            homework.save()
            return redirect('oursite:show', slug)
        else:
            homework = HomeworkForm()

    homework = HomeworkForm()
    form = HomeworkForm()
    id = slug
    context = {
        'dz': dz,
        'id': id,
        'Cour': course,
        'Mod': module,
        'form': form
    }
    if request.method == 'POST':
        var = request.POST.get("videoConstruct", "")
        try:
            if Constructor.objects.get(owner=request.user).owner == User.objects.filter(id=request.user.id).first():
                constructor = Constructor.objects.get(owner=request.user)
                vids = VideoForConstructor.objects.create(constructor=constructor,
                                                          video=var)
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        except:
            const = Constructor.objects.create(owner=User.objects.filter(id=request.user.id).first(),
                                              title='Test',
                                              description='Description',
                                              )
            vids = VideoForConstructor(video=var, constructor_id=const.id)
            vids.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if t:
        return render(request, 'oursite/id_playlist.html', context)
    else:
        return redirect('oursite:profile')

@login_required(login_url='/register')
def constructor(request):
    constructor = Constructor.objects.filter(owner=request.user.id).first()
    vids = VideoForConstructor.objects.filter(constructor=constructor)
    if request.method == 'POST':
        var = request.POST.get("delete", "")
        videoDelete = VideoForConstructor(id=var).delete()
    context = {
    'vids': vids,
    'const': constructor
    }
    return render(request, 'oursite/constructor.html', context)



def upload(request):
    return render(request, 'oursite/upload.html')

def collaboration(request):
    return render(request, 'oursite/collaboration.html')

def contacts(request):
    return render(request, 'oursite/contacts.html')

@login_required(login_url='/register')
def courses(request):
    video = Video.objects.all()
    return render(request, 'oursite/courses.html', {'Vid': video})


@login_required(login_url='/register')

def profile(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    user = User.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect('register')
    orders = Order.objects.filter(first_name=request.user, paid=True)
    item = OrderItem.objects.filter(order__in=orders)

    content = {
        'Ord': orders,
        'Item': item,
        'category': category,
        'categories': categories,
        'products': products
    }
    if request.user.is_staff or request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data.get("subj")
                cat = Subject(subj=data, slug=slugify(data))
                cat.save()

        else:
            categoryf = CategoryForm(request.POST)
        categoryf = CategoryForm(request.POST)
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            form_module = ModuleForm(request.POST, request.FILES)
            if form.is_valid() and form_module.is_valid():
                course = form.save(commit=False)
                module = form_module.save(commit=False)
                course.slug = slugify(course.title)
                course.owner = User.objects.filter(id=request.user.id).first()
                course.save()
                for video in request.FILES.getlist('video'):
                    vids = Module(title="title", description="description", video=video, course=course)
                    vids.save()




                # Module.objects.create(title='test',
                #                       course=course,
                #                       video=course.video)

                return redirect('oursite:profile')
        else:
            course = CourseForm()
            module = ModuleForm()

        course = CourseForm()
        module = ModuleForm()

        data = {
            'form_category': categoryf,
            'form': course,
            'form_module': module,
            'error': error,
            'Ord': orders,
            'Item': item,
            'category': category,
            'categories': categories,
            'products': products

        }
        return render(request, 'oursite/Profile_admin.html', data)
    else:

        return render(request, 'oursite/Profile.html', content)


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

    return render(request, 'oursite/Profile_admin.html', data)


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


def logout(request):
    user = User.objects.filter(id=request.user.id).first()
    return redirect('oursite:register')

@login_required(login_url='/register')
def razrab(request):
    error=""
    check = UrlCheck.objects.all()
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.user = User.objects.filter(id=request.user.id).first()
            newform.save()
            return redirect('oursite:product_list')
    else:
        newform = CheckForm()

    newform = CheckForm()

    data = {
        'check': check,
        'form': newform,
        'error': error,
    }

    return render(request, 'oursite/razrab.html', data)




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



def product_detail(request, id, slug):
    product = get_object_or_404(Course,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'oursite/detail.html', {'product': product,
                                                   'cart_product_form': cart_product_form})
