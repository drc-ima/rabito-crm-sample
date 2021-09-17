from apps.schedule.models import Comment, Engagement, Planner
from django.contrib import admin

# Register your models here.

admin.site.register(Planner)
admin.site.register(Comment)
admin.site.register(Engagement)