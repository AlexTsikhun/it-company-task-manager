from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Worker, Task, TaskType, Position


def index(request):
    res = Worker.objects.count()
    return render(request, template_name="base.html", context={"ind": res})


class WorkerListView(generic.ListView):
    model = Worker


class WorkerCreateView(generic.CreateView):
    model = Worker
    fields = ("position", "username", "password", "first_name", "last_name")
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = "__all__"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(generic.ListView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.all()


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(generic.ListView):
    model = TaskType


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    queryset = TaskType.objects.all()


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task_type-list")


class PositionListView(generic.ListView):
    model = Position


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDetailView(generic.DetailView):
    model = Position
    queryset = Position.objects.all()


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
