from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.tests.base_test_case import BaseTestCase


class TestStatusView(BaseTestCase):
    def test_create_status(self):
        self.login_user()
        response = self.client.post(reverse_lazy('statuses:create'), {
            'name': "New Status"
        })
        self.assertRedirects(response, reverse_lazy('statuses:statuses'))
        self.assertMessage(response, 'Статус успешно создан')

    def test_status_list(self):
        self.login_user()
        status = Status.objects.create(name="New Status")
        response = self.client.get(reverse_lazy('statuses:statuses'))
        self.assertTemplateUsed(response, 'statuses/statuses.html')
        self.assertContains(response, status.name, status_code=200)
