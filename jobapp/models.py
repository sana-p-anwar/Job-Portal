from django.db import models
from django.contrib.auth.models import User


class JobDB(models.Model):

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("remote", "Remote")
    )

    job_type = models.CharField(
        max_length=100,
        choices=JOB_TYPE_CHOICES,
        default="full_time"
    )

    experience = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()

    published_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="jobs_created",
    null=True,
    blank=True
)
  



    def __str__(self):
        return self.title

class ApplicationDb(models.Model):
    
    job = models.ForeignKey(
    JobDB,
    on_delete=models.CASCADE,
    related_name="applications",
    null=True,
    blank=True
    )
    applicant = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="job_applications",
    null=True,
    blank=True
    )

 

    applicant_name = models.CharField(max_length=100)

    email = models.EmailField()

    cover_letter = models.TextField()

    resume_link = models.URLField()

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("selected", "Selected")
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="pending"
    )

    application_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.applicant_name