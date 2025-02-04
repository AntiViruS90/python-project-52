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
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.mixins import (
    UserLoginRequiredMixin,
)

from .filter import TasksFilter
from .forms import CreateTaskForm
from .mixins import AuthorPermissionTestMixin
from .models import Task


class TaskView(UserLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    filterset_class = TasksFilter


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail_task.html'
    context_object_name = 'task'


class CreateTaskView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create_task.html'
    success_message = _('Task successfully created')
    success_url = reverse_lazy('tasks:tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/update_task.html'
    success_message = _('Task successfully changed')
    success_url = reverse_lazy('tasks:tasks')


class DeleteTaskView(
    UserLoginRequiredMixin,
    SuccessMessageMixin,
    AuthorPermissionTestMixin,
    DeleteView
):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully deleted')
