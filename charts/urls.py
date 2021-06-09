from django.urls import include, path
from charts import views


urlpatterns = [
    path('', views.ChartsView.as_view(), name='main_charts'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_charts'))
]
