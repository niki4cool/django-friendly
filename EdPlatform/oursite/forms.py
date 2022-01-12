from .models import Video, UrlCheck, Homework, Course, Module, Constructor, VideoForConstructor, Subject
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
        fields = ['title', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'last_name'}),
            'url': forms.TextInput(attrs={'class': 'email'}),
        }


class CourseForm(forms.ModelForm):
    video = forms.FileField()
    class Meta:
        model = Course
        fields = ('category', 'title', 'overview', 'available', 'price', 'image', 'video', 'work')
        widgets = {
            'title': TextInput(attrs={
                'class': 'title',

            }),
            'overview': Textarea(attrs={
                'class': 'overview',

            }),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('video',)
    video = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ('homework_file', 'title')
        homework_file: forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('title',)


