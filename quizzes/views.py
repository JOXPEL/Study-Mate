from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizAttempt

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected == q.correct_answer:
                score += 1
                
        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_questions=total
        )
        return redirect('dashboard:home')

    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})