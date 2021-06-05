from django.urls import include, path
from tasks import views


urlpatterns = [
    path('', views.UserTasksViewFa.as_view(), name='user_charts'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_charts'))
]
