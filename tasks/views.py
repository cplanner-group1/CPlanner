from tasks.models import Task
from tasks.serializers import UserTasksSerializer

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserTasksView(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_tasks = Task.objects.filter(owner__email=request.user.email).order_by('-deadline')
        result = []
        for task in user_tasks[::-1]:
            result.append({
                'user': request.user.email,
                'title': task.title,
                'group': task.group,
                'status': task.status,
                'deadline': task.deadline.strftime("%Y-%m-%d %H:%M:%S"),
                'priority': task.priority,
                'description': task.description,
                'remained_time': task.remained_time(),
            })
        return Response({'tasks_list': result}, status=status.HTTP_200_OK)

    def post(self, request):
        Task.objects.create(
            owner=request.user,
            title=request.data.get('title'),
            group=request.data.get('group'),
            status=request.data.get('status'),
            deadline=request.data.get('deadline'),
            priority=request.data.get('priority'),
            description=request.data.get('description'),
        )
        return Response("New task successfully added.", status=status.HTTP_200_OK)

