
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    EMPLOYMENT_TYPES = [
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("IN", "Internship"),
        ("RM", "Remote"),
    ]

    # The employer who owns this job.
    # Null allows existing jobs to remain in the database.
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150)

    employment_type = models.CharField(
        max_length=2,
        choices=EMPLOYMENT_TYPES,
        default="FT",
    )

    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.company}"

    class Meta:
        ordering = ["-created_at"]
