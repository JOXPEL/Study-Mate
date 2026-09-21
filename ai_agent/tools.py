import datetime
from quizzes.models import QuizAttempt
from dashboard.models import StudyPlan, StudyPlanItem
from courses.models import Module

def analyze_student_weaknesses(user):
    """
    define the week part in the module for the student
    """
    attempts = QuizAttempt.objects.filter(student=user)
    weak_modules = []
    #define the weekness degree percengate
    for attempt in attempts:
        percentage = (attempt.score / attempt.total_questions) * 100
        if percentage < 70: 
            module = attempt.quiz.module
            if module not in weak_modules:
                weak_modules.append(module)
                
    return weak_modules

def create_study_plan_tool(user, plan_title, duration_days=3):
    """
    add the week modules in the dashboard, and make a study plan
    """
    weak_modules = analyze_student_weaknesses(user)
    
    if not weak_modules:
        #if the student is perfect we will revise on these modules
        weak_modules = list(Module.objects.all()[:duration_days])

    #make the studyplane and store it in the database
    plan = StudyPlan.objects.create(
        student=user,
        title=plan_title,
        start_date=datetime.date.today(),
        duration_days=duration_days
    )

    #add the lessons in the study plan item for each day
    created_items = []
    #what does enumerate do?
    #...!
    for index, module in enumerate(weak_modules[:duration_days]):
        day_number = index + 1
        item = StudyPlanItem.objects.create(
            study_plan=plan,
            module=module,
            day_number=day_number,
            completed=False
        )
        created_items.append(f"Day {day_number}: {module.title}")

    return {
        "status": "success",
        "plan_id": plan.id,
        "plan_title": plan.title,
        "assigned_modules": created_items
    }