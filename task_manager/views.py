from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Worker


def index(request):
    res = Worker.objects.count()
    return render(request, template_name="base.html", context={"ind": res})


class WorkerListView(generic.ListView):
    model = Worker


class WorkerCreateView(generic.CreateView):
    model = Worker
    fields = ("position", "username", "password", "first_name", "last_name")
    success_url = reverse_lazy("worker-list")


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


