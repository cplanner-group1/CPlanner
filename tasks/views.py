from django.http import HttpResponse
from tasks.models import Task
from charts.models import CourseTracker
from tasks.serializers import UserTasksSerializer
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserTasksViewFa(APIView):
    serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by index
        current_time = request.GET.get('now')
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
                'remained_time': task.remained_time_fa(datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S%z')),
                'index': task.index,
                'id': task.id
            })
        return Response({'tasks_list': result}, status=status.HTTP_200_OK)


class UserTasksAdd(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        ind = Task.objects.all().filter(owner__email=request.user.email).count()
        task = Task.objects.create(
            owner=request.user,
            index=ind,
        )
        return Response({'status': "با موفقیت اضافه شد.",
                         'id': task.id,
                         'date': task.deadline.strftime("%Y-%m-%d %H:%M:%S")},
                        status=status.HTTP_200_OK)


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
                new_index = 0
                tasks = Task.objects.filter(owner__email=request.user.email).order_by('index')
                for task in tasks:
                    task.index = new_index
                    task.save()
                    new_index += 1
                return Response("حذف ناموفق بود.", status=status.HTTP_200_OK)
        # now rewrite indexes
        new_index = 0
        tasks = Task.objects.filter(owner__email=request.user.email).order_by('index')
        for task in tasks:
            task.index = new_index
            task.save()
            new_index += 1

        return Response("با موفقیت حذف شد.", status=status.HTTP_200_OK)


class UserTasksEdit(APIView):
    # serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        update_tasks = list(request.data.get('data'))
        for task in update_tasks:
            try:
                current_task = Task.objects.get(id=task['id'])
                current_task.title = task['title']
                current_task.group = task['owner']
                current_task.status = task['status']
                current_task.deadline = datetime.strptime(task['deadlineDateTime'], "%Y-%m-%d %H:%M:%S")
                current_task.priority = task['priority']
                current_task.description = task['description']
                current_task.save()
            except:
                return Response("ذخیره تغییرات ناموفق بود.", status=status.HTTP_200_OK)
        return Response("تغییرات با موفقیت ثبت شد.", status=status.HTTP_200_OK)


class UserTaskDragDrop(APIView):
    # serializer_class = UserTasksSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # task_id = request.data.get('id')
        old_index = request.data.get('old')
        new_index = request.data.get('new')

        tasks = Task.objects.filter(owner__email=request.user.email).order_by('-index')

        temp = tasks.get(index=old_index)
        temp.index = -1
        temp.save()

        if old_index < new_index:
            i = old_index + 1
            while i <= new_index:
                temp = tasks.get(index=i)
                temp.index -= 1
                temp.save()
                i += 1

        elif new_index < old_index:
            i = old_index - 1
            while i >= new_index:
                temp = tasks.get(index=i)
                temp.index += 1
                temp.save()
                i -= 1

        temp = tasks.get(index=-1)
        temp.index = new_index
        temp.save()

        return Response("جابجایی با موفقیت انجام شد.", status=status.HTTP_200_OK)


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


# Dashboard
class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    # serializer_class = CourseSerializer

    def get(self, request):
        courses = CourseTracker.objects.filter(owner__email=request.user.email, status=1)
        unit_sum = 0
        for c in courses:
            unit_sum += c.unit

        all_tasks = Task.objects.filter(owner__email=request.user.email).count()
        p1 = Task.objects.filter(owner__email=request.user.email, priority=1).count()
        p2 = Task.objects.filter(owner__email=request.user.email, priority=2).count()
        p3 = Task.objects.filter(owner__email=request.user.email, priority=3).count()
        s1 = Task.objects.filter(owner__email=request.user.email, status=0).count()
        s2 = Task.objects.filter(owner__email=request.user.email, status=1).count()
        s3 = Task.objects.filter(owner__email=request.user.email, status=2).count()
        if all_tasks == 0:
            p1_per = 0
            p2_per = 0
            p3_per = 0
            s1_per = 0
            s2_per = 0
            s3_per = 0
        else:
            p1_per = round(p1 * 1000 / all_tasks) / 10.0
            p2_per = round(p2 * 1000 / all_tasks) / 10.0
            p3_per = round(p3 * 1000 / all_tasks) / 10.0
            s1_per = round(s1 * 1000 / all_tasks) / 10.0
            s2_per = round(s2 * 1000 / all_tasks) / 10.0
            s3_per = round(s3 * 1000 / all_tasks) / 10.0
        result = {
            'passed': unit_sum,
            'priority1': p1,
            'priority2': p2,
            'priority3': p3,
            'status1': s1,
            'status2': s2,
            'status3': s3,
            'task_count': all_tasks,
            'remaining': s1 + s2,
            'p1': p1_per,
            'p2': p2_per,
            'p3': p3_per,
            's1': s1_per,
            's2': s2_per,
            's3': s3_per
        }
        return Response(result, status=status.HTTP_200_OK)


def time_check(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S\n")
    return HttpResponse(current_time)

