from django.db import models
from django.utils import timezone
from datetime import datetime
from pytz import timezone as py_timezone
from accounts.models import User
from persiantools.digits import to_word


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_owner')
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default='')
    group = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0)
    tt = timezone.now() + timezone.timedelta(days=1)
    tt -= timezone.timedelta(minutes=tt.minute, seconds=tt.second)
    deadline = models.DateTimeField(default=tt)

    priority = models.IntegerField(default=1)
    description = models.TextField(default='')

    def remained_time_fa(self, tz):
        current_time = datetime.now(py_timezone(tz))
        current_time = current_time.replace(tzinfo=None)
        dead = self.deadline.replace(tzinfo=None)
        remained = dead - current_time
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
