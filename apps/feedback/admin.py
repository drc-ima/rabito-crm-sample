from apps.feedback.models import Answer, Feedback, FeedbackResponse, Question
from django.contrib import admin

# Register your models here.

admin.site.register(Feedback)
admin.site.register(Question)
admin.site.register(FeedbackResponse)
admin.site.register(Answer)