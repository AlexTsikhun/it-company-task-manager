from django.test import TestCase

from task_manager.models import Task, TaskType, Worker, Position


class ModelTest(TestCase):
    def setUp(self):
        username = "username"
        password = "password123"
        position = Position.objects.create(name="position")
        self.worker = Worker.objects.create_user(
            username=username, password=password, position=position
        )

    def test_task_creation(self):
        task_type = TaskType.objects.create(name="task type")

        task = Task.objects.create(
            name="name",
            description="description",
            #  datetime is not necessary
            is_completed=False,
            priority="medium",
            task_type=task_type,
        )
        task.assignees.set([self.worker])
        self.assertEqual(str(task), task.name)
