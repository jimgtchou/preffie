from django import forms
from django.forms import ModelForm, Textarea
from .models import Poll
from django.core.files.base import ContentFile

class PollCreateForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ('media_a', 'media_b', 'caption')
        widgets = {
            'caption': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
