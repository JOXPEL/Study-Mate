from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course, Module
from .forms import CourseForm, ModuleForm
from quizzes.models import QuizAttempt

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all()
    return render(request, 'courses/course_detail.html', {'course': course, 'modules': modules})

# 3. إضافة كورس جديد (خاصة بالمدرس)
@login_required
def course_create(request):
    if hasattr(request.user, 'role') and request.user.role != 'INSTRUCTOR' and not request.user.is_staff:
        return HttpResponseForbidden("غير مصرح لك بإضافة كورسات.")

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'إضافة كورس جديد'})

# 4. تعديل كورس (خاصة بمالك الكورس فقط)
@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if course.instructor != request.user and not request.user.is_staff:
        return HttpResponseForbidden("عفواً، لا يمكنك تعديل كورس لا تملكه.")

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
        
    module_form = ModuleForm()
    return render(request, 'courses/course_edit.html', {
        'form': form, 
        'module_form': module_form, 
        'course': course
    })

# 5. عرض درجات الطلاب الخاصة بمدرس الكورس
@login_required
def instructor_grades(request):
    if hasattr(request.user, 'role') and request.user.role != 'INSTRUCTOR' and not request.user.is_staff:
        return HttpResponseForbidden("غير مصرح لك برؤية هذه الصفحة.")

    attempts = QuizAttempt.objects.filter(
        quiz__module__course__instructor=request.user
    ).select_related('student', 'quiz', 'quiz__module__course').order_by('-completed_at')

    return render(request, 'courses/instructor_grades.html', {'attempts': attempts})