from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('contact/', views.contact_us, name='contact_us'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('student-life/', views.student_life, name='student_life'),
    path('leadership/', views.leadership, name='leadership'),
]
