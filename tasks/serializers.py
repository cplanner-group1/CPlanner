from tasks.models import Task
from rest_framework import serializers


class UserTasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'group', 'status',
                  'deadline', 'priority', 'description']

