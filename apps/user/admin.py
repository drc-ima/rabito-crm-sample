from django.contrib.auth.models import Permission
from apps.user.models import Branch, Role, User
from django.contrib import admin

# Register your models here.
admin.site.register(Role)
admin.site.register(Branch)
admin.site.register(Permission)
admin.site.register(User)