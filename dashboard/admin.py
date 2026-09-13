from django.contrib import admin
from .models import StudyPlan, StudyPlanItem

class StudyPlanItemInline(admin.TabularInline):
    model = StudyPlanItem
    extra = 1

@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ['student', 'title', 'start_date', 'duration_days']
    inlines = [StudyPlanItemInline]