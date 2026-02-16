from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------------
# StaffProfile model
# -------------------------
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True, null=True)  # e.g., Teacher, Admin
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role or 'Staff'}"

# -------------------------
# StudentApplication model
# -------------------------
class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_number = models.CharField(max_length=50, unique=True)
    applied_class = models.ForeignKey('students.Class', on_delete=models.SET_NULL, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    previous_grade_level = models.CharField(max_length=50)
    previous_grade_results = models.TextField()
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} ({self.registration_number})"

# -------------------------
# Signals for StaffProfile
# -------------------------
@receiver(post_save, sender=User)
def create_or_update_staff_profile(sender, instance, created, **kwargs):
    """
    Automatically create a StaffProfile when a User is created,
    and save the profile if it already exists.
    """
    if created:
        StaffProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'staffprofile'):
            instance.staffprofile.save()

class GalleryItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    video = models.FileField(upload_to='gallery/videos/', blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StudentLifeItem(models.Model):
    CATEGORY_CHOICES = (
        ('sport', 'Sports Team'),
        ('club', 'Club or Society'),
        ('boarding', 'Boarding & Facilities'),
    )

    title = models.CharField(max_length=100)  # e.g., "Soccer Team" or "Debate Club"
    description = models.TextField()          # e.g., "Reigning provincial champions..."
    image = models.ImageField(upload_to='student_life/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    passport_photo = models.ImageField(upload_to='staff_passports/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class LeadershipProfile(models.Model):
    CATEGORY_CHOICES = (
        ('admin', 'Administration (Principal/Deputy)'),
        ('teacher', 'Teaching Staff'),
        ('support', 'Support Staff'),
        ('prefect', 'School Prefect'),
    )

    name = models.CharField(max_length=100)       # e.g., Mr. N. Mangena
    position = models.CharField(max_length=100)   # e.g., Headmaster
    bio = models.TextField(blank=True, null=True) # Short bio
    image = models.ImageField(upload_to='staff_profiles/')
    passport_photo = models.ImageField(upload_to='staff_passports/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)        # 1 for Principal, 2 for Deputy...

    def __str__(self):
        return f"{self.name} - {self.position}"