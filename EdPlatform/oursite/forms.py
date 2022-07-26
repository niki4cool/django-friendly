from .models import Video, UrlCheck, Course, Module, Constructor, VideoForConstructor, Subject, Message, Chat, ImageForUser
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

class SearchForm(forms.Form):
    fields = ['from', 'to']
    CHOICES = [('1', '24h'),
               ('2', '7d'),
               ('3', 'all')]
    date = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    widgets = {
        'from': TextInput(attrs={
            'class': 'from',

        }),
        'to': TextInput(attrs={
            'class': 'to',

        }),
    }


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
        fields = ('category', 'title', 'overview', 'available', 'price', 'image', 'video', 'number', 'selling')
        widgets = {
            'title': TextInput(attrs={
                'class': 'title',

            }),
            'overview': Textarea(attrs={
                'class': 'overview',

            }),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('video',)
    video = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('subj',)

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageForUser
        fields = ['image']