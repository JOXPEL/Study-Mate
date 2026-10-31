from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # تغيير name إلى 'home' ليتطابق مع {% url 'dashboard:home' %}
    path('', views.dashboard_home, name='home'),
]