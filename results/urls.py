from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('student/', views.student_results, name='student_results'),
    path('add-mark/', views.add_or_update_mark, name='add_or_update_mark'),
]
