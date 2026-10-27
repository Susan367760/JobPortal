
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile
from jobs.models import Job
from .forms import ApplicationForm
from .models import Application


@login_required
@require_http_methods(["GET", "POST"])
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    # Only job seekers may apply.
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, "Please complete your profile before applying.")
        return redirect("home")

    if profile.role != "JOB_SEEKER":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("job_detail", job_id=job.id)

    # Prevent duplicate applications.
    if Application.objects.filter(applicant=request.user, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect("my_applications")

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                with transaction.atomic():
                    application = form.save(commit=False)
                    application.applicant = request.user
                    application.job = job
                    application.save()

                messages.success(request, "Your application was submitted successfully!")
                return redirect("my_applications")

            except IntegrityError:
                messages.info(request, "You have already applied for this job.")
                return redirect("my_applications")
    else:
        form = ApplicationForm()

    return render(
        request,
        "applications/apply.html",
        {"form": form, "job": job},
    )


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related("job")

    return render(
        request,
        "applications/my_applications.html",
        {"applications": applications},
    )
from django.shortcuts import render

# Create your views here.
