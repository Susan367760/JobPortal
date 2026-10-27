
from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cv", "cover_letter"]

        widgets = {
            "cv": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Explain why you are suitable for this role..."
                }
            ),
        }

        labels = {
            "cv": "Upload your CV (PDF or DOCX)",
            "cover_letter": "Cover Letter",
        }

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")

        if not cv:
            raise forms.ValidationError("Please upload your CV.")

        allowed_extensions = (".pdf", ".docx")
        filename = cv.name.lower()

        if not filename.endswith(allowed_extensions):
            raise forms.ValidationError(
                "Upload your CV as a PDF or DOCX file."
            )

        if cv.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Your CV must not exceed 5 MB."
            )

        return cv
