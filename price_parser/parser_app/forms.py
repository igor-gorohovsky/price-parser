from django import forms
from .models import Urls
from django.core.validators import URLValidator


class MultiUrlField(forms.Field):

    def to_python(self, value):
        """Normalize data to a list of strings"""
        # Return an empty list if no input was given
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid urls"""
        super().validate(value)
        for url in value:
            validate = URLValidator()
            validate(url)


class UrlsForm(forms.ModelForm):
    url = MultiUrlField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label='Add URL',
    )

    class Meta:
        model = Urls
        fields = ['url',]
