from django import forms
from django.utils.translation import (
    gettext_lazy as _,
)

from .models import Label


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

        labels = {
            'name': _('Name')
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Name')
                }),
        }
