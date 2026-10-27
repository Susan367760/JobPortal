
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import UserProfile
from applications.models import Application
from .forms import JobForm
from .models import Job


def employer_required(view_func):
    """Allow only authenticated users with an employer profile."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            messages.error(
                request,
                "Your account does not have a profile. Please contact support."
            )
            return redirect("home")

        if profile.role != "EMPLOYER":
            messages.error(
                request,
                "Only registered employers can access this page."
            )
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


def home(request):
    jobs = Job.objects.filter(is_active=True)

    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()

    if query:
        jobs = jobs.filter(title__icontains=query)

    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, "home.html", {"jobs": jobs})


def job_detail(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True,
    )
    return render(request, "jobs/job_detail.html", {"job": job})


@employer_required
def employer_dashboard(request):
    jobs = Job.objects.filter(
        employer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "jobs/employer_dashboard.html",
        {
            "jobs": jobs,
            "total_jobs": jobs.count(),
            "active_jobs": jobs.filter(is_active=True).count(),
            "total_applications": Application.objects.filter(
                job__employer=request.user
            ).count(),
        },
    )


@employer_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user

            # Use the employer's registered company name when available.
            if request.user.profile.company_name:
                job.company = request.user.profile.company_name

            job.save()

            messages.success(request, "Your job has been posted successfully!")
            return redirect("employer_dashboard")
    else:
        initial = {}
        if request.user.profile.company_name:
            initial["company"] = request.user.profile.company_name

        form = JobForm(initial=initial)

    return render(
        request,
        "jobs/job_form.html",
        {"form": form, "page_title": "Post a Job"},
    )


@employer_required
def edit_job(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user,
    )

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            updated_job = form.save(commit=False)

            if request.user.profile.company_name:
                updated_job.company = request.user.profile.company_name

            updated_job.save()

            messages.success(request, "Your job has been updated successfully!")
            return redirect("employer_dashboard")
    else:
        form = JobForm(instance=job)

    return render(
        request,
        "jobs/job_form.html",
        {
            "form": form,
            "job": job,
            "page_title": "Edit Job",
        },
    )


@employer_required
@require_POST
def toggle_job_status(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user,
    )

    job.is_active = not job.is_active
    job.save(update_fields=["is_active"])

    if job.is_active:
        messages.success(request, "Your job is now active.")
    else:
        messages.success(request, "Your job has been deactivated.")

    return redirect("employer_dashboard")
