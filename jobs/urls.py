
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),

    # Employer dashboard
    path(
        "employer/dashboard/",
        views.employer_dashboard,
        name="employer_dashboard",
    ),
    path(
        "employer/jobs/create/",
        views.create_job,
        name="create_job",
    ),
    path(
        "employer/jobs/<int:job_id>/edit/",
        views.edit_job,
        name="edit_job",
    ),
    path(
        "employer/jobs/<int:job_id>/toggle/",
        views.toggle_job_status,
        name="toggle_job_status",
    ),
]
