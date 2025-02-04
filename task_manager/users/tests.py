from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests.base_test_case import BaseTestCase


class TestUsersView(BaseTestCase):
    def test_users(self):
        self.login_user()
        response = self.client.get(reverse_lazy('users:users'))
        self.assertTemplateUsed(response, 'users/users.html')
        self.assertContains(response, 'testuser1', status_code=200)
        self.assertContains(response, 'testuser2', status_code=200)

    def test_update_get_with_uknown_user(self):
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 1}))
        self.assertRedirectsToLogin(response)

    def test_update_get_with_wrong_user(self):
        self.login_user()
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse_lazy('users:users'), 302, 200)
        self.assertMessage(
            response, 'У вас нет прав для изменения другого пользователя.')

    def test_update_get(self):
        self.login_user()
        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'users/update.html')
        self.assertContains(response, 'Test1', status_code=200)
        self.assertContains(response, 'User1', status_code=200)

    def test_delete_get(self):
        self.login_user()
        response = self.client.get(
            reverse_lazy('users:delete', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertContains(
            response, 'Вы уверены, что хотите удалить Test1 User1',
            status_code=200)

    def test_delete_post(self):
        self.login_user()
        response = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse_lazy('users:users'), 302, 200)
        self.assertMessage(response, 'Пользователь успешно удален')
        self.assertFalse(
            get_user_model().objects.filter(username='testuser1'))

    def test_delete_post_user_with_tasks(self):
        self.login_user()
        status = Status.objects.create(name='Test_status')
        Task.objects.create(
            name='test_task',
            status=status,
            author=get_user_model().objects.filter(
                username='testuser1'
            ).first()
        )
        response = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse_lazy('users:users'), 302, 200)
        self.assertMessage(
            response,
            'Невозможно удалить пользователя, потому что он используется'
        )
        self.assertTrue(
            get_user_model().objects.filter(username='testuser1'))

