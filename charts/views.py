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


# semester course
class UserSCView(APIView):
    # serializer_class = UserSemesterCourseSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = []
        user_semester_course = SemesterCourse.objects.filter(owner__email=request.user.email)
        user_status = user_semester_course.exists()
        if user_status:
            for sc in user_semester_course[::-1]:
                one_semester_course = []
                exam = sc.time_exam.split('$')
                dates = sc.times.split('%')
                each_date = []
                for d in dates:
                    each_date.append(d.split('$'))
                one_semester_course.append({
                    'id': sc.id,
                    'courses': sc.course,
                    'master': sc.instructor,
                    'date': each_date,
                    'finalExam': exam,
                    'priority': sc.priority,
                    'description': sc.description,
                    'selected': sc.selected,
                })
                result.append(one_semester_course)
            return Response({'status': user_status, 'user_semester_course': result}, status=status.HTTP_200_OK)

        return Response({'status': user_status, 'user_semester_course': result}, status=status.HTTP_200_OK)

    def post(self, request):
        exam = request.data.get('finalExam')
        exam_time = "$".join(list(exam.values()))

        date = request.data.get('date')
        t = []
        for d in date:
            t.append("$".join(list(d.values())))
        times = "%".join(t)

        SemesterCourse.objects.create(
            owner=request.user,
            instructor=request.data.get('master'),
            times=times,
            time_exam=exam_time,
            course=request.data.get('courses'),
            priority=request.data.get('priority'),
            description=request.data.get('description')
        )
        return Response("با موفقیت اضافه شد.", status=status.HTTP_200_OK)


class DeleteSCView(APIView):
    # serializer_class = UserSemesterCourseSerializer
    permission_classes = (IsAuthenticated,)

    # delete one semester course
    def post(self, request):
        ids = request.data.get('id')
        try:
            SemesterCourse.objects.get(id=ids).delete()
        except:
            return Response("حذف ناموفق بود.",
                            status=status.HTTP_200_OK)
        return Response("با موفقیت حذف شد.",
                        status=status.HTTP_200_OK)

    # delete all semester courses (delete timetables as well?)
    def get(self, request):
        user_semester_course = SemesterCourse.objects.filter(owner__email=request.user.email)
        # user_timetable = Timetable.objects.get(owner__email=request.user.email)
        for course in user_semester_course:
            try:
                course.delete()
                # user_timetable.delete()
            except:
                return Response("حذف ناموفق بود.",
                                status=status.HTTP_200_OK)
        return Response("با موفقیت حذف شدند.",
                        status=status.HTTP_200_OK)


class EditSCView(APIView):
    # serializer_class = UserSemesterCourseSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):  # edit one semester course
        exam = request.data.get('finalExam')
        exam_list = [exam['startTime'], exam['endTime'],
                     exam['date'], exam['week']]
        exam_time = "$".join(exam_list)
        date = request.data.get('date')
        t = []
        for d in date:
            d_list = [d['startTime'], d['endTime'],
                      d['date'], d['week']]
            t.append("$".join(d_list))
        times = "%".join(t)
        try:
            current_course = SemesterCourse.objects.get(id=request.data.get('id'))
            current_course.course = request.data.get('courses')
            current_course.instructor = request.data.get('master')
            current_course.times = times
            current_course.time_exam = exam_time
            current_course.priority = request.data.get('priority')
            current_course.description = request.data.get('description')
            current_course.save()
            return Response("تغییرات با موفقیت ثبت شد.", status=status.HTTP_200_OK)
        except:
            return Response("ذخیره تغییرات ناموفق بود.", status=status.HTTP_200_OK)


class UserSCDragDrop(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            sc = SemesterCourse.objects.get(id=request.data.get('id'))
            if sc.selected:
                sc.selected = False
            else:
                sc.selected = True
            sc.save()
        except:
            return Response("جابجایی ناموفق بود.", status=status.HTTP_200_OK)
        return Response("جابجایی با موفقیت انجام شد.", status=status.HTTP_200_OK)


class SCAutoCompleteView(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = UserSemesterCourseSerializer

    def get(self, request):
        text = request.GET.get('text')
        chart = CourseTracker.objects.filter(owner__email=request.user.email, course__icontains=text)
        result = []
        for c in chart:
            if len(result) <= 10:
                result.append({'title': c.title})
            else:
                break
        return Response({'courses': result}, status=status.HTTP_200_OK)


class UserOverlapCheck(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        selected_courses = SemesterCourse.objects.filter(owner__email=request.user.email, selected=1)
        overlap = []
        for c in selected_courses:
            for k in selected_courses:
                if c.index != k.index and c.time_exam == k.time_exam:
                    overlapping_courses = ({
                        'course1': c.course,
                        'course2': k.course,
                        'finalExam': c.time_exam, })
                    overlap.append(overlapping_courses)
        if len(overlap) == 0:
            return Response({'status': 'بدون تداخل.',
                             'data': overlap}, status=status.HTTP_200_OK)

        return Response({'status': 'تداخل امتحانی وجود دارد.',
                        'data': overlap}, status=status.HTTP_200_OK)


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
