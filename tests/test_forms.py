from django.test import TestCase

from task_manager.forms import WorkerCreationForm
from task_manager.models import Position


class FormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="position")

    def test_worker_creation_form_with_fields_is_valid(self):
        form_data = {
            "username": "test_u",
            "password1": "password_1",
            "password2": "password_1",
            "position": self.position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
