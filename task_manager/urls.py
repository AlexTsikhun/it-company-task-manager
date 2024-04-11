from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from task_manager.views import index

urlpatterns = [
    path("", index, name='index'),
]
