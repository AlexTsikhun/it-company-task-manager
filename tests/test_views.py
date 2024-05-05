from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from task_manager.models import Worker, Position, Task, TaskType
from task_manager.views import TaskListView

WORKER_URL = reverse("task_manager:worker-list")
TASK_URL = reverse("task_manager:task-list")
TASKTYPE_URL = reverse("task_manager:task_type-list")
POSITION_URL = reverse("task_manager:position-list")


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


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test5",
            password="password3"
        )
        self.client.force_login(self.user)

        user_dict = []

        for i in range(1, 3):
            task_type_name = f"task type{i}"
            task_type_obj = TaskType.objects.create(name=task_type_name)

            user_dict.append({
                "name": f"name{i}",
                "description": f"description{i}",
                "is_completed": False,
                "priority": "low" if i % 2 else "medium",
                "task_type": task_type_obj,
            })

        tasks = Task.objects.bulk_create(
            Task(
                name=user["name"],
                description=user["description"],
                is_completed=user["is_completed"],
                priority=user["priority"],
                task_type=user["task_type"]
            ) for user in user_dict
        )

        position = Position.objects.create(name="position")
        [task.assignees.set([Worker.objects.create(
            username=f"username{i}",
            password=f"password{i}",
            position=position
        )]) for i, task in enumerate(tasks)]
        self.resp = self.client.get(TASK_URL)

    def test_retrieve_tasks(self):
        self.assertEqual(self.resp.status_code, 200)

        tasks = Task.objects.all()
        self.assertEqual(
            list(self.resp.context["object_list"]),
            list(tasks)
        )

    def test_check_template_tasks(self):
        self.assertTemplateUsed(
            self.resp, "task_manager/task_list.html"
        )


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test5",
            password="password3"
        )
        self.client.force_login(self.user)

        TaskType.objects.create(name="task type")
        self.resp = self.client.get(TASKTYPE_URL)

    def test_retrieve_tasks(self):
        self.assertEqual(self.resp.status_code, 200)

        tasks_type = TaskType.objects.all()
        self.assertEqual(
            list(self.resp.context["object_list"]),
            list(tasks_type)
        )

    def test_check_template_tasks(self):
        self.assertTemplateUsed(
            self.resp, "task_manager/tasktype_list.html"
        )

    def test_tasktype_url_accessible_by_name(self):
        response = self.client.get(TASKTYPE_URL)
        self.assertEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test5",
            password="password3"
        )
        self.client.force_login(self.user)

        Position.objects.create(name="position")
        self.resp = self.client.get(POSITION_URL)

    def test_retrieve_tasks(self):
        self.assertEqual(self.resp.status_code, 200)

        position = Position.objects.all()
        self.assertEqual(
            list(self.resp.context["object_list"]),
            list(position)
        )

    def test_check_template_tasks(self):
        self.assertTemplateUsed(
            self.resp, "task_manager/position_list.html"
        )

    def test_position_url_exists_at_desired_location(self):
        # checks specific path, without domain
        response = self.client.get('/positions/')
        self.assertEqual(response.status_code, 200)

    def test_position_url_accessible_by_name(self):
        # generates the URL from its name in the URL configuration
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)


class SearchTaskTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test5",
            password="password3"
        )
        self.client.force_login(self.user)

        user_dict = []

        for i in range(1, 3):
            task_type_name = f"task type{i}"
            task_type_obj = TaskType.objects.create(name=task_type_name)

            user_dict.append({
                "name": f"name{i}",
                "description": f"description{i}",
                "is_completed": False,
                "priority": "low" if i % 2 else "medium",
                "task_type": task_type_obj,
            })

        tasks = Task.objects.bulk_create(
            Task(
                name=user["name"],
                description=user["description"],
                is_completed=user["is_completed"],
                priority=user["priority"],
                task_type=user["task_type"]
            ) for user in user_dict
        )

        position = Position.objects.create(name="position")
        [task.assignees.set([Worker.objects.create(
            username=f"username{i}",
            password=f"password{i}",
            position=position
        )]) for i, task in enumerate(tasks)]

        self.factory = RequestFactory()

    def test_search_task_valid_result(self):
        test_data = "1"
        request = self.factory.get(TASK_URL, {"name": test_data})
        request.user = self.user

        view = TaskListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 1)
        self.assertQuerysetEqual(
            queryset, Task.objects.filter(name__icontains=test_data)
        )

    def test_search_car_no_result(self):
        test_data = "$$$"
        request = self.factory.get(TASK_URL, {"name": test_data})
        request.user = self.user

        view = TaskListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 0)
        self.assertQuerysetEqual(
            queryset, Task.objects.filter(name__icontains=test_data)
        )

    def test_search_car_all_result(self):
        test_data = ""
        request = self.factory.get(TASK_URL, {"name": test_data})
        request.user = self.user

        view = TaskListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        queryset = response.context_data["object_list"]
        self.assertEqual(queryset.count(), 2)
        self.assertQuerysetEqual(
            queryset,
            Task.objects.filter(name__icontains=test_data),
            ordered=False
        )
