from django.urls import reverse_lazy

from task_manager.tasks.models import Label, Status, Task
from task_manager.tests.base_test_case import BaseTestCase


class TestTaskDetailView(BaseTestCase):
    def test_task_detail_with_uknown_user(self):
        status = Status.objects.first() or \
                 Status.objects.create(name='Default Status')
        task = Task.objects.create(name="Test Task",
                                   status=status,
                                   author=self.user_1)
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': task.id}))
        self.assertRedirectsToLogin(response)

    def test_task_detail(self):
        self.login_user()
        status = Status.objects.first() or \
                 Status.objects.create(name='Default Status')
        task = Task.objects.create(name="Test Task",
                                   status=status,
                                   author=self.user_1)
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': task.id}))
        self.assertTemplateUsed(response, 'tasks/detail_task.html')
        self.assertContains(response, task.name, status_code=200)


class TestTasksViewWithFilter(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status_1 = Status.objects.create(name='Test_status_1')
        self.status_2 = Status.objects.create(name='Test_status_2')
        self.label = Label.objects.create(name='test_label_1')
        Task.objects.create(
            name='test_task_1', status=self.status_1, author=self.user_1)
        task_2 = Task.objects.create(
            name='test_task_2', status=self.status_2, author=self.user_2)
        task_2.labels.add(self.label)

    def test_filter_tasks_without_condition(self):
        self.login_user()
        response = self.client.get(reverse_lazy('tasks:tasks'), {
            'status': '',
            'executor': '',
            'label': '',
            'self_tasks': 'on'
        })

        self.assertContains(response, 'test_task_1', status_code=200)
        self.assertNotContains(response, 'test_task_2', status_code=200)
