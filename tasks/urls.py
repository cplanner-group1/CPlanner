from django.urls import include, path
from tasks import views


urlpatterns = [
    path('', views.UserTasksViewFa.as_view(), name='user_tasks'),
    path('ordered-by-priority/', views.GetTasksByPriority.as_view(), name='tasks_by_priority'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_tasks'))
]