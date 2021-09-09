from itertools import chain
from apps.schedule.models import Planner
from django import template
import time
register = template.Library()


@register.simple_tag
def hourly_planners(hour, todate, user):
    hour = time.strptime(hour, '%H:%M')

    user_planners = Planner.objects.filter(start_time__hour=hour.tm_hour, activity_date=todate, created_by=user)

    group_planners = Planner.objects.filter(activity_date=todate, start_time__hour=hour.tm_hour, group__code=user.code)

    planners = list(chain(user_planners, group_planners))

    return {
        'planners': planners,
        'hour': hour.tm_hour,
    }