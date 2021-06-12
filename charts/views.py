from charts.models import *
from charts.serializer import *

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Charts
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


class AddChartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self):
        pass


class SearchChartsView(APIView):
    # serializer_class = ChartSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):  # recommends charts
        uni = request.data.get('university')
        field = request.data.get('field')
        charts = Chart.objects.filter(university__icontains=uni, field__icontains=field)[:10]
        # order by what so we return best results?
        result = []
        for chart in charts:
            courses = chart.course_set.all()
            courses_res = []
            for course in courses:
                courses_res.append(course.title)

            result.append({
                'id': chart.id,
                'title': chart.title,
                'used': chart.used,
                'owner': chart.owner,
                'university': chart.university,
                'study': chart.field,
                'date': chart.build_date,
                'courses': courses_res
            })

        return Response({'courses': result}, status=status.HTTP_200_OK)


# CourseTracker
class UserCourseTrackerView(APIView):
    serializer_class = CourseTrackerSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # ordered by index
        user_courses = CourseTracker.objects.filter(owner__email=request.user.email).order_by('-index')
        result = []
        for course in user_courses[::-1]:
            result.append({
                'title': course.title,
                'grade': course.grade,
                'unit': course.unit,
                'status': course.status,
                'label': course.label,
                'description': course.description,
                'index': course.index,
                'id': course.id
            })
        return Response({'data': result}, status=status.HTTP_200_OK)


class UserCTAdd(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        ind = CourseTracker.objects.all().filter(owner__email=request.user.email).count()
        course = CourseTracker.objects.create(
            owner=request.user,
            index=ind,
        )
        return Response({'id': course.id}, status=status.HTTP_200_OK)


class UserCTDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ids = request.data.get('deleted')
        counts = 0
        for ID in ids:
            try:
                CourseTracker.objects.filter(id=ID).delete()
                counts += 1
            except:
               continue

        # now rewrite indexes
        new_index = 0
        courses = CourseTracker.objects.filter(owner__email=request.user.email).order_by('index')
        for course in courses:
            course.index = new_index
            course.save()
            new_index += 1

        return Response("با موفقیت حذف شد.", status=status.HTTP_200_OK)


class UserCTsEdit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        update_courses = list(request.data.get('data'))
        for course in update_courses:
             # try:
                current_course = CourseTracker.objects.get(id=course['course']['id'])
                current_course.title = course['course']['title']
                current_course.grade = course['grade']
                current_course.status = course['status']
                current_course.label = course['label']
                current_course.unit = course['unit']
                current_course.description = course['description']
                current_course.save()
             # except:
                 #return Response("ذخیره تغییرات ناموفق بود.", status=status.HTTP_200_OK)
        return Response("تغییرات با موفقیت ثبت شد.", status=status.HTTP_200_OK)


class UserCTDragDrop(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # task_id = request.data.get('id')
        old_index = request.data.get('old')
        new_index = request.data.get('new')

        courses = CourseTracker.objects.filter(owner__email=request.user.email).order_by('-index')

        temp = courses.get(index=old_index)
        temp.index = -1
        temp.save()

        if old_index < new_index:
            i = old_index + 1
            while i <= new_index:
                temp = courses.get(index=i)
                temp.index -= 1
                temp.save()
                i += 1

        elif new_index < old_index:
            i = old_index - 1
            while i >= new_index:
                temp = courses.get(index=i)
                temp.index += 1
                temp.save()
                i -= 1

        temp = courses.get(index=-1)
        temp.index = new_index
        temp.save()

        return Response("جابجایی با موفقیت انجام شد.", status=status.HTTP_200_OK)


# time table
class UserTimetableView(APIView):
    # serializer_class = UserTimetableSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # get one specific timetable
        user_timetable = Timetable.objects.get(owner__user__email=request.user.email)
        result = {
            'info': user_timetable.info,
        }
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        # add timetable for user
        item = request.get('item')

        Timetable.objects.create(
            owner=request.user,

            info=request.data.get('info'),
        )
        return Response("New timetable successfully saved.", status=status.HTTP_200_OK)
