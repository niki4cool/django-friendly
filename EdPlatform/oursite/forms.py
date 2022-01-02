from .models import Video, UrlCheck, Homework, Course, Module
from django.forms import ModelForm, TextInput, Textarea, FileField
from django import forms
from django.forms.models import inlineformset_factory


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['caption', 'description', 'video', 'preview', 'tags']

        widgets = {
            'caption': TextInput(attrs={
                'class': 'frm1',

            }),
            'description': Textarea(attrs={
                'class': 'frm2',

            }),
            'tags': Textarea(attrs={
                'class': 'frm3',

            }),

        }



class CoursesForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video',)
        video: forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class CheckForm(forms.ModelForm):
    class Meta:
        model = UrlCheck
        fields = ['user', 'url']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('owner', 'category', 'title', 'slug', 'overview', 'available', 'price', 'image')

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('video',)
        video: forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('title', 'user', 'slug', 'homework_file',)
        homework_file: forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

