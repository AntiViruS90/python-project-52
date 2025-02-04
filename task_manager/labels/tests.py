from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.tests.base_test_case import BaseTestCase


class TestLabelView(BaseTestCase):
    def test_create_label(self):
        self.login_user()
        response = self.client.post(reverse_lazy('labels:create'), {
            'name': "New Label"
        })
        self.assertRedirects(response, reverse_lazy('labels:labels'))
        self.assertTrue(Label.objects.filter(name='New Label').exists())
        self.assertMessage(response, "Метка успешно создана")

    def test_label_list(self):
        self.login_user()
        label = Label.objects.create(name="New Label")

        response = self.client.get(reverse_lazy('labels:labels'))
        self.assertTemplateUsed(response, 'labels/labels.html')
        self.assertContains(response, label.name, status_code=200)
