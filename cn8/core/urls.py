"""URL patterns for the core app."""
from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.login_view,            name='home'),
    path('login/',                    views.login_view,             name='login'),
    path('signup/',                   views.signup_view,            name='signup'),
    path('logout/',                   views.logout_view,            name='logout'),
    path('dashboard/',                views.dashboard_view,         name='dashboard'),
    path('student/',                  views.student_dashboard_view, name='student'),
    path('teacher/',                  views.teacher_dashboard_view, name='teacher'),
    path('teacher/edit/<int:student_id>/', views.edit_student_view, name='edit_student'),
]
