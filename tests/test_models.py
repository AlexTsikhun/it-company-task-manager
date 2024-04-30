from datetime import datetime

from django.test import TestCase

from task_manager.models import Task, TaskType, Worker, Position


class ModelTest(TestCase):
    def test_task_creation(self):
        username = "username"
        password = "password123"
        position = Position.objects.create(name="position")
        assignees = Worker.objects.create_user(
            username=username,
            password=password,
            position=position
        )

        task_type = TaskType.objects.create(name="task type")

        task = Task.objects.create(
            name="name",
            description="description",
            #  datetime is not necessary
            is_completed=False,
            priority="medium",
            task_type=task_type,
        )
        task.assignees.set([assignees])
        self.assertEqual(
            str(task),
            task.name
        )

    def test_driver_creation(self):
        driver = Driver.objects.create(
            license_number="12345678"
        )
        driver_str = (f"{driver.username} "
                      f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), driver_str)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test1111"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(license_number, driver.license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        model = "Model1"
        manufacturer = Manufacturer.objects.create(
            name="Name1", country="County1"
        )
        username = "test"
        password = "test1111"
        license_number = "12345678"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), car.model)