from django.urls import include, path
from tasks import views


urlpatterns = [
    path('timecheck/', views.time_check),
    path('', views.UserTasksViewFa.as_view(), name='user_tasks'),
    path('add/', views.UserTasksAdd.as_view(), name='user_tasks_add'),
    path('edit/', views.UserTasksEdit.as_view(), name='user_tasks_edit'),
    path('delete/', views.UserTaskDelete.as_view(), name='user_tasks_delete'),
    path('dragdrop/', views.UserTaskDragDrop.as_view(), name='user_task_dragdrop'),
    path('ordered-by-priority/', views.GetTasksByPriority.as_view(), name='tasks_by_priority'),
    path('ordered-by-deadline/', views.GetTasksByDeadline.as_view(), name='tasks_by_deadline'),

    path('dashboard/', views.DashboardView.as_view(), name='user_dashboard'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_tasks'))
]