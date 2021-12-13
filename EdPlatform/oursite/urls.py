from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.views.generic import RedirectView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile_admin/', views.profile_admin, name='profile_admin'),
    # path('accounts/profile/', RedirectView.as_view(pattern_name="index")),
    path('upload/', views.upload, name='upload'),
    path('course/', views.courses, name='course'),
    path('course/<int:course_id>/', views.show_course, name='show'),

]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)