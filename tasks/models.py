from django.db import models
from django.utils import timezone


class Task(models.Model):
    # owner = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    group = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0)
    deadline = models.DateTimeField(default=timezone.now)
    priority = models.IntegerField(default=0)
    last_edit = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='')

    def remained_time(self):
        return self.deadline - timezone.now()

    def last_edit_time(self):
        return timezone.now() - self.last_edit

    def __str__(self):
        return self.title
