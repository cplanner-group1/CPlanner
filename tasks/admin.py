from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'group', 'priority',
                    'status', 'deadline']


admin.site.register(Task, TaskAdmin)
