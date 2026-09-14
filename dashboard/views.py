from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import QuizAttempt
from .models import StudyPlan

@login_required
def dashboard_home(request):
    attempts = QuizAttempt.objects.filter(student=request.user).order_by('-completed_at')[:5]
    plans = StudyPlan.objects.filter(student=request.user)
    context = {
        'attempts': attempts,
        'plans': plans
    }
    return render(request, 'dashboard/home.html', context)