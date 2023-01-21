from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'cart'

urlpatterns = [
    # url('api/favouriteShow', views.FavouriteShow.as_view(), name='favourite'),
    url(r'^$', views.cart_detail, name='cart_detail'),
    url('^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]