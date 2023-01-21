from django.contrib.auth import authenticate
from rest_framework import serializers
from oursite.models import Course, Module, ImageForUser

class FavouriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'overview')