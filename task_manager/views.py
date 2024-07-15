from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import (
    WorkerCreationForm,
    TaskForm,
    RegistrationForm,
    TaskSearchForm,
    WorkerSearchForm,
)
from task_manager.models import Worker, Task, TaskType, Position


def index(request):
    res = Worker.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    closed_task_counter = Task.objects.filter(is_completed=True).count()

    name = request.GET.get("name", "")

    last_task = Task.objects.last()

    context = {
        "ind": res,
        "num_visits": num_visits + 1,
        "closed_task_counter": closed_task_counter,
        "search_form": TaskSearchForm(initial={"name": name}),
        "last_task": last_task,
    }

    if name:
        queryset = Task.objects.all()
        task_list = queryset.filter(name__icontains=name)

        context["task_list"] = task_list
        return render(
            request, template_name="task_manager/task_list.html", context=context
        )

    return render(request, template_name="task_manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    # add search form to the page
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form_worker"] = WorkerSearchForm(initial={"username": username})
        return context

    # update data in the page after searching
    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
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
    queryset = Worker.objects.select_related("position")  # not help


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")
    queryset = Worker.objects.select_related("position")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add search form to the page"""
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        """update data in the page after searching"""
        queryset = Task.objects.all()
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    paginate_by = 8


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    queryset = TaskType.objects.all()


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task_type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task_type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 8


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    queryset = Position.objects.all()


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TaskCompletedView(LoginRequiredMixin, generic.ListView):
    # queryset = Task.objects.filter(is_completed=True)
    paginate_by = 10

    # add search form to the page
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskCompletedView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    # update data in the page after searching
    def get_queryset(self):
        queryset = Task.objects.filter(is_completed=True)
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


@login_required
def task_completed(request):
    completed_tasks = Task.objects.filter(is_completed=True)

    query_name = request.GET.get("name", "")
    if query_name:
        filtered_completed_tasks = completed_tasks.filter(name__icontains=query_name)
        context = {"filtered_completed_tasks": filtered_completed_tasks}
        return render(request, "task_manager/task_completed.html", context)

    context = {
        "completed_tasks": completed_tasks,
    }
    return render(request, "task_manager/task_completed.html", context)


@login_required()
def task_not_completed(request):
    not_completed_tasks = Task.objects.filter(is_completed=False)
    context = {
        "not_completed_tasks": not_completed_tasks,
    }
    return render(request, "task_manager/task_not_completed.html", context)


@login_required()
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
