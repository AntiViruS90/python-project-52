from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy


class BaseTestCase(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user_1 = self.user_model.objects.create_user(
            username='testuser1',
            password='password123',
            first_name='Test1',
            last_name='User1'
        )
        self.user_2 = self.user_model.objects.create_user(
            username='testuser2',
            password='password123',
            first_name='Test2',
            last_name='User2'
        )

    def login_user(self, user=None):
        if user is None:
            user = self.user_1
        self.client.login(username=user.username, password='password123')

    def assertMessage(self, response, expected_message):
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), expected_message)

    def assertRedirectsToLogin(self, response):
        self.assertRedirects(
            response, reverse_lazy('main:login'), 302, 200
        )
        self.assertMessage(
            response, 'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
