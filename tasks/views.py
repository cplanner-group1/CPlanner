from tasks.models import Task
from tasks.serializers import UserTasksSerializer

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserTasksViewFa(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by deadline then priority
        user_tasks = Task.objects.filter(owner__email=request.user.email).order_by('-deadline', 'priority')
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
                'remained_time': task.remained_time_fa(),
                'id': task.id
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


class UserTaskDelete(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ids = request.data.get('deleted')
        counts = 0
        for ID in ids:
            try:
                #Task.objects.filter(id=ID).delete()
                counts += 1
            except:
                continue
        return Response(str(counts) + " tasks deleted successfully.",
                        status=status.HTTP_200_OK)


class UserTaskEdit(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ids = request.data.getlist('ids')
        user_tasks = Task.objects.filter(owner__email=request.user.email)
        for task in user_tasks[::-1]:
            try:
                if task.id in ids:
                    Task.objects.filter(id=task.id).update(
                        # owner=request.user,
                        title=request.data.get('title'),
                        group=request.data.get('group'),
                        status=request.data.get('status'),
                        deadline=request.data.get('deadline'),
                        priority=request.data.get('priority'),
                        description=request.data.get('description'),
                    )
            except:
                continue

        return Response("Tasks updated successfully.", status=status.HTTP_200_OK)


class GetTasksByPriority(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by priority then deadline
        user_tasks = Task.objects.filter(owner__email=request.user.email).order_by('priority', '-deadline')
        result_by_priority = []
        for task in user_tasks[::-1]:
            result_by_priority.append({
                'user': request.user.email,
                'title': task.title,
                'group': task.group,
                'status': task.status,
                'deadline': task.deadline.strftime("%Y-%m-%d %H:%M:%S"),
                'priority': task.priority,
                'description': task.description,
                'remained_time': task.remained_time_fa(),
                'id': task.id
            })
        return Response({'tasks_list': result_by_priority}, status=status.HTTP_200_OK)
