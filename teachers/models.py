from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from students.models import Student, Class
#from results.models import Term


class Subject(models.Model):
    name = models.CharField(max_length=50)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} - {self.class_assigned}"


class Teacher(models.Model):
    national_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    subjects = models.ManyToManyField('Subject', related_name='teachers', blank=True)
    
    # Reference the single Class model from students
    classes = models.ManyToManyField(Class, related_name='teachers', blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.full_name


