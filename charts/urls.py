from django.urls import include, path
from charts import views


urlpatterns = [
    path('', views.UserCourseTrackerView.as_view(), name='user_courses'),
    path('add/', views.UserCTAdd.as_view(), name='user_courses_add'),
    path('edit/', views.UserCTsEdit.as_view(), name='user_courses_edit'),
    path('delete/', views.UserCTDelete.as_view(), name='user_courses_delete'),
    path('dragdrop/', views.UserCTDragDrop.as_view(), name='user_course_dragdrop'),
    # timetable
    path('timetable/', views.UserTimetableView.as_view(), name='user_courses'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_CTs'))
]