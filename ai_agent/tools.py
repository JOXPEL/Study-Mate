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
        if not attempt.total_questions or attempt.total_questions == 0:
            continue
        percentage = (attempt.score / attempt.total_questions) * 100
        if percentage < 70: 
            module = attempt.quiz.module
            if module not in weak_modules:
                weak_modules.append(module)
                
    return weak_modules

def create_study_plan_tool(user, plan_title = "Specific study plan", duration_days=3, **kwargs):
    """
    add the week modules in the dashboard, and make a study plan
    """
    if not plan_title:
        plan_title = "Specific study plan"
    weak_modules = analyze_student_weaknesses(user)
    
    if not weak_modules:
            return {
                "status": "info",
                "message": "الطالب لا يعاني من أي نقاط ضعف في الاختبارات الحالية، أو لم يقم بحل أي كويزات بعد. لا داعي لإنشاء خطة تقوية حالياً.",
            }

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