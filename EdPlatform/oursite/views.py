import os
import uuid

from django.urls import reverse
import requests
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlquote
from django.views import View
from requests import Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from django.shortcuts import render, redirect
from taggit.models import Tag
from django.http import request, HttpResponse, Http404, HttpResponseRedirect
from cart.forms import CartAddProductForm
from .models import Course, Module, Homework, UrlCheck, Constructor, Chat, Message, ImageForUser, Notifications
from orders.models import Order, OrderItem
from .models import Video, Subject, VideoForConstructor
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VideoForm, CourseForm, ModuleForm, CategoryForm, SearchForm, MessageForm, ImageForm
from .forms import CoursesForm
from .forms import CheckForm
from pytils.translit import slugify
from . import forms
from django.db.models import Q, Count

#import to use iframe
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin


# Create your views here.
def Search(request):
    query = request.GET.get('q')
    print("gdsgfdsgd")
    # object_list = Course.objects.filter(title__iregex=query)
    object_list = Course.objects.filter(title__iregex=query, available=True)
    cart_product_form = CartAddProductForm()
    type1 = ""
    type2 = ""
    price_from = ""
    price_to = ""
    time = ""

    if request.method == 'POST':
        type1 = request.POST.get('buy')
        type2 = request.POST.get('sell')
        price_from = request.POST.get('from')
        price_to = request.POST.get('to')
        time = request.POST.get('time')
        if type1 == "buy" and type2 == "sell":
            print("all :)")
        elif type1 == 'buy':
            object_list = object_list.filter(selling=True)
            print(type1)
        elif type2 == 'sell':
            object_list = object_list.filter(selling=False)
            print(type1)
        if len(price_from) != 0:
            object_list = object_list.filter(price__gte=price_from)
        if len(price_to) != 0:
            object_list = object_list.filter(price__lte=price_to)
        if time == "7d":
            object_list = object_list.filter(created_date__gte=datetime.today()-timedelta(days=7))
        elif time == "24h":
            object_list = object_list.filter(created_date__gte=datetime.today() - timedelta(days=1))
    data = {
        't1': type1,
        't2': type2,
        'price_from': price_from,
        'price_to': price_to,
        'time': time,
        'list': object_list,
        'query': query,
        'cart_product_form':cart_product_form
    }
    return render(request, 'oursite/search.html', data)


def post_list(request):
    return render(request, 'oursite/index.html')



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
@xframe_options_sameorigin

def profilee(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(owner=request.user, available=True, selling=True)

    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)

    image = ImageForUser.objects.get(user=request.user)

    user = User.objects.get(username=request.user)


    return render(request, 'oursite/Profile_.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'image': image,
                   'user': user})



@login_required(login_url='/register')

def profile_archive(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(owner=request.user, available=False, selling=True)
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    print(products)
    image = ImageForUser.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    return render(request, 'oursite/Profile_archive.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'image': image,
                   'user': user
                   })

@login_required(login_url='/register')
@xframe_options_sameorigin

def profile_buying(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(owner=request.user, available=True, selling=False)
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    image = ImageForUser.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    return render(request, 'oursite/Profile_buying.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'image': image,
                   'user': user
                   })

@login_required(login_url='/register')

def profile_buying_archive(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    products = Course.objects.filter(owner=request.user, available=False, selling=False)
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    image = ImageForUser.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    return render(request, 'oursite/Profile_buying_archive.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'image': image,
                   'user': user
                   })

@login_required(login_url='/register')
def profile_manage(request, category_slug=None):

    user = get_object_or_404(User,
                             id=request.user.id)

    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    image = ImageForUser.objects.get(user=request.user)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        username = request.POST.get('username')
        user.username = username
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        #if image.first() == None:
        if not image:
            print('1')
            if form.is_valid():
                t = form.save(commit=False)
                t.user = request.user
                t.save()
                return redirect('oursite:profile_manage')
        else:
            print('2')
            instance = ImageForUser.objects.get(user=request.user)
            t = ImageForm(request.POST, request.FILES, instance=instance)
            t.save()



    else:
        form = ImageForm()

    imgg = ImageForUser.objects.get(user=request.user)
    userr = User.objects.get(username=request.user)
    return render(request, 'oursite/Profile_manage.html', {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'form': form,
        'img': imgg,
        'user': userr
    })


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
    if 1 == 1:
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
                course.slug = uuid.uuid1()
                course.owner = User.objects.filter(id=request.user.id).first()
                course.save()
                for video in request.FILES.getlist('video'):
                    vids = Module(title="title", description="description", video=video, course=course)
                    vids.save()




                # Module.objects.create(title='test',
                #                       course=course,
                #                       video=course.video)

                return redirect('oursite:confirm')
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


def confirm(request):
    return render(request, 'oursite/confirm.html')

def negative(request):
    return render(request, 'oursite/negative.html')

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
    user = User.objects.get(username=request.user)

    try:
        user = models.User.objects.get(id=request.user.id)
    except:
        form = UserCreationForm(request.POST)
        return render(request, 'registration/register.html', {'form': form})
        quit()

    return render(request, 'oursite/index.html', {'user': user})
    raise_exception = True


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            name = request.POST.get('username')
            user.first_name = name
            user.save()
            img = ImageForUser.objects.create(user=user)

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


def recommendations(request, category_slug=None):
    category = None
    categories = Subject.objects.all()


    if request.user.is_authenticated:
        user_products_selling = Course.objects.filter(owner=request.user, selling=True)
        user_products_buying = Course.objects.filter(owner=request.user, selling=False)
        catts1 = []
        result = []
        result_buying = []
        for i in categories:
            if user_products_buying.filter(category=i):
                user_products_buying.filter(category=i)
                catts1.append(i)
        for g in catts1:
            products_selling = Course.objects.filter(~Q(owner=request.user), selling=True).filter(category=g)
            result.append(products_selling)

        catts2 = []
        for i in categories:
            if user_products_selling.filter(category=i):
                user_products_selling.filter(category=i)
                catts2.append(i)
        for g in catts2:

            products_buying = Course.objects.filter(~Q(owner=request.user), selling=False).filter(category=g)
            result_buying.append(products_buying)

        result.extend(result_buying)
    else:
        result = Course.objects.filter(available=True)


    cart_product_form = CartAddProductForm()
    if not request.user.is_authenticated:
        if category_slug:
            result = Course.objects.filter(available=True)
            tempArr = []
            for t in result:
                category = get_object_or_404(Subject, slug=category_slug)
                if t.category == category:
                    tempArr.append(t)

            result = tempArr
            print(result)
    else:
        if category_slug:
            temparr = []
            for t in result:
                category = get_object_or_404(Subject, slug=category_slug)
                t = t.filter(category=category)
                temparr.append(t)
            result = temparr


    return render(request,
                  'oursite/recommendations.html',
                  {'category': category,

                   'result': result,
                   'categories': categories,

                   'cart_product_form': cart_product_form})

def product_list(request, category_slug=None):

    category = None
    categories = Subject.objects.all()
    if not request.user.is_authenticated:
        products = Course.objects.filter(available=True, selling=True)
    else:
        products = Course.objects.filter(~Q(owner=request.user), available=True, selling=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'oursite/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart_product_form': cart_product_form})


def product_list_buy(request, category_slug=None):
    category = None
    categories = Subject.objects.all()
    if not request.user.is_authenticated:
        products = Course.objects.filter(available=True, selling=False)
    else:
        products = Course.objects.filter(~Q(owner=request.user), available=True, selling=False)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Subject, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'oursite/list_buy.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'cart_product_form': cart_product_form})


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




def product_detail(request, id, slug):
    product = get_object_or_404(Course,
                                id=id,
                                slug=slug,
                                available=True)
    module = Module.objects.filter(course=product)
    cart_product_form = CartAddProductForm()
    neededUser = product.owner
    print(neededUser)
    user_id = neededUser.id
    first_name = neededUser.first_name
    last_name = neededUser.last_name
    query = request.GET.get('q')
    catalog = Course.objects.filter(owner=user_id)

    if query:
        if request.user.id:
            CreateDialogView.get(request, request, user_id)
            chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
            chat = chats.first()
            return redirect(reverse('oursite:messages', kwargs={'chat_id': chat.id}))
        else:
            return redirect('oursite:register')
    return render(request, 'oursite/detail.html', {'product': product,
                                                   'cart_product_form': cart_product_form,
                                                   'module': module,
                                                   'neededUser':neededUser,
                                                   'catalog': catalog,
                                                   'first_name': first_name,
                                                   'last_name': last_name})


class DialogsView(View):
    def get(self, request):
        if request.user.is_authenticated == False:
            return redirect('login')
        chats = Chat.objects.filter(members__in=[request.user.id])
        members = []
        messages = []
        checkMessages = False
        for chat in chats:

            first = chat.members.all().first()
            second = chat.members.all().last()
            if not str(first) in members:
                members.append(str(first))
            if not str(second) in members:
                members.append(str(second))

        for member in members:
            user = User.objects.filter(username=member)

            message = Message.objects.filter(author=user.first())
            if not message.first() == None:
                messages.append(message.first())
        if messages:
            checkMessages = True
        image = ImageForUser.objects.get(user=request.user)
        # chat_member = chats.members.filter(~Q(username=request.user))

        for chat in chats:
            member = chat.members.filter(~Q(username=request.user))
            images = ImageForUser.objects.all()
        return render(request, 'oursite/dialogs.html', {'user_profile': request.user, 'chats': chats, 'checkMessages': checkMessages, 'member': member, 'image': image, 'images': images})


class MessagesView(View):

    def get(self, request, chat_id):
        if request.user.is_authenticated == False:
            return redirect('login')
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None
        chat_member = chat.members.get(~Q(username=request.user))
        image = ImageForUser.objects.get(user=request.user)
        chat_image = ImageForUser.objects.get(user=chat_member)
        print(chat_image)

        return render(
            request,
            'oursite/messages.html',
            {
                'image': image,
                'chat_image': chat_image,
                'chat_member': chat_member,
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        if request.user.is_authenticated == False:
            return redirect('login')
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('oursite:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        if request.user.is_authenticated == False:
            return redirect('login')
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        user = get_object_or_404(User,
                                 id=user_id)
        # user = User.objects.filter(id=user_id)

        # if not (Message.objects.filter(chat=chats.first())):
        #     msg = Message(chat=chats.first(), author=user, message="Хотите что-то спросить?")
        #     msg.save()
        return redirect(reverse('oursite:messages', kwargs={'chat_id': chat.id}))

@login_required(login_url='/register')
def notifications(request):
    image = ImageForUser.objects.get(user=request.user)
    nots = Notifications.objects.filter(members__in=[request.user.id])
    return render(request, 'oursite/notifications.html', {'nots': nots,
                                                          'image': image})
@login_required(login_url='/register')
def notification(request, id):
    image = ImageForUser.objects.get(user=request.user)
    nots = get_object_or_404(Notifications,
                                id=id)
    return render(request, 'oursite/notification.html', {'nots': nots,
                                                         'image': image})

def seller_catalog(request, owner):
    id = get_object_or_404(User,
                           username=owner)
    if request.user.is_authenticated:
        image = ImageForUser.objects.get(user=request.user)
    else:
        image = ImageForUser.objects.get(user=id.id)


    catalog = Course.objects.filter(owner=id, selling=True, available=True)
    if catalog:
        product = catalog[0]
    else:
        noproduct = Course.objects.filter(owner=id, selling=False, available=True)
        product = noproduct[0]


    return render(request, 'oursite/seller_catalog.html', {'catalog': catalog,
                                                           'id': id,
                                                           'product': product,
                                                           'image': image})
#
#
def buyer_catalog(request, owner):
    id = get_object_or_404(User,
                           username=owner)
    if request.user.is_authenticated:
        image = ImageForUser.objects.get(user=request.user)
    else:
        image = ImageForUser.objects.get(user=id.id)
    catalog = Course.objects.filter(owner=id, selling=False, available=True)
    if catalog:
        product = catalog[0]
    else:
        noproduct = Course.objects.filter(owner=id, selling=True, available=True)
        product = noproduct[0]

    return render(request, 'oursite/buyer_catalog.html', {'catalog': catalog,
                                                           'id': id,
                                                           'product': product,
                                                          'image': image})