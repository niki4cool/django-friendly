from .models import Video
from django.forms import ModelForm, TextInput, Textarea, FileField


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
