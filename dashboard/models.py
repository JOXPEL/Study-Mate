from django.db import models
from django.conf import settings
from courses.models import Module

class StudyPlan(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_plans'
    )
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    duration_days = models.PositiveIntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.title}"

class StudyPlanItem(models.Model):
    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name='items'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='plan_items'
    )
    day_number = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number}: {self.module.title} (Plan: {self.study_plan.id})"