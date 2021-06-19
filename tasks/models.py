from django.db import models
import datetime
from tzlocal import get_localzone
from accounts.models import User
from persiantools.digits import to_word


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner')
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default='')
    group = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0)
    dt = datetime.datetime.now(tz=get_localzone().__str__())
    dt.replace(hour=0, minute=0, second=0)
    deadline = models.DateTimeField(default=dt)
    priority = models.IntegerField(default=1)
    description = models.TextField(default='')

    def remained_time_fa(self):
        remained = self.deadline - timezone.now()
        if remained.days > 0:
            return str(remained.days)\
                   + " روز"
        elif remained.days == 0:
            if remained.seconds >= 3600:
                return str(remained.seconds // 3600)\
                       + " ساعت"
            elif remained.seconds >= 60:
                return str(remained.seconds // 60)\
                       + " دقیقه"
            else:
                return "چند ثانیه"
        else:
            return "پایان یافته"

    def __str__(self):
        return self.title
