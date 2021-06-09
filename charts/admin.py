from django.contrib import admin
from .models import Chart, Course, CourseTracker


class CourseTrackerAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'unit', 'prerequisites',
                    'status', 'grade', 'label']


admin.site.register(CourseTracker, CourseTrackerAdmin)


class ChartAdmin(admin.ModelAdmin):
    list_display = ['university', 'field']


admin.site.register(Chart, ChartAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'label', 'id']


admin.site.register(Course, CourseAdmin)

