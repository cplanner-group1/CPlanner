from django.shortcuts import render
from tasks.models import Task
from rest_framework import viewsets
from .serializers import AllTasksSerializer


class TasksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = AllTasksSerializer
