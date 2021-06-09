from charts.models import Chart
from rest_framework import serializers


class CourseTrackerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart
        fields = ['owner', 'title', 'prerequisites', 'status',
                  'grade', 'label', 'description', 'unit']


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart
        fields = ['title', 'unit', 'label']


class ChartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chart
        fields = ['university', 'study', 'courses']
