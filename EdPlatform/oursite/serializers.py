from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Course, Module, ImageForUser, Homework, User, Constructor, Content, Message,Notifications, Post
from . import models

class ConstructorSerializerOfCurrentUser(serializers.ModelSerializer):
    # username = serializers.CharField()

    class Meta:
        model = Constructor
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'author')

class LoginSerializer(serializers.Serializer):

    id = serializers.CharField(required=False)
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    def getSession(self, request):
        return request.session

        raise serializers.ValidationError("Incorrect Credentials")
    def get_count(self,obj):
        request = self.context.get("request")
        user_id = request.user.id

        return


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('video',)


class CourseSerializer(serializers.ModelSerializer):
    # categoryTitle = serializers.CharField(source="category.title", read_only=True)
    modules = ModuleSerializer(many=True)
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(CourseSerializer, self).to_representation(instance)
        rep['category'] = instance.category.subj
        return rep


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email')

class ImageUserSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    class Meta:
        model = ImageForUser
        fields = ('user', 'image',)


class ConstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructor
        fields = ('id', 'title', 'description', 'slug', 'owner')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        image = ImageForUser.objects.create(image="video/v20_51.png", user_id=user.id)
        return user

class ModuleCreateSerializer(serializers.ModelSerializer):
    # vid = serializers.ImageField()
    class Meta:
        model = Module
        fields = ('video',)

    # def create(self, validated_data):
    #     modules = Module.objects.create(**validated_data)
    #     return modules

class CreateCourseSerializer(serializers.ModelSerializer):
    modules = ModuleCreateSerializer()
    owner_id = serializers.CharField()
    class Meta:
        model = Course
        fields = ('owner_id', 'title', 'price', 'overview', 'category', 'image', 'number', 'modules')



    def create(self, validated_data):
        # userId = self.userId
        modules_data = validated_data.pop('modules')
        course = Course.objects.create(**validated_data)
        Module.objects.create(title="title", course_id=course.id, **modules_data)
        # modules.set()
        # modules = Module.objects.create(video=modules)
        return course

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'owner', 'overview', 'created', 'url_to_course', 'url_to_catalog', 'url_to_catalog_buy')

class RecommendByUserSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(RecommendByUserSerializer, self).to_representation(instance)
        rep['category'] = instance.category.subj
        return rep






class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(SearchSerializer, self).to_representation(instance)
        rep['category'] = instance.category.subj
        return rep