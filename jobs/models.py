from django.db import models
from django.conf import settings

# Create your models here.
JOB_TYPE_CHOICES = [
    ('FULL_TIME', 'Full Time'),
    ('PART_TIME', 'Part Time'),
    ('INTERNSHIP', 'Internship'),
    ('CONTRACT', 'Contract'),
]

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.IntegerField()
    deadline = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company}"
    