
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("REVIEWING", "Under Review"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
        ("ACCEPTED", "Accepted"),
    ]

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    cv = models.FileField(upload_to="cvs/")
    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "job"],
                name="unique_application_per_job"
            )
        ]

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
from django.db import models

# Create your models here.
