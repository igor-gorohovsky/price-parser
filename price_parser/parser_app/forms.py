from django import forms
from .models import Urls


class UrlsForm(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ['url',]
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control',}),
        }
        labels = {
            'url': 'Add URL',
        }
