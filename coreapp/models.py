from django.db import models

class SchoolUpdate(models.Model):
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('academics', 'Academics'),
        ('notices', 'Notices'),
    ]

    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
