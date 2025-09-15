from django import forms
from .models import Student, Family, StudentNonAcademic, StudentAcademic

class StudentForm(forms.ModelForm):
    # Custom fields for 'enrolling_as' to handle multiple checkboxes
    ENROLLING_AS_CHOICES = [
        ('4 Ps Member', '4 Ps Member'),
        ('Retained', 'Retained'),
        ('Balik-aral', 'Balik-aral'),
        ('Transferee', 'Transferee'),
    ]
    # enrolling_as = forms.MultipleChoiceField(
    #     choices=ENROLLING_AS_CHOICES,
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': 'option'}),
    #     required=False,
    #     label="Please check the appropriate box if you are enrolling as one of the following:"
    # )
    enrolling_as = forms.MultipleChoiceField(
    choices=ENROLLING_AS_CHOICES,
    widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'checkbox-options',
    }),
    required=False,
    label="Please check the appropriate box if you are enrolling as one of the following:"
)


    # Custom fields for 'is_sped' and 'is_working_student' to handle radio buttons and text input
    is_sped = forms.ChoiceField(
        choices=[('1', 'YES'), ('0', 'NO')],
        widget=forms.RadioSelect,
        required=True,
        label="Does the student need a Special Education Program?"
    )
    # sped_details = forms.CharField(
    #     max_length=255,
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'fill-in-box', 'placeholder': 'Please specify...', 'disabled': 'disabled'})
    # )
    
    sped_details = forms.CharField(
    max_length=255,
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'fill-in-box',
        'placeholder': 'Please specify...',
        'disabled': 'disabled',
        'id': 'id_sped_details',

    })
)


    is_working_student = forms.ChoiceField(
        choices=[('1', 'YES'), ('0', 'NO')],
        widget=forms.RadioSelect,
        required=True,
        label="Is the student a Working Student?"
    )
    # working_details = forms.CharField(
    #     max_length=255,
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'fill-in-box', 'placeholder': 'Please specify...', 'disabled': 'disabled'})
    # )
    working_details = forms.CharField(
    max_length=255,
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'fill-in-box',
        'placeholder': 'Please specify...',
        'disabled': 'disabled',
        'id': 'id_working_details',
    })
)


    class Meta:
        model = Student
        fields = [
            'lrn', 'enrolling_as', 'is_sped', 'sped_details', 'is_working_student', 'working_details', 'photo',
            'last_name', 'first_name', 'middle_name', 'address', 'age', 'gender', 'date_of_birth',
            'place_of_birth', 'religion', 'dialect_spoken', 'ethnic_tribe', 'last_school_attended',
            'previous_grade_section', 'last_school_year'
        ]
        widgets = {
            'lrn': forms.TextInput(attrs={'placeholder': 'Enter LRN (numbers only)'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Middle Name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Present Home Address'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'gender': forms.Select(choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Non-binary', 'Non-binary'), ('Prefer not to say', 'Prefer not to say'), ('Other', 'Other')]),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'place_of_birth': forms.TextInput(attrs={'placeholder': 'Place of Birth'}),
            'religion': forms.Select(choices=[('', 'Select'), ('christianity', 'Christianity'), ('islam', 'Islam'), ('hinduism', 'Hinduism'), ('buddhism', 'Buddhism'), ('judaism', 'Judaism'), ('atheism', 'Atheism'), ('agnosticism', 'Agnosticism'), ('other', 'Other')]),
            'dialect_spoken': forms.Select(choices=[('', 'Select a dialect'), ('Chavacano', 'Chavacano'), ('Tagalog', 'Tagalog'), ('Cebuano', 'Cebuano'), ('Ilocano', 'Ilocano'), ('Tausug', 'Tausug'), ('Sama', 'Sama'), ('Other', 'Other')]),
            'ethnic_tribe': forms.Select(choices=[('', 'Select'), ('tagalog', 'Tagalog'), ('cebuano', 'Cebuano'), ('ilokano', 'Ilokano'), ('bisaya', 'Bisaya'), ('bicolano', 'Bicolano'), ('hiligaynon', 'Hiligaynon'), ('kapampangan', 'Kapampangan'), ('moros', 'Moros'), ('other', 'Other')]),
            'last_school_attended': forms.TextInput(attrs={'placeholder': 'Name of Last School Attended'}),
            'previous_grade_section': forms.TextInput(attrs={'placeholder': 'Previous Grade and Section'}),
            'last_school_year': forms.TextInput(attrs={'placeholder': 'e.g., 2023-2024'}),
            'photo': forms.FileInput(attrs={'id': 'photo-upload', 'class': 'file-input'}),
            
        }

    def clean_enrolling_as(self):
        # Convert list of choices to a comma-separated string
        return ",".join(self.cleaned_data.get('enrolling_as', []))
    
    def clean_lrn(self):
        lrn = self.cleaned_data.get('lrn')

        # Ensure it's only digits
        if not lrn.isdigit():
            raise forms.ValidationError("LRN must contain numbers only.")

        # Ensure exactly 12 digits
        if len(lrn) != 12:
            raise forms.ValidationError("LRN must be exactly 12 digits long.")

        return lrn

    def clean(self):
        cleaned_data = super().clean()
        is_sped = cleaned_data.get('is_sped')
        sped_details = cleaned_data.get('sped_details')
        is_working_student = cleaned_data.get('is_working_student')
        working_details = cleaned_data.get('working_details')

        # Convert 'is_sped' and 'is_working_student' to boolean
        cleaned_data['is_sped'] = (is_sped == '1')
        cleaned_data['is_working_student'] = (is_working_student == '1')

        if cleaned_data['is_sped'] and not sped_details:
            self.add_error('sped_details', "Please specify details for Special Education Program.")
        if not cleaned_data['is_sped']:
            cleaned_data['sped_details'] = None # Clear details if 'NO' is selected

        if cleaned_data['is_working_student'] and not working_details:
            self.add_error('working_details', "Please specify details for Working Student.")
        if not cleaned_data['is_working_student']:
            cleaned_data['working_details'] = None # Clear details if 'NO' is selected

        return cleaned_data


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        widgets = {
            'father_family_name': forms.TextInput(attrs={'placeholder': "Father's Family Name"}),
            'father_first_name': forms.TextInput(attrs={'placeholder': "Father's First Name"}),
            'father_middle_name': forms.TextInput(attrs={'placeholder': "Father's Middle Name"}),
            'father_age': forms.NumberInput(attrs={'placeholder': "Age"}),
            'father_occupation': forms.TextInput(attrs={'placeholder': "Occupation"}),
            'father_dob': forms.DateInput(attrs={'type': 'date'}),
            'father_contact_number': forms.TextInput(attrs={'placeholder': "Contact Number"}),
            'father_email': forms.EmailInput(attrs={'placeholder': "Email Address"}),

            'mother_family_name': forms.TextInput(attrs={'placeholder': "Mother's Family Maiden Name"}),
            'mother_first_name': forms.TextInput(attrs={'placeholder': "Mother's First Name"}),
            'mother_middle_name': forms.TextInput(attrs={'placeholder': "Mother's Middle Name"}),
            'mother_age': forms.NumberInput(attrs={'placeholder': "Age"}),
            'mother_occupation': forms.TextInput(attrs={'placeholder': "Occupation"}),
            'mother_dob': forms.DateInput(attrs={'type': 'date'}),
            'mother_contact_number': forms.TextInput(attrs={'placeholder': "Contact Number"}),
            'mother_email': forms.EmailInput(attrs={'placeholder': "Email Address"}),

            'guardian_family_name': forms.TextInput(attrs={'placeholder': "Guardian's Family Name"}),
            'guardian_first_name': forms.TextInput(attrs={'placeholder': "Guardian's First Name"}),
            'guardian_middle_name': forms.TextInput(attrs={'placeholder': "Guardian's Middle Name"}),
            'guardian_age': forms.NumberInput(attrs={'placeholder': "Age"}),
            'guardian_occupation': forms.TextInput(attrs={'placeholder': "Occupation"}),
            'guardian_dob': forms.DateInput(attrs={'type': 'date'}),
            'guardian_address': forms.TextInput(attrs={'placeholder': "Complete Home Address"}),
            'guardian_relationship': forms.TextInput(attrs={'placeholder': "Relationship with the student"}),
            'guardian_contact_number': forms.TextInput(attrs={'placeholder': "Contact Number"}),
            'guardian_email': forms.EmailInput(attrs={'placeholder': "Email Address"}),

            'parent_photo': forms.FileInput(attrs={'class': 'file-input'}),
            
        }


class StudentNonAcademicForm(forms.ModelForm):
    # Custom fields to handle 'other' inputs and multiple selections
    STUDY_PLACE_CHOICES = [
        ('Bedroom', 'Bedroom'),
        ('Living Room', 'Living room'),
        ('Library', 'Library'),
        ('other', 'Other:'),
    ]
    study_place = forms.MultipleChoiceField(
        choices=STUDY_PLACE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    study_place_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )

    LIVE_WITH_CHOICES = [
        ('Parents', 'Parents'),
        ('Siblings', 'Siblings'),
        ('Grandparents', 'Grandparents'),
        ('other', 'Other:'),
    ]
    live_with = forms.MultipleChoiceField(
        choices=LIVE_WITH_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    live_with_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )

    HIGHEST_EDUCATION_CHOICES = [
        ('Did not finish high school', 'Did not finish high school'),
        ('High school graduate', 'High school graduate'),
        ('College graduate', 'College graduate'),
        ('other', 'Other:'),
    ]
    highest_education = forms.ChoiceField(
        choices=HIGHEST_EDUCATION_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    highest_education_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )

    MARITAL_STATUS_CHOICES = [
        ('Married', 'Married'),
        ('Separated', 'Separated'),
        ('other', 'Other:'),
    ]
    marital_status = forms.ChoiceField(
        choices=MARITAL_STATUS_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    marital_status_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )
    
    PARENT_HELP_CHOICES = [
    ('never', 'Never'),
    ('sometimes', 'Sometimes'),
    ('often', 'Often'),
    ('always', 'Always'),
    
    ]

    parent_help = forms.ChoiceField(
        choices=PARENT_HELP_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    HOUSE_TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Shared_housing', 'Shared housing'),
        ('other', 'Other:'),
    ]
    house_type = forms.ChoiceField(
        choices=HOUSE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    house_type_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )
    
    QUIET_PLACE_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ]

    quiet_place = forms.ChoiceField(
        choices=QUIET_PLACE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    STUDY_AREA_CHOICES = [
        ('Very_quiet', 'Very quiet'),
        ('Somewhat_quiet', 'Somewhat quiet'),
        ('Noisy', 'Noisy'),
    ]

    study_area = forms.ChoiceField(
        choices=STUDY_AREA_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    TRANSPORT_MODE_CHOICES = [
        ('Walk', 'Walk'),
        ('Bicycle', 'Bicycle'),
        ('Public transport', 'Public transport (e.g., jeepney, tricycle)'),
        ('Family vehicle', 'Family vehicle'),
        ('other', 'Other:'),
    ]
    transport_mode = forms.ChoiceField(
        choices=TRANSPORT_MODE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    transport_mode_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )

    PERSONALITY_TRAITS_CHOICES = [
        ('shy', 'Shy'),
        ('outgoing', 'Outgoing'),
        ('organized', 'Organized'),
        ('creative', 'Creative'),
        ('other', 'Other:'),
    ]
    personality_traits = forms.MultipleChoiceField(
        choices=PERSONALITY_TRAITS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    personality_traits_other = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify'})
    )
    
    STUDY_HOURS_CHOICES = [
    ('less_than_1', 'Less than 1 hour'),
    ('1_2_hours', '1-2 hours'),
    ('2_3_hours', '2-3 hours'),
    ('more_than_3', 'More than 3 hours'),
    
    ]

    study_hours = forms.ChoiceField(
        choices=STUDY_HOURS_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )
    
    STUDY_WITH_CHOICES = [
    ('never', 'Never'),
    ('sometimes', 'Sometimes'),
    ('often', 'Often'),
    ('always', 'Always'),
    
    ]

    study_with = forms.ChoiceField(
        choices=STUDY_WITH_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    TRAVEL_TIME_CHOICES = [
        ('Less than 15 minutes', 'Less than 15 minutes'),
        ('15-30 minutes', '15-30 minutes'),
        ('30-60 minutes', '30-60 minutes'),
        ('More than 1 hour', 'More than 1 hour'),
    ]

    travel_time = forms.ChoiceField(
        choices=TRAVEL_TIME_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    ACCESS_RESOURCES_CHOICES = [
        ('books & materials', 'Books or study materials'),
        ('computer & tablet', 'Computer or tablet'),
        ('Internet', 'Internet'),
        ('None', 'None'),
    ]

    access_resources = forms.MultipleChoiceField(
        choices=ACCESS_RESOURCES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    COMPUTER_USE_CHOICES = [
        ('Never', 'Never'),
        ('Sometimes', 'Sometimes'),
        ('Often', 'Often'),
        ('Always', 'Always'),
    ]

    computer_use = forms.ChoiceField(
        choices=COMPUTER_USE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )
    
    CONFIDENCE_LEVEL_CHOICES = [
    ('Very_confident', 'Very confident'),
    ('Somewhat_confident', 'Somewhat confident'),
    ('Not_confident', 'Not confident'),
    
    ]
    
    confidence_level = forms.ChoiceField(
        choices=CONFIDENCE_LEVEL_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    
    


    class Meta:
        model = StudentNonAcademic
        fields = [
            'study_hours', 'study_place', 'study_with',
            'live_with', 'parent_help', 'highest_education', 'marital_status',
            'house_type', 'quiet_place', 'study_area',
            'transport_mode', 'travel_time',
            'access_resources', 'computer_use',
            'hobbies', 'personality_traits', 'confidence_level'
        ]
        widgets = {
            'study_hours': forms.RadioSelect,
            'study_with': forms.RadioSelect,
            'parent_help': forms.RadioSelect,
            'quiet_place': forms.RadioSelect,
            'study_area': forms.RadioSelect,
            'travel_time': forms.RadioSelect,
            'access_resources': forms.CheckboxSelectMultiple,
            'computer_use': forms.RadioSelect,
            'hobbies': forms.TextInput(attrs={'placeholder': 'Please specify'}),
            'confidence_level': forms.RadioSelect,
        }

    def _process_other_field(self, field_name, other_field_name, is_multiple_choice=False):
        """Helper to combine main field and 'other' field data."""
        main_data = self.cleaned_data.get(field_name)
        other_data = self.cleaned_data.get(other_field_name)
        
        if is_multiple_choice:
            if 'other' in main_data and other_data:
                main_data.remove('other')
                main_data.append(other_data)
            return ",".join(main_data)
        else:
            if main_data == 'other' and other_data:
                return other_data
            return main_data

    def clean(self):
        cleaned_data = super().clean()

        # Process fields with 'other' input
        cleaned_data['study_place'] = self._process_other_field('study_place', 'study_place_other', is_multiple_choice=True)
        cleaned_data['live_with'] = self._process_other_field('live_with', 'live_with_other', is_multiple_choice=True)
        cleaned_data['highest_education'] = self._process_other_field('highest_education', 'highest_education_other')
        cleaned_data['marital_status'] = self._process_other_field('marital_status', 'marital_status_other')
        cleaned_data['house_type'] = self._process_other_field('house_type', 'house_type_other')
        cleaned_data['transport_mode'] = self._process_other_field('transport_mode', 'transport_mode_other')
        cleaned_data['personality_traits'] = self._process_other_field('personality_traits', 'personality_traits_other', is_multiple_choice=True)
        
        # Convert list of choices to a comma-separated string for access_resources
        access_resources = cleaned_data.get('access_resources')
        if access_resources:
            cleaned_data['access_resources'] = ",".join(access_resources)
        else:
            cleaned_data['access_resources'] = "" # Ensure it's an empty string if nothing selected

        return cleaned_data


class StudentAcademicForm(forms.ModelForm):
    class Meta:
        model = StudentAcademic
        fields = [
            'lrn', 'dost_exam_result', 'report_card',
            'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
            'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh',
            'agreed_to_terms' # overall_average, is_working_student, work_type, is_pwd, disability_type will be set in view
        ]
        widgets = {
            'lrn': forms.TextInput(attrs={'placeholder': 'Enter LRN (numbers only)'}),
            'dost_exam_result': forms.Select(choices=[('', '-- Select Result --'), ('passed', 'Passed'), ('failed', 'Failed'), ('not-taken', 'Not Taken')]),
            'report_card': forms.FileInput(),
            'mathematics': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'araling_panlipunan': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'english': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'edukasyon_pagpapakatao': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'science': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'edukasyon_pangkabuhayan': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'filipino': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'mapeh': forms.NumberInput(attrs={'placeholder': 'Grade', 'min': 75, 'max': 100, 'step': 0.01}),
            'agreed_to_terms': forms.CheckboxInput(attrs={'id': 'agreeTerms'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        grades = [
            cleaned_data.get('mathematics'),
            cleaned_data.get('araling_panlipunan'),
            cleaned_data.get('english'),
            cleaned_data.get('edukasyon_pagpapakatao'),
            cleaned_data.get('science'),
            cleaned_data.get('edukasyon_pangkabuhayan'),
            cleaned_data.get('filipino'),
            cleaned_data.get('mapeh'),
        ]

        # Filter out None values in case some fields are not filled (though they are required)
        valid_grades = [g for g in grades if g is not None]

        if valid_grades:
            overall_average = sum(valid_grades) / len(valid_grades)
            cleaned_data['overall_average'] = round(overall_average, 2)
        else:
            cleaned_data['overall_average'] = 0.0 # Or raise a validation error if no grades are provided

        # Validate grades are within 75-100 range
        for field_name, grade in zip(self.fields, grades):
            if grade is not None and (grade < 75 or grade > 100):
                self.add_error(field_name, "Grade must be between 75 and 100.")

        return cleaned_data

