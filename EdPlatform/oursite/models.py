import uuid

from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from embed_video.fields import EmbedVideoField
from django.utils.translation import gettext as _



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Video(models.Model):
    caption=models.CharField(max_length=100)
    description = models.TextField()
    video=models.FileField(upload_to='video/')
    preview=models.ImageField(upload_to='media/')
    tags=models.TextField()
    def __str__(self):
        return self.caption

class Subject(models.Model):
    subj = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('subj',)

    def __str__(self):
        return self.subj

    def get_absolute_url(self):
        return reverse('oursite:product_list_by_category',
                       args=[self.slug])

    def get_absolute_url_buy(self):
        return reverse('oursite:product_list_by_category_buy',
                       args=[self.slug])

    def get_absolute_url_recommendations(self):
        return reverse('oursite:recommendations_by_category',
                       args=[self.slug])

class Notifications(models.Model):
    members = models.ManyToManyField(User, verbose_name=_("Пользователь"))
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    title = models.CharField(max_length=200)
    clickbait = models.TextField()
    overview = models.TextField()
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField(_('Дата уведомления'), default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('oursite:notification',
                       args=[self.id])

class ImageForUser(models.Model):
    user = models.ForeignKey(User, related_name='userPic', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', default='../static/images/v20_51.png')
    userstr = str(user)
    def __str__(self):
        return str(self.user)

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))


    def get_absolute_url(self):
        return reverse('oursite:messages', args=[self.pk])


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    selling = models.BooleanField(default=True)
    category = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default=uuid.uuid1())
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    number = models.CharField(max_length=200)
    created_date = models.DateTimeField(editable=True, auto_now_add=True)



    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('oursite:product_detail',
                       args=[self.id, self.slug])

    def url_to_course(self):
        return reverse('oursite:show',
                       args=[self.slug])

    def url_to_catalog(self):
        return reverse('oursite:seller_catalog',
                       args=[self.owner])

    def url_to_catalog_buy(self):
        return reverse('oursite:buyer_catalog',
                       args=[self.owner])

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.ImageField(upload_to='video/')
    slug = models.SlugField(max_length=200, default=uuid.uuid1())
    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.title


class UrlCheck(models.Model):
    title = url = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Homework(models.Model):
    course = models.ForeignKey(Course, related_name='homework', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    homework_file = models.FileField(upload_to='homework/')
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

class Constructor(models.Model):
    owner = models.ForeignKey(User, related_name='constructor_created',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, default=uuid.uuid1())

class VideoForConstructor(models.Model):
    constructor = models.ForeignKey(Constructor, related_name='constr', on_delete=models.CASCADE)
    video = models.CharField(max_length=200)

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': ('text',
                                                                                  'video',
                                                                                  'image',
                                                                                  'file')},on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


