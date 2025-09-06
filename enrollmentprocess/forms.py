from django import forms
from .models import StudentData, FamilyData, StudentNonAcademicData, StudentAcademicData


class StudentDataForm(forms.ModelForm):
    class Meta:
        model = StudentData
        exclude = ['family']  # family will be linked later
        
class FamilyDataForm(forms.ModelForm):
    class Meta:
        model = FamilyData
        fields = '__all__'  # all family fields including parent_photo
        
# class StudentNonAcademicDataForm(forms.ModelForm):
#     # Override multiple checkbox fields to MultipleChoiceField + "Other" text input
#     STUDY_PLACE_CHOICES = [
#         ('Bedroom', 'Bedroom'),
#         ('Living room', 'Living room'),
#         ('Library', 'Library'),
#         ('Other', 'Other'),
#     ]
#     study_place = forms.MultipleChoiceField(
#         choices=STUDY_PLACE_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )
#     study_place_other = forms.CharField(required=False)

#     LIVE_WITH_CHOICES = [
#         ('parents', 'Parents'),
#         ('siblings', 'Siblings'),
#         ('grandparents', 'Grandparents'),
#         ('Other', 'Other'),
#     ]
#     live_with = forms.MultipleChoiceField(
#         choices=LIVE_WITH_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )
#     live_with_other = forms.CharField(required=False)

#     ACCESS_RESOURCES_CHOICES = [
#         ('books_materials', 'Books or study materials'),
#         ('computer_tablet', 'Computer or tablet'),
#         ('internet', 'Internet'),
#         ('none', 'None'),
#     ]
#     access_resources = forms.MultipleChoiceField(
#         choices=ACCESS_RESOURCES_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )

#     PERSONALITY_TRAITS_CHOICES = [
#         ('shy', 'Shy'),
#         ('outgoing', 'Outgoing'),
#         ('organized', 'Organized'),
#         ('creative', 'Creative'),
#         ('Other', 'Other'),
#     ]
#     personality_traits = forms.MultipleChoiceField(
#         choices=PERSONALITY_TRAITS_CHOICES,
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )
#     personality_traits_other = forms.CharField(required=False)

#     class Meta:
#         model = StudentNonAcademicData
#         exclude = ['student']

# def clean(self):
#     cleaned_data = super().clean()

#     # Combine study_place + other
#     study_places = cleaned_data.get('study_place', [])
#     other_study_place = cleaned_data.get('study_place_other', '').strip()
#     if other_study_place:
#         study_places.append(other_study_place)
#     combined_study_place = ', '.join(study_places)
#     self.cleaned_data['study_place'] = combined_study_place

#     # Combine live_with + other
#     live_with = cleaned_data.get('live_with', [])
#     other_live_with = cleaned_data.get('live_with_other', '').strip()
#     if other_live_with:
#         live_with.append(other_live_with)
#     combined_live_with = ', '.join(live_with)
#     self.cleaned_data['live_with'] = combined_live_with

#     # Combine access_resources (no other field)
#     access_resources = cleaned_data.get('access_resources', [])
#     combined_access_resources = ', '.join(access_resources)
#     self.cleaned_data['access_resources'] = combined_access_resources

#     # Combine personality_traits + other
#     personality_traits = cleaned_data.get('personality_traits', [])
#     other_personality = cleaned_data.get('personality_traits_other', '').strip()
#     if other_personality:
#         personality_traits.append(other_personality)
#     combined_personality_traits = ', '.join(personality_traits)
#     self.cleaned_data['personality_traits'] = combined_personality_traits

#     return self.cleaned_data



class StudentNonAcademicDataForm(forms.ModelForm):
    # Choices copied from model for consistency
    STUDY_HOURS_CHOICES = StudentNonAcademicData.STUDY_HOURS_CHOICES
    STUDY_WITH_CHOICES = StudentNonAcademicData.STUDY_WITH_CHOICES
    LIVE_WITH_CHOICES = [
        ('parents', 'Parents'),
        ('siblings', 'Siblings'),
        ('grandparents', 'Grandparents'),
        ('Other', 'Other'),
    ]
    PARENT_HELP_CHOICES = StudentNonAcademicData.PARENT_HELP_CHOICES
    HIGHEST_EDUCATION_CHOICES = StudentNonAcademicData.HIGHEST_EDUCATION_CHOICES
    MARITAL_STATUS_CHOICES = StudentNonAcademicData.MARITAL_STATUS_CHOICES
    HOUSE_TYPE_CHOICES = StudentNonAcademicData.HOUSE_TYPE_CHOICES
    QUIET_PLACE_CHOICES = StudentNonAcademicData.QUIET_PLACE_CHOICES
    STUDY_AREA_CHOICES = StudentNonAcademicData.STUDY_AREA_CHOICES
    TRANSPORT_MODE_CHOICES = StudentNonAcademicData.TRANSPORT_MODE_CHOICES
    TRAVEL_TIME_CHOICES = StudentNonAcademicData.TRAVEL_TIME_CHOICES
    ACCESS_RESOURCES_CHOICES = [
        ('books_materials', 'Books or study materials'),
        ('computer_tablet', 'Computer or tablet'),
        ('internet', 'Internet'),
        ('none', 'None'),
    ]
    COMPUTER_USE_CHOICES = StudentNonAcademicData.COMPUTER_USE_CHOICES
    PERSONALITY_TRAITS_CHOICES = [
        ('shy', 'Shy'),
        ('outgoing', 'Outgoing'),
        ('organized', 'Organized'),
        ('creative', 'Creative'),
        ('Other', 'Other'),
    ]
    CONFIDENCE_LEVEL_CHOICES = StudentNonAcademicData.CONFIDENCE_LEVEL_CHOICES

    study_hours = forms.ChoiceField(choices=STUDY_HOURS_CHOICES, widget=forms.RadioSelect, required=True)
    study_place = forms.MultipleChoiceField(choices=LIVE_WITH_CHOICES[:-1], widget=forms.CheckboxSelectMultiple, required=False)
    study_place_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    study_with = forms.ChoiceField(choices=STUDY_WITH_CHOICES, widget=forms.RadioSelect, required=True)

    live_with = forms.MultipleChoiceField(choices=LIVE_WITH_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    live_with_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    parent_help = forms.ChoiceField(choices=PARENT_HELP_CHOICES, widget=forms.RadioSelect, required=True)
    highest_education = forms.ChoiceField(choices=HIGHEST_EDUCATION_CHOICES, widget=forms.RadioSelect, required=True)
    highest_education_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS_CHOICES, widget=forms.RadioSelect, required=True)
    marital_status_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))

    house_type = forms.ChoiceField(choices=HOUSE_TYPE_CHOICES, widget=forms.RadioSelect, required=True)
    house_type_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    quiet_place = forms.ChoiceField(choices=QUIET_PLACE_CHOICES, widget=forms.RadioSelect, required=True)
    study_area = forms.ChoiceField(choices=STUDY_AREA_CHOICES, widget=forms.RadioSelect, required=True)

    transport_mode = forms.ChoiceField(choices=TRANSPORT_MODE_CHOICES, widget=forms.RadioSelect, required=True)
    transport_mode_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    travel_time = forms.ChoiceField(choices=TRAVEL_TIME_CHOICES, widget=forms.RadioSelect, required=True)

    access_resources = forms.MultipleChoiceField(choices=ACCESS_RESOURCES_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    computer_use = forms.ChoiceField(choices=COMPUTER_USE_CHOICES, widget=forms.RadioSelect, required=True)

    hobbies = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))

    personality_traits = forms.MultipleChoiceField(choices=PERSONALITY_TRAITS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    personality_traits_other = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))

    confidence_level = forms.ChoiceField(choices=CONFIDENCE_LEVEL_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = StudentNonAcademicData
        exclude = ['student']

    def clean(self):
        cleaned_data = super().clean()

        # Combine multiple choice + other fields into comma-separated strings
        def combine_choices(field_name, other_field_name):
            choices = cleaned_data.get(field_name, [])
            other = cleaned_data.get(other_field_name, '').strip()
            if other:
                if isinstance(choices, str):
                    choices = [choices]
                choices.append(other)
            return ', '.join(choices) if choices else ''

        cleaned_data['study_place'] = combine_choices('study_place', 'study_place_other')
        cleaned_data['live_with'] = combine_choices('live_with', 'live_with_other')
        cleaned_data['access_resources'] = ', '.join(cleaned_data.get('access_resources', []))
        cleaned_data['personality_traits'] = combine_choices('personality_traits', 'personality_traits_other')

        # For single choice fields with 'other' option, replace value if 'other' selected
        for field, other_field in [('highest_education', 'highest_education_other'),
                                   ('marital_status', 'marital_status_other'),
                                   ('house_type', 'house_type_other'),
                                   ('transport_mode', 'transport_mode_other')]:
            if cleaned_data.get(field) == 'other':
                other_val = cleaned_data.get(other_field, '').strip()
                if other_val:
                    cleaned_data[field] = other_val

        return cleaned_data




class StudentAcademicDataForm(forms.ModelForm):
    YES_NO_CHOICES = [('yes', 'Yes'), ('no', 'No')]

    is_working_student = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'id': 'id_is_working_student'}),
        label="Is the Student a Working Student?"
    )
    work_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify work type', 'id': 'id_work_type'}),
        label="Work Type"
    )

    is_sped = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.Select(attrs={'id': 'id_is_sped'}),
        label="Is the Student in Special Education Program (SPED)?"
    )
    sped_details = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify SPED details', 'id': 'id_sped_details'}),
        label="SPED Details"
    )

    class Meta:
        model = StudentAcademicData
        fields = [
            'lrn',
            'dost_exam_result',
            # 'dost_result_file',
            'report_card',
            'mathematics',
            'araling_panlipunan',
            'english',
            'edukasyon_pagpapakatao',
            'science',
            'edukasyon_pangkabuhayan',
            'filipino',
            'mapeh',
            'overall_average',
            'is_working_student',
            'work_type',
            'is_sped',
            'sped_details',
            'agreed_to_terms',
        ]
        widgets = {
            'lrn': forms.TextInput(attrs={
                'maxlength': 12,
                'placeholder': 'Enter LRN (numbers only)',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'readonly': True,
            }),
            'dost_exam_result': forms.Select(choices=StudentAcademicData.DOST_EXAM_RESULT_CHOICES),
            # 'dost_result_file': forms.ClearableFileInput(),
            'report_card': forms.ClearableFileInput(),
            'mathematics': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'araling_panlipunan': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'english': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'edukasyon_pagpapakatao': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'science': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'edukasyon_pangkabuhayan': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'filipino': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'mapeh': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
            'overall_average': forms.NumberInput(attrs={'readonly': True, 'placeholder': 'Overall Average'}),
            'agreed_to_terms': forms.CheckboxInput(attrs={'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Calculate overall average from subject grades
        subjects = [
            'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
            'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
        ]
        total = 0
        count = 0
        for subject in subjects:
            grade = cleaned_data.get(subject)
            if grade is not None:
                total += grade
                count += 1
        if count > 0:
            cleaned_data['overall_average'] = round(total / count, 2)
        else:
            cleaned_data['overall_average'] = None

        # Clear work_type if not working student
        if cleaned_data.get('is_working_student') != 'yes':
            cleaned_data['work_type'] = ''

        # Clear sped_details if not SPED
        if cleaned_data.get('is_sped') != 'yes':
            cleaned_data['sped_details'] = ''

        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()

        # Calculate overall average from subject grades
        subjects = [
            'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
            'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
        ]
        total = 0
        count = 0
        for subject in subjects:
            grade = cleaned_data.get(subject)
            if grade is not None:
                total += grade
                count += 1
        if count > 0:
            cleaned_data['overall_average'] = round(total / count, 2)
        else:
            cleaned_data['overall_average'] = None

        # Enable work_type only if is_working_student is yes
        if cleaned_data.get('is_working_student') != 'yes':
            cleaned_data['work_type'] = None

        # Enable disability_type only if is_pwd is yes
        if cleaned_data.get('is_pwd') != 'yes':
            cleaned_data['disability_type'] = None

        return cleaned_data
