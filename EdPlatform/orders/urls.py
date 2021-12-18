from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url('', views.order_create, name='order_create'),
]
