from tasks.models import Task
from tasks.serializers import UserTasksSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserTasksViewFa(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by index
        user_tasks = Task.objects.filter(owner__email=request.user.email).order_by('-index')
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
                'index': task.index,
                'id': task.id
            })
        return Response({'tasks_list': result}, status=status.HTTP_200_OK)

    def post(self, request):
        ind = Task.objects.all().filter(owner__email=request.user.email).count()
        Task.objects.create(
            owner=request.user,
            index=ind
        )
        return Response("New empty task added.", status=status.HTTP_200_OK)


class UserTaskDelete(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # delete all tasks given by id
        ids = request.data.get('deleted')
        counts = 0
        for ID in ids:
            try:
                Task.objects.filter(id=ID).delete()
                counts += 1
            except:
                continue

        # now rewrite indexes
        new_index = 0
        tasks = Task.objects.filter(owner__email=request.user.email).order_by('-index')
        for task in tasks:
            task.index = new_index
            task.save()
            new_index += 1

        return Response("با موفقیت حذف شد.", status=status.HTTP_200_OK)


class UserTasksEdit(APIView):
    # serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        update_tasks = request.data.get('data')
        user_tasks = Task.objects.filter(owner__email=request.user.email)
        for task in user_tasks[::-1]:
            try:
                if task.id in update_tasks:
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


class UserTaskDragDrop(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # task_id = request.data.get('id')
        old_index = request.data.get('old')
        new_index = request.data.get('new')

        tasks = Task.objects.filter(owner__email=request.user.email).order_by('-index')

        tasks[old_index].index = new_index
        tasks[old_index].save()

        if old_index < new_index:
            i = old_index + 1
            while i <= new_index:
                tasks[i].index -= 1
                tasks[i].save()
                i += 1

        elif new_index < old_index:
            i = new_index
            while i < old_index:
                tasks[i].index += 1
                tasks[i].save()
                i += 1


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


class GetTasksByDeadline(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by deadline then priority
        user_tasks = Task.objects.filter(owner__email=request.user.email).order_by('-deadline', 'priority')
        result_by_deadline = []
        for task in user_tasks[::-1]:
            result_by_deadline.append({
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
        return Response({'tasks_list': result_by_deadline}, status=status.HTTP_200_OK)
