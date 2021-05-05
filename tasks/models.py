from django.db import models
from django.utils import timezone


class Task(models.Model):
    # user_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    deadline = models.DateTimeField()
    priority = models.IntegerField(default=0)
    last_edit = models.DateTimeField()
    description = models.TextField()

    def remained_time(self):
        return self.deadline - timezone.now()

    def last_edit_time(self):
        return timezone.now() - self.last_edit

    def __str__(self):
        return self.title
