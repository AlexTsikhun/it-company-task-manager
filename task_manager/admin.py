from django.contrib import admin

from task_manager.models import Task, Worker, Position

admin.site.register(Task)

admin.site.register(Worker)
admin.site.register(Position)
