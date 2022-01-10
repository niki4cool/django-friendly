from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['last_name', 'email',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'last_name'}),
            'email': forms.TextInput(attrs={'class': 'email'}),
        }
