from django.shortcuts import render
from tasks.models import Task
from rest_framework import viewsets
from tasks.serializers import AllTasksSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = AllTasksSerializer
