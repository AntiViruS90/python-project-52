from django.contrib.messages.views import (
    SuccessMessageMixin,
)
from django.urls import reverse_lazy
from django.utils.translation import (
    gettext_lazy as _,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.mixins import (
    DeleteProtectErrorMixin,
    UserLoginRequiredMixin,
)

from .forms import CreateStatusForm
from .models import Status


class StatusesView(UserLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class CreateStatusView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_message = _('Status successfully created')
    success_url = reverse_lazy('statuses:statuses')


class UpdateStatusView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Status
    form_class = CreateStatusForm
    template_name = 'statuses/update_status.html'
    success_message = _('Status succesfully changed')
    success_url = reverse_lazy('statuses:statuses')


class DeleteStatusView(
    UserLoginRequiredMixin,
    DeleteProtectErrorMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status succesfully deleted')
    delete_error_message = _(
        'It is not possible to delete the status because it is in use')

