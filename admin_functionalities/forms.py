from django import forms
from .models import StudentRequirements

class StudentRequirementsForm(forms.ModelForm):
    class Meta:
        model = StudentRequirements
        fields = [
            'birth_certificate',
            'good_moral',
            'interview_done',
            'reading_assessment_done',
        ]
        widgets = {
            'birth_certificate': forms.CheckboxInput(),
            'good_moral': forms.CheckboxInput(),
            'interview_done': forms.CheckboxInput(),
            'reading_assessment_done': forms.CheckboxInput(),
        }
