from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Student application (apply first)
    path('apply/', views.student_apply, name='apply'),
    path('success/<str:reg_no>/', views.application_success, name='application_success'),

    # Registration after approval
    path('register/', views.student_register, name='register'),

    # Login / Dashboard / Logout
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('logout/', views.student_logout, name='logout'),

    # Password reset
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    
    path('subjects/', views.view_subjects, name='view_subjects'),
    path('calendar/', views.view_calendar, name='view_calendar'),
    path('timetable/', views.view_timetable, name='view_timetable'),
    path('profile/', views.view_profile, name='view_profile'),
    #path('edit-profile/', views.edit_profile, name='edit_profile'),
    
]   
