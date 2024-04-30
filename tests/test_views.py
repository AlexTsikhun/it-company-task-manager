from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from task_manager.models import Worker, Position
from tests.test_models import ModelTest

WORKER_URL = reverse("task_manager:worker-list")


class PublicWorkerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        resp = self.client.get(WORKER_URL)
        self.assertNotEquals(resp.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="password3"
        )
        self.client.force_login(self.user)

        user_dict = [
            {
                "username": "username1",
                "password": "password123",
                "position": Position.objects.create(name="position1")
            },
            {
                "username": "username2",
                "password": "password123",
                "position": Position.objects.create(name="position2")
            },
        ]
        Worker.objects.bulk_create(
            Worker(
                username=user["username"],
                password=user["password"],
                position=user["position"]
            ) for user in user_dict

        )
        self.resp = self.client.get(WORKER_URL)

    def test_retrieve_workers(self):
        self.assertEqual(self.resp.status_code, 200)

        manufacturers = Worker.objects.all()
        self.assertEqual(
            list(self.resp.context["object_list"]),
            list(manufacturers)
        )

    def test_check_template_workers(self):
        self.assertTemplateUsed(
            self.resp, "task_manager/worker_list.html"
        )
