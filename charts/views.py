from charts.models import *
from charts.serializers import *

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse


# Course
class CourseAutocompleteView(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = CourseSerializer

    def get(self, request):
        text = request.data.get('textfield')
        courses = Course.objects.filter(title__icontains=text)
        result = []
        for c in courses:
            if len(result) <= 10:
                r = [{
                    'title': c.title,
                    'id': c.id
                }]
                result.append({r})
            else:
                break
        return Response({'courses': result}, status=status.HTTP_200_OK)


class GetCourseView(APIView):  # send course information when user clicks on a autocompleted course option
    permission_classes = (IsAuthenticated,)
    # serializer_class = CourseSerializer

    def get(self, request):
        course = Course.objects.get(id=request.data.get('id'))
        result = {
            'course': course.title,
            'unit': course.unit,
            'label': course.label,
            'suggestedPrerequisites': course.suggested_prerequisites,
        }

        return Response({result}, status=status.HTTP_200_OK)


class SuggestPrerequisitesView(APIView):
    # serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):  # recommends prerequisites
        title = request.GET.get('course')
        result = []
        user_courses = CourseTracker.objects.filter(owner__email=request.user.email)
        for course in user_courses:
            if course.title not in result:
                result.append(course.title)
            if len(result) == 10:
                break
        if len(result) < 10:
            all_courses = Course.objects.filter(title=title)
            for course in all_courses:  # need change
                prerequisites = course.suggested_prerequisites
                for p in prerequisites:
                    if p not in result:
                        result.append(p)
                if len(result) >= 10:
                    break
        return Response({'suggestions': result}, status=status.HTTP_200_OK)


# Charts
class AddChartToCTView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # delete old courses to overwrite them
        old_courses = CourseTracker.objects.filter(owner__email=request.user.email)
        old_courses.delete()

        # now add new courses from given chart
        ID = request.GET.get('id')
        chart = Chart.objects.get(id=ID)
        courses = chart.course_set.all().order_by('title')
        result = []
        i = 0
        for course in courses:
            # Create CourseTracker for user
            added_course = CourseTracker.objects.create(
                owner=request.user,
                index=i,
                title=course.title,
                label=course.label,
                unit=course.unit
            )
            # Get Course Tracker data to Response
            result.append({
                'title': added_course.title,
                'grade': added_course.grade,
                'unit': added_course.unit,
                'status': added_course.status,
                'label': added_course.label,
                'description': added_course.description,
                'index': added_course.index,
                'id': added_course.id
            })
            i += 1
        return Response({'data': result}, status=status.HTTP_200_OK)


class AddCTToChartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        student = Student.objects.get(user__email=user.email)
        user_courses = CourseTracker.objects.filter(owner__email=request.user.email)
        # Create Chart
        chart_title = request.GET.get('title')
        new_chart = Chart(
            owner=user,
            title=chart_title,
            university=student.university,
            field=student.field
        )
        new_chart.save()
        # Save and add Courses to chart
        for course in user_courses:
            temp = Course(
                title=course.title,
                unit=course.unit,
                label=course.label,
                suggested_prerequisites=course.prerequisites
            )
            temp.save()
            temp.charts.add(new_chart)

        return Response("چارت با موفقیت اضافه شد.", status=status.HTTP_200_OK)


class SearchChartsByUFView(APIView):
    # serializer_class = ChartSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request):  # recommends charts
        uni = request.GET.get('university')
        field = request.GET.get('field')
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
                'owner': chart.owner.first_name + " " + chart.owner.last_name,
                'university': chart.university,
                'study': chart.field,
                'date': chart.build_date,
                'courses': courses_res
            })

        return JsonResponse({'data': result}, status=status.HTTP_200_OK)


class SearchChartsByTView(APIView):
    # serializer_class = ChartSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request):  # recommends charts
        title = request.GET.get('title')
        charts = Chart.objects.filter(title__icontains=title)[:10]
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
                'owner': chart.owner.first_name + " " + chart.owner.last_name,
                'university': chart.university,
                'study': chart.field,
                'date': chart.build_date,
                'courses': courses_res
            })

        return JsonResponse({'data': result}, status=status.HTTP_200_OK)


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


class UserCTsDelete(APIView):
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


class UserCTsOrderByAlphabet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_courses = CourseTracker.objects.filter(owner__email=request.user.email).order_by('title')
        i = 0
        for course in user_courses:
            course.index = i
            course.save()
            i += 1
        result = []
        for course in user_courses:
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
