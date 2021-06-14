from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import User, Student
from datetime import datetime


# user courses just like tasks
class CourseTracker(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_tracker_owner')
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    # prerequisites = ArrayField(models.CharField(max_length=100))  # list of course titles
    status = models.IntegerField(default=0)
    grade = models.FloatField(default=0)
    label = models.CharField(max_length=2, default='0')
    # primary = 0, optional = 1
    description = models.TextField(max_length=300, default='')
    unit = models.IntegerField(default=3)
    # checklist = models.BooleanField(default=false)

    def __str__(self):
        return self.title


# predefined charts
class Chart(models.Model):  # created by us only? option for user to create onr?
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default=0)
    title = models.CharField(max_length=100, default='')
    used = models.IntegerField(default=0)
    # number of users using this chart
    build_date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))

    university = models.CharField(max_length=100)
    field = models.CharField(max_length=100)

    def __str__(self):
        return self.university + " - " + self.field


# courses in charts
class Course(models.Model):
    charts = models.ManyToManyField(Chart)
    title = models.CharField(max_length=100)
    unit = models.IntegerField(default=0)
    label = models.CharField(max_length=2, default='0')
    suggested_prerequisites = models.TextField(default='')


# timetable
class Timetable(models.Model):
    owner = models.OneToOneField(Student, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=100, default='')
    info = models.TextField()
