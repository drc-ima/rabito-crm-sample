from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
# Create your models here.


ACTIVITY_TYPES = [
    ("Individual", "Individual"),
    ("Joint", "Joint"),
    ("Group", "Group")
]

class Planner(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    # activity_type = models.CharField(max_length=100, blank=True, null=True, choices=ACTIVITY_TYPES)
    # joint_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="joint_with_planner", blank=True, null=True)
    group = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group_planner", blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    activity_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    report = models.CharField(max_length=500, blank=True, null=True)
    is_rescheduled = models.BooleanField(default=False)
    reschedule_at = models.DateTimeField(blank=True, null=True)
    reschedule_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reschedule_planners", blank=True, null=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="planners", on_delete=models.DO_NOTHING)
    comments = models.ManyToManyField('Comment', related_name="comments_planner", blank=True)

    class Meta:
        db_table = 'planner'
        managed = True
        verbose_name = 'Planner'
        verbose_name_plural = 'Planners'

    def __str__(self):
        return self.description
    


class Engagement(models.Model):
    planner = models.ForeignKey(Planner, blank=True, null=True, related_name="planner_engagement", on_delete=models.DO_NOTHING)
    engaged_with = models.CharField(max_length=100, blank=True, null=True, choices=[('I', 'Individual'), ('C', 'Company')])
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="engagements", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'engagement'
        managed = True
        verbose_name = 'Engagement'
        verbose_name_plural = 'Engagements'

    def __str__(self):
        return self.full_name
    


class Comment(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="comments", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'comment'
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
    

