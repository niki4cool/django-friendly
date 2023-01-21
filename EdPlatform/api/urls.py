from django.urls import path
from .views import TestAPIView, test

urlpatterns = [
    path('test-api/', TestAPIView.as_view(), name='test'),
    path('test/', test, name='test'),

]