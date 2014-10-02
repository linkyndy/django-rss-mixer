from django import forms
from django.forms.widgets import URLInput


class AddFeedForm(forms.Form):
    url = forms.URLField(widget=URLInput({
        'placeholder': 'Feed URL', 'class': 'form-control'}))

