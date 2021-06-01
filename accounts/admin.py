from django.contrib import admin
from .models import User, Student
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    actions = []

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']


admin.site.register(User, UserAdmin)


# temporary adding student
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'university', 'field', 'entry_year']


admin.site.register(Student, StudentInfoAdmin)
