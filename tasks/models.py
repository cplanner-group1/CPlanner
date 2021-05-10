from django.db import models
from django.utils import timezone
from accounts.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner')
    title = models.CharField(max_length=100, default='')
    group = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0)
    deadline = models.DateTimeField(default=timezone.now)
    priority = models.IntegerField(default=0)
    # last_edit = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='')

    def remained_time(self):
        remained = self.deadline - timezone.now()
        if remained.days > 0:
            return str(remained.days) + " days"
        elif remained.days == 0:
            if remained.seconds >= 3600:
                return str(remained.seconds // 3600) + " hours"
            elif remained.seconds >= 60:
                return str(remained.seconds // 60) + " minutes"
            else:
                return "few seconds"
        else:
            return "overdue"

    def __str__(self):
        return self.title
