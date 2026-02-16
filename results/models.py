from django.db import models

# results/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from students.models import Student





class Term(models.Model):
    name = models.CharField(max_length=80)  # e.g. "Form 4 — Third Term"
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date', '-id']

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='result_marks')
    subject = models.ForeignKey('teachers.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    term = models.ForeignKey('results.Term', on_delete=models.SET_NULL, null=True, blank=True, related_name='marks')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'term')
        ordering = ['subject__name']

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.score}"

    @property
    def grade(self):
        try:
            s = float(self.score)
        except Exception:
            return ''
        if s >= 75:
            return "A"
        if s >= 65:
            return "B"
        if s >= 50:
            return "C"
        if s >= 40:
            return "D"
        return "E"


# Create your models here.
