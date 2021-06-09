from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import User


# user courses just like tasks
class CourseTracker(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_tracker_owner')
    title = models.CharField(max_length=100)
    prerequisites = ArrayField(models.CharField(max_length=100))  # list of course titles
    status = models.IntegerField(default=0)
    grade = models.FloatField(default=0)
    label = models.IntegerField(default=0)
    description = models.TextField(max_length=300, default='')
    unit = models.IntegerField(default=0)
    # checklist = models.BooleanField(default=false)

    def __str__(self):
        return self.title


# predefined charts
class Chart(models.Model):  # created by us only? option for user to create onr?
    university = models.CharField(max_length=100)
    field = models.CharField(max_length=100)

    def __str__(self):
        return self.university + " - " + self.field


# courses in charts
class Course(models.Model):
    charts = models.ManyToManyField(Chart)
    title = models.CharField(max_length=100)
    unit = models.IntegerField(default=0)
    label = models.CharField(max_length=100)
    # suggested_prerequisites = list()
