from django.contrib import admin
from django.contrib import admin
from .models import Teacher, Subject, Class

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_id', 'email')
    search_fields = ('full_name', 'national_id', 'email')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_assigned')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'section', 'advisor')

# Register your models here.
