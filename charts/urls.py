from django.urls import include, path
from charts import views


urlpatterns = [
    # CourseTracker
    path('ct/', views.UserCourseTrackerView.as_view(), name='user_courses'),
    path('ct/add/', views.UserCTAdd.as_view(), name='user_course_add'),
    path('ct/edit/', views.UserCTsEdit.as_view(), name='user_courses_edit'),
    path('ct/delete/', views.UserCTsDelete.as_view(), name='user_courses_delete'),
    path('ct/dragdrop/', views.UserCTDragDrop.as_view(), name='user_course_dragdrop'),
    path('ct/order/alpha/', views.UserCTOrderByAlphabet.as_view(), name='user_courses_order_alpha'),

    # TimeTable
    path('timetable/', views.UserTimetableView.as_view(), name='user_courses'),

    # Charts
    path('search/unif/', views.SearchChartsByUFView.as_view(), name='search_charts'),
    path('search/title/', views.SearchChartsByTView.as_view(), name='search_charts'),

    # Course
    path('course/suggest/', views.CourseAutocompleteView.as_view(), name='suggest_course'),
    path('course/suggestpre/', views.CourseAutocompleteView.as_view(), name='suggest_course'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_CTs'))
]