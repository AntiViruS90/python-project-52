from django.contrib.auth.views import (
    get_user_model,
)
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.tasks.models import Task

from .forms import CreateTaskForm
from .models import Status

test_user_1 = {
    "first_name": 'test_first_name_1',
    "last_name": 'test_last_name_1',
    "username": 'test_username_1',
    "password": 'test1'
}
test_user_2 = {
    "first_name": 'test_first_name_2',
    "last_name": 'test_last_name_2',
    "username": 'test_username_2',
    "password": 'test2'
}


class TestCreateTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user_1)

    def test_create_task_get_with_uknown_user(self):
        response = self.client.get(reverse_lazy('tasks:create'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_create_task_get(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(reverse_lazy('tasks:create'))

        self.assertTemplateUsed(response, 'create_task.html')
        self.assertContains(response, 'Имя', status_code=200)
        self.assertContains(response, 'Описание', status_code=200)
        self.assertContains(response, 'Статус', status_code=200)
        self.assertContains(response, 'Исполнитель', status_code=200)

    def test_create_task_post(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user_1['username'])
        response = self.client.post(reverse_lazy('tasks:create'), {
            "name": 'test_task',
            "status": status.pk
        })
        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

        new_task = Task.objects.get(name="test_task")
        self.assertTrue(new_task)
        self.assertEqual(new_task.author, author)


class TestCreateTaskForm(TestCase):
    def test_right(self):
        status = Status.objects.create(name='Test_status')
        form = CreateTaskForm(data={
            "name": 'test_first_name',
            "status": status
        })
        self.assertTrue(form.is_valid())

    def test_with_empty_name_field(self):
        status = Status.objects.create(name="Test_status")
        form = CreateTaskForm(data={
            "name": "",
            "status": status
        })
        self.assertFalse(form.is_valid())

    def test_with_empty_status_field(self):
        form = CreateTaskForm(data={
            'name': "test_first_name",
            "status": ''
        })
        self.assertFalse(form.is_valid())


class TestDeleteTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user_1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user_1['username'])
        Task.objects.create(name='test_task', status=status, author=author)

    def test_delete_task_get_with_uknown_user(self):
        response = self.client.get(reverse_lazy(
            'tasks:delete', kwargs={'pk': 1})
        )
        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_task_get(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(reverse_lazy(
            'tasks:delete', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'delete_task.html')
        self.assertContains(response,
                            'Вы уверены, что хотите удалить test_task?',
                            status_code=200)
        self.assertContains(response, 'Да, удалить', status_code=200)

    def test_delete_task_post(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.post(reverse_lazy(
            'tasks:delete', kwargs={'pk': 1}))
        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')
        self.assertFalse(Task.objects.filter(name='test_task'))


class TestUpdateTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user_1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user_1['username'])
        Task.objects.create(name='test_task', status=status, author=author)

    def test_update_task_get_with_uknown_user(self):
        response = self.client.get(reverse_lazy(
            'tasks:update', kwargs={'pk': 1})
        )
        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_update_task_get(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(reverse_lazy(
            'tasks:update', kwargs={'pk': 1})
        )
        self.assertTemplateUsed(response, 'update_task.html')
        self.assertContains(response, 'test_task', status_code=200)

    def test_delete_task_post(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': 1})
        )
        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

        self.assertFalse(Task.objects.filter(name='test_task'))


class TestTaskDetailView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user_1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user_1['username'])
        Task.objects.create(name='test_task', status=status, author=author)

    def test_task_detail_with_uknown_user(self):
        response = self.client.get(reverse_lazy(
            'tasks:detail', kwargs={'pk': 1})
        )
        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(reverse_lazy(
            'tasks:detail', kwargs={'pk': 1})
        )
        self.assertTemplateUsed(response, 'detail_task.html')
        self.assertContains(response, 'test_task', status_code=200)
        self.assertContains(response, 'Test_status', status_code=200)


class TestTasksView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user_1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user_1['username'])
        Task.objects.create(name='test_task_1', status=status, author=author)
        Task.objects.create(name='test_task_2', status=status, author=author)

    def test_tasks_with_uknown_user(self):
        response = self.client.get(reverse_lazy('tasks:tasks'))

        self.assertRedirects(
            response,
            reverse_lazy('main:login'),
            status_code=302,
            target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(reverse_lazy('tasks:tasks'))
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertContains(response, 'test_task_1', status_code=200)
        self.assertContains(response, 'test_task_2', status_code=200)

    def test_filter_tasks_without_conditions(self):
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password']
        )
        response = self.client.get(
            reverse_lazy('tasks:tasks'),
            kwargs={
                'status': '',
                'executor': '',
                'label': '',
            },
        )
        self.assertContains(response, 'test_task_1', status_code=200)
        self.assertContains(response, 'test_task_2', status_code=200)


class TestTasksViewWithFilter(TestCase):
    def setUp(self):
        users = get_user_model()
        author_1 = users.objects.create_user(**test_user_1)
        author_2 = users.objects.create_user(**test_user_2)
        self.client.login(
            username=test_user_1['username'],
            password=test_user_1['password'])
        status_1 = Status.objects.create(name='Test_status_1')
        status_2 = Status.objects.create(name='Test_status_2')
        label = Label.objects.create(name='test_label_1')
        Task.objects.create(
            name="test_task_1",
            status=status_1,
            author=author_1
        )
        Task.objects.create(
            name='test_task_2',
            status=status_2,
            author=author_2,
            executor=author_1
        ).labels.add(label)

    def test_filter_tasks_without_conditions(self):
        response = self.client.get(
            reverse_lazy('tasks:tasks'), {
                'status': '',
                'executor': '',
                'label': '',
                'self_tasks': 'on'
            },
        )
        self.assertContains(response, 'test_task_1', status_code=200)
        self.assertNotContains(response, 'test_task_2', status_code=200)

    def test_filter_tasks_by_status(self):
        response = self.client.get(
            reverse_lazy('tasks:tasks'), {
                'status': '1',
                'executor': '',
                'label': '',
            },
        )
        self.assertContains(response, 'test_task_1', status_code=200)
        self.assertNotContains(response, 'test_task_2', status_code=200)

    def test_filter_tasks_by_executor(self):
        response = self.client.get(
            reverse_lazy('tasks:tasks'), {
                'status': '',
                'executor': '1',
                'label': '',
            },
        )
        self.assertContains(response, 'test_task_2', status_code=200)
        self.assertNotContains(response, 'test_task_1', status_code=200)

    def test_filter_tasks_by_all_options(self):
        response = self.client.get(
            reverse_lazy('tasks:tasks'), {
                'status': '2',
                'executor': '1',
                'label': '1',
            },
        )
        self.assertContains(response, 'test_task_2', status_code=200)
        self.assertNotContains(response, 'test_task_1', status_code=200)
