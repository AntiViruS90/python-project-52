from django.contrib.auth.views import (
    get_user_model,
)
from rest_framework import status
from rest_framework.test import APITestCase

user_1 = {
    "username": 'test_username_1',
    "first_name": 'test_first_name_1',
    "last_name": 'test_last_name_1',
    "password": 'test123',
}

user_2 = {
    "username": 'test_username_2',
    "first_name": 'test_first_name_2',
    "last_name": 'test_last_name_2',
    "password": 'test123',
}


class UsersAPITests(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user(**user_1)
        get_user_model().objects.create_user(**user_2)

    def test_create_user_with_current_data(self):
        data = {
            "username": 'test_username_3',
            "first_name": 'test_first_name_3',
            "last_name": 'test_last_name_3',
            "password": 'test123',
            "password2": 'test123',
        }
        response = self.client.post('api/v1/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)

    def test_create_user_with_empty_username(self):
        data = {
            "username": '',
            "first_name": 'test_first_name',
            "last_name": 'test_last_name',
            "password": 'test123',
            "password2": 'test123',
        }
        response = self.client.post('api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['username'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_first_name(self):
        data = {
            "username": 'test_username_1',
            "first_name": '',
            "last_name": 'test_last_name_1',
            "password": 'test123',
            "password2": 'test123',
        }
        response = self.client.post('api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['first_name'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_empty_last_name(self):
        data = {
            "username": 'test_username_2',
            "first_name": 'test_first_name',
            "last_name": '',
            "password": 'test123',
            "password2": 'test123',
        }
        response = self.client.post('api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['last_name'][0].title(),
            'Это Поле Не Может Быть Пустым.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_mismatched_passwords(self):
        data = {
            "username": 'test_username_2',
            "first_name": 'test_first_name',
            "last_name": 'test_last_name',
            "password": 'test12',
            "password2": 'test123',
        }
        response = self.client.post('api/v1/users/', data, format='json')

        self.assertEqual(
            response.data['password'][0].title(),
            'Пароли Не Совпадают'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_passwords(self):
        data = {
            "username": 'test_username_2',
            "first_name": 'test_first_name',
            "last_name": 'test_last_name',
            "password": '12',
            "password2": '12',
        }
        response = self.client.post('api/v1/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.data['password'][0].title(),
            'Введённый Пароль Слишком Короткий. '
            'Он Должен Содержать Как Минимум 3 Символа.')

    def test_users_list(self):
        response = self.client.get('api/v1/users/')
        self.assertEqual(len(response.data), 2)

    def test_user_data(self):
        response = self.client.get('api/v1/users/1/')

        self.assertEqual(response.data['pk'], 1)
        self.assertEqual(response.data['username'], 'test_username_1')
        self.assertEqual(response.data['first_name'], 'test_first_name_1')
        self.assertEqual(response.data['last_name'], 'test_last_name_1')

    def test_patch_user_data(self):
        new_data = {
            "username": 'new_test_username_3',
            "first_name": 'new_test_first_name_3',
            "last_name": 'new_test_last_name_3',
            "password": 'new_test123',
            "password2": 'new_test123',
        }
        response_without_auth = self.client.patch(
            'api/v1/users/1/',
            new_data,
            format='json'
        )
        self.assertEqual(
            response_without_auth.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response_without_auth.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )
        self.client.login(
            username=user_1['username'],
            password=user_1['password']
        )
        response_with_auth = self.client.patch(
            'api/v1/users/1/',
            new_data,
            format='json'
        )
        self.assertEqual(response_with_auth.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_with_auth.data['username'],
            'new_test_username_3'
        )
        self.assertEqual(
            response_with_auth.data['first_name'],
            'new_test_first_name_3'
        )
        self.assertEqual(
            response_with_auth.data['last_name'],
            'new_test_last_name_3'
        )
        response = self.client.patch(
            'api/v1/users/2/',
            new_data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )

    def test_delete_another_user(self):
        response_without_auth = self.client.delete('api/v1/users/1/')

        self.assertEqual(
            response_without_auth.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response_without_auth.data['detail'].title(),
            'Учетные Данные Не Были Предоставлены.'
        )

    def test_delete_user(self):
        self.client.login(
            username=user_1['username'],
            password=user_1['password']
        )

        response = self.client.delete('/api/v1/users/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
