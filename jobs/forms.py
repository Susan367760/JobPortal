
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company",
            "location",
            "employment_type",
            "salary",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Job title",
            }),
            "company": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Company name",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Job location",
            }),
            "employment_type": forms.Select(attrs={
                "class": "form-select",
            }),
            "salary": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. KSh 50,000 per month",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Describe the job responsibilities and requirements...",
            }),
        }
