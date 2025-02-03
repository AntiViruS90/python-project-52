from django import forms
from django.utils.translation import (
    gettext_lazy as _,
)

from .models import Status


class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
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
