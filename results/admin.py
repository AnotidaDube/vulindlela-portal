from django.contrib import admin
from .models import Term, Mark

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'score', 'teacher', 'date_recorded')
    list_filter = ('term', 'subject')
    search_fields = ('student__full_name', 'student__registration_number', 'subject__name')

# Register your models here.
