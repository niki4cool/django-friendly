from .models import Video
from django.forms import ModelForm, TextInput, Textarea, FileField
from django import forms


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields =['caption', 'description', 'video', 'preview', 'tags']

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
        fields =('video',)
        video: forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
