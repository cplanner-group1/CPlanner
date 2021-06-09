from charts.models import *
from charts.serializer import *

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ChartsView(APIView):
    serializer_class = ChartSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):  # sends a chart and creates coursetrackers per each of it's courses
        uni = request.data.get('university')
        field = request.data.get('field')
        chart = Chart.objects.get(university=uni, field=field)
        courses = chart.course_set.all()
        result = []
        for course in courses:
            result.append({
                'title': course.title,
                'unit': course.unit,
                'label': course.label
            })
        return Response({'courses': result}, status=status.HTTP_200_OK)


class UserCourseTrackerView(APIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_all(self, request):  # sends all of users coursetrackers
        user_coursetrackers = CourseTracker.objects.filter(owner__email=request.user.email)
        result = []
        for ct in user_coursetrackers[::-1]:
            result.append({
                'user': request.user.email,
                'id': ct.id,
                'course': ct.course,
                'prerequisites': ct.prerequisites,
                'status': ct.status,
                'grade': ct.grade,
                'label': ct.label,
                'description': ct.description,
                'unit': ct.unit
            })
        return Response({'ct_list': result}, status=status.HTTP_200_OK)

    def get(self, request):  # sends one specific coursetrackers
        ids = request.data.getlist('ids')
        ct = CourseTracker.objects.filter(id=ids)
        result = [{
                'user': request.user.email,
                'id': ct.id,
                'course': ct.course,
                'prerequisites': ct.prerequisites,
                'status': ct.status,
                'grade': ct.grade,
                'label': ct.label,
                'description': ct.description,
                'unit': ct.unit
                }]
        return Response({'coursetracker': result}, status=status.HTTP_200_OK)

    def post(self, request):  # adds one coursetracker for user (if it does not cause loop in prerequisites.)
        user_coursetrackers = CourseTracker.objects.filter(owner__email=request.user.email)
        loop = 0
        queue = [request.data.get('course')]
        visited = [request.data.get('course')]
        while queue:
            s = queue.pop(0)
            for j in s.prerequisites:
                if j not in visited:
                    visited.append(j)
                    queue.append(j)
                else:
                    loop = j.title
        if loop == 0:
            CourseTracker.objects.append(
                user_id=request.user.email,
                id=request.data.get('id'),
                course=request.data.get('course'),
                prerequisites=request.data.get('prerequisites'),
                status=request.data.get('status'),
                grade=request.data.get('grade'),
                label=request.data.get('label'),
                description=request.data.get('description'),
                unit=request.data.get('unit')
            )
            return Response("New Course successfully added.", status=status.HTTP_200_OK)
        else:
            return Response("could not add course because it causes a Loop in prerequisites.", status=status.HTTP_200_OK)

    def delete(self, request):  # delete removes the coursetracker created for user
        ids = request.data.getlist('ids')
        try:
            CourseTracker.objects.filter(id=ids).delete()
        except:
            return Response("Could not delete Course.",
                            status=status.HTTP_200_OK)
        return Response("Course deleted successfully.",
                        status=status.HTTP_200_OK)

    def delete_all(self, request):  # delete all of users course
        user_ct = CourseTracker.objects.filter(owner__email=request.user.email)
        try:
            user_ct.all().delete()
        except:
            return Response("Could not delete course.",
                            status=status.HTTP_200_OK)
        return Response("course deleted successfully.",
                        status=status.HTTP_200_OK)

