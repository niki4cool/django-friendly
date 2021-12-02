from django.urls import path, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', RedirectView.as_view(pattern_name="index")),
    path('upload/', views.upload, name='upload'),
    path('course/', views.courses, name='course')

]