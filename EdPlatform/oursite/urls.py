from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile_admin/', views.profile_admin, name='profile_admin'),
    path('test', views.newCourses, name='newCourses'),
    # path('accounts/profile/', RedirectView.as_view(pattern_name="index")),
    path('upload/', views.upload, name='upload'),
    path('course/', views.courses, name='course'),
    path('course/<int:course_id>/', views.show_course, name='show'),

    url('list', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)