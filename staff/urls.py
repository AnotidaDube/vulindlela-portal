from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('login/', views.staff_login, name='login'),
    path('logout/', views.staff_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.applications_review, name='applications'),
    path('reports/', views.admissions_report, name='reports'),
    path('gallery/upload/', views.upload_media, name='upload_media'),
    path('gallery/delete/<int:pk>/', views.delete_gallery_item, name='delete_gallery_item'),
    path('student-life/manage/', views.manage_student_life, name='manage_student_life'),
    path('student-life/delete/<int:pk>/', views.delete_student_life, name='delete_student_life'),
    path('leadership/manage/', views.manage_leadership, name='manage_leadership'),
    path('leadership/delete/<int:pk>/', views.delete_leadership, name='delete_leadership'),
]
