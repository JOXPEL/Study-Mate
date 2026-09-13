from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'created_at']
    inlines = [QuestionInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'completed_at']
    list_filter = ['quiz', 'student']