from django.contrib.auth.models import AbstractUser
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = {
        "urgent": "Urgent",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
    }
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="low"
    )
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    assignees = models.ManyToManyField("Worker", related_name="tasks")


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        db_constraint=False,
        default=1
    )


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
