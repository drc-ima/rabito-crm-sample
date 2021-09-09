from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

STATUS = [
    (1, 'Pending'),
    (2, 'Published'),
    (3, 'Unpublished')
]

class Feedback(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="feedbacks", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = 'feedback'
        managed = True
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
    

QUESTION_TYPES = [
    ('Radio', 'Radio'),
    ('Scale', 'Scale'),
    ('Rating', 'Rating'),
    ('Fill', 'Fill'),
    ('Choice', 'Choice'),
]

class Question(models.Model):
    feedback_code = models.CharField(max_length=100, blank=True, null=True)
    text = models.CharField(max_length=300, blank=True, null=True)
    question_type = models.CharField(max_length=300, blank=True, null=True, choices=QUESTION_TYPES)
    scale_start_text = models.CharField(max_length=300, blank=True, null=True)
    scale_middle_text = models.CharField(max_length=300, blank=True, null=True)
    scale_end_text = models.CharField(max_length=300, blank=True, null=True)
    scale_count = models.IntegerField(blank=True, null=True)
    choice_answer_one = models.CharField(max_length=300, blank=True, null=True)
    choice_answer_two = models.CharField(max_length=300, blank=True, null=True)
    choice_answer_three = models.CharField(max_length=300, blank=True, null=True)
    choice_answer_four = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="quetions", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text
    
    class Meta:
        db_table = 'question'
        managed = True
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class FeedbackResponse(models.Model):
    patient_id = models.CharField(max_length=100, blank=True, null=True)
    officer_id = models.CharField(max_length=100, blank=True, null=True)
    feedback_code = models.CharField(max_length=100, blank=True, null=True)
    is_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="responses", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.feedback_code
    
    class Meta:
        db_table = 'feedback_response'
        managed = True
        verbose_name = 'Feedback Response'
        verbose_name_plural = 'Feedback Responses'


class Answer(models.Model):
    response = models.ForeignKey(FeedbackResponse, blank=True, null=True, related_name="feedback_response_answer", on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, blank=True, null=True, related_name="question_answer", on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="feedbacks", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answer'
        managed = True
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
    