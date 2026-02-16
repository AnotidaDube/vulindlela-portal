from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Class(models.Model):
    # Name of the class, e.g., "Grade 10A"
    name = models.CharField(max_length=100)

    # Optional: academic year for the class, e.g., 2025
    academic_year = models.CharField(max_length=9, blank=True, null=True)  

    # Optional: section/stream within the grade, e.g., "A", "B", "C"
    section = models.CharField(max_length=5, blank=True, null=True)

    # Optional: class advisor / form teacher
    advisor = models.ForeignKey(
        'teachers.Teacher',  # assuming your Teacher model is in teachers app
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='advised_classes'
    )

    # Optional: any notes about the class
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        # Show name + section + academic year nicely
        parts = [self.name]
        if self.section:
            parts.append(f"Section {self.section}")
        if self.academic_year:
            parts.append(f"({self.academic_year})")
        return " ".join(parts)



class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='student_photos/%Y/%m/%d/')
    registration_number = models.CharField(max_length=20, unique=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"
    @staticmethod
    def get_email_field_name():
        return 'email'


# Create your models here.
