from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import (
    gettext_lazy as _,
)

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class CreateTaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label=_('Name'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Name')})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Labels'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        labels = {
            'description': _('Description'),
            'executor': _('Executor')
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Description'),
                'cols': '40',
                'rows': '10',
            }),
        }
