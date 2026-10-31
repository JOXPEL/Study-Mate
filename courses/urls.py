from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('instructor/grades/', views.instructor_grades, name='instructor_grades'),
]