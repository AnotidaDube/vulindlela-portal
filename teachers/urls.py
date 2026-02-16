from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', views.teacher_logout, name='teacher_logout'),
    path('add-marks/', views.add_marks, name='add_marks'),
    path('signup/', views.teacher_signup, name='teacher_signup'),

]
