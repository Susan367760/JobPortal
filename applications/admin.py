
from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "applicant",
        "job",
        "status",
        "applied_at",
    )
    list_filter = ("status", "applied_at")
    search_fields = (
        "applicant__username",
        "job__title",
        "job__company",
    )
    readonly_fields = ("applied_at",)
from django.contrib import admin

# Register your models here.
