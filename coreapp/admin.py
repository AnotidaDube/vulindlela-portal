from django.contrib import admin
from .models import SchoolUpdate

@admin.register(SchoolUpdate)
class SchoolUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_on')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'posted_on')

# Register your models here.
