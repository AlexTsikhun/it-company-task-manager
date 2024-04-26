from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import WorkerCreationForm, TaskForm, RegistrationForm
from task_manager.models import Worker, Task, TaskType, Position


def index(request):
    res = Worker.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    closed_task_counter = Task.objects.filter(is_completed=True).count()

    context = {
        "ind": res,
        "num_visits": num_visits + 1,
        "closed_task_counter": closed_task_counter,
    }
    return render(
        request, template_name="task_manager/index.html", context=context
    )


class WorkerListView(generic.ListView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "position",
    )
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class TaskListView(generic.ListView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.all()


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
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


def task_completed(request):
    completed_tasks = Task.objects.filter(is_completed=True)
    context = {
        "completed_tasks": completed_tasks,
    }
    return render(request, "task_manager/task_completed.html", context)


def task_not_completed(request):
    not_completed_tasks = Task.objects.filter(is_completed=False)
    context = {
        "not_completed_tasks": not_completed_tasks,
    }
    return render(request, "task_manager/task_not_completed.html", context)


def complete_task(request, pk):
    task_complete = Task.objects.get(pk=pk)
    if not Task.objects.get(pk=pk).is_completed:
        task_complete.is_completed = True
    else:
        task_complete.is_completed = False
    task_complete.save()

    return HttpResponseRedirect(reverse("task_manager:task-not-completed"))


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("/accounts/login/")
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)
