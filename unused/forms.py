# from django import forms
# from .models import StudentData, FamilyData, StudentNonAcademicData, StudentAcademicData


# class StudentDataForm(forms.ModelForm):
#     class Meta:
#         model = StudentData
#         exclude = ['family']  # family will be linked later
        
# class FamilyDataForm(forms.ModelForm):
#     class Meta:
#         model = FamilyData
#         fields = '__all__'  # all family fields including parent_photo
        
# # class StudentNonAcademicDataForm(forms.ModelForm):
# #     # Override multiple checkbox fields to MultipleChoiceField + "Other" text input
# #     STUDY_PLACE_CHOICES = [
# #         ('Bedroom', 'Bedroom'),
# #         ('Living room', 'Living room'),
# #         ('Library', 'Library'),
# #         ('Other', 'Other'),
# #     ]
# #     study_place = forms.MultipleChoiceField(
# #         choices=STUDY_PLACE_CHOICES,
# #         widget=forms.CheckboxSelectMultiple,
# #         required=False,
# #     )
# #     study_place_other = forms.CharField(required=False)

# #     LIVE_WITH_CHOICES = [
# #         ('parents', 'Parents'),
# #         ('siblings', 'Siblings'),
# #         ('grandparents', 'Grandparents'),
# #         ('Other', 'Other'),
# #     ]
# #     live_with = forms.MultipleChoiceField(
# #         choices=LIVE_WITH_CHOICES,
# #         widget=forms.CheckboxSelectMultiple,
# #         required=False,
# #     )
# #     live_with_other = forms.CharField(required=False)

# #     ACCESS_RESOURCES_CHOICES = [
# #         ('books_materials', 'Books or study materials'),
# #         ('computer_tablet', 'Computer or tablet'),
# #         ('internet', 'Internet'),
# #         ('none', 'None'),
# #     ]
# #     access_resources = forms.MultipleChoiceField(
# #         choices=ACCESS_RESOURCES_CHOICES,
# #         widget=forms.CheckboxSelectMultiple,
# #         required=False,
# #     )

# #     PERSONALITY_TRAITS_CHOICES = [
# #         ('shy', 'Shy'),
# #         ('outgoing', 'Outgoing'),
# #         ('organized', 'Organized'),
# #         ('creative', 'Creative'),
# #         ('Other', 'Other'),
# #     ]
# #     personality_traits = forms.MultipleChoiceField(
# #         choices=PERSONALITY_TRAITS_CHOICES,
# #         widget=forms.CheckboxSelectMultiple,
# #         required=False,
# #     )
# #     personality_traits_other = forms.CharField(required=False)

# #     class Meta:
# #         model = StudentNonAcademicData
# #         exclude = ['student']

# # def clean(self):
# #     cleaned_data = super().clean()

# #     # Combine study_place + other
# #     study_places = cleaned_data.get('study_place', [])
# #     other_study_place = cleaned_data.get('study_place_other', '').strip()
# #     if other_study_place:
# #         study_places.append(other_study_place)
# #     combined_study_place = ', '.join(study_places)
# #     self.cleaned_data['study_place'] = combined_study_place

# #     # Combine live_with + other
# #     live_with = cleaned_data.get('live_with', [])
# #     other_live_with = cleaned_data.get('live_with_other', '').strip()
# #     if other_live_with:
# #         live_with.append(other_live_with)
# #     combined_live_with = ', '.join(live_with)
# #     self.cleaned_data['live_with'] = combined_live_with

# #     # Combine access_resources (no other field)
# #     access_resources = cleaned_data.get('access_resources', [])
# #     combined_access_resources = ', '.join(access_resources)
# #     self.cleaned_data['access_resources'] = combined_access_resources

# #     # Combine personality_traits + other
# #     personality_traits = cleaned_data.get('personality_traits', [])
# #     other_personality = cleaned_data.get('personality_traits_other', '').strip()
# #     if other_personality:
# #         personality_traits.append(other_personality)
# #     combined_personality_traits = ', '.join(personality_traits)
# #     self.cleaned_data['personality_traits'] = combined_personality_traits

# #     return self.cleaned_data



# class StudentNonAcademicDataForm(forms.ModelForm):
#     """
#     Form for StudentNonAcademicData model.
#     Handles checkbox selections and 'other' text inputs.
#     """
#     # The ModelForm will automatically create fields for the model.
#     # We need to explicitly define the fields that are not in the model
#     # but are used in the form, such as 'other' text inputs.
    
#     # Study habits
#     study_place_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    
#     # Family support
#     live_with_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
#     highest_education_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
#     marital_status_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    
#     # Living environment
#     house_type_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    
#     # Transportation
#     transport_mode_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    
#     # Personality traits
#     personality_traits_other = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify'}))
    
#     class Meta:
#         model = StudentNonAcademicData
#         fields = [
#             'study_hours',
#             'study_place',
#             'study_with',
#             'live_with',
#             'parent_help',
#             'highest_education',
#             'marital_status',
#             'house_type',
#             'quiet_place',
#             'study_area',
#             'transport_mode',
#             'travel_time',
#             'access_resources',
#             'computer_use',
#             'hobbies',
#             'personality_traits',
#             'confidence_level',
#         ]
        
#     def __init__(self, *args, **kwargs):
#         super(StudentNonAcademicData, self).__init__(*args, **kwargs)
#         # Use CheckboxSelectMultiple for the fields that can have multiple values
#         self.fields['study_place'].widget = forms.CheckboxSelectMultiple()
#         self.fields['live_with'].widget = forms.CheckboxSelectMultiple()
#         self.fields['access_resources'].widget = forms.CheckboxSelectMultiple()
#         self.fields['personality_traits'].widget = forms.CheckboxSelectMultiple()

#     def clean(self):
#         cleaned_data = super().clean()
        
#         # Combine the selected choices with 'other' input for each multi-select field
#         # and save it to the main field.
        
#         # Study place
#         study_place_list = cleaned_data.get('study_place', [])
#         study_place_other = cleaned_data.get('study_place_other')
#         if study_place_other:
#             study_place_list.append(study_place_other)
#         cleaned_data['study_place'] = ', '.join(study_place_list)
        
#         # Live with
#         live_with_list = cleaned_data.get('live_with', [])
#         live_with_other = cleaned_data.get('live_with_other')
#         if live_with_other:
#             live_with_list.append(live_with_other)
#         cleaned_data['live_with'] = ', '.join(live_with_list)
        
#         # Access resources
#         access_resources_list = cleaned_data.get('access_resources', [])
#         access_resources_other = cleaned_data.get('access_resources_other')
#         if access_resources_other:
#             access_resources_list.append(access_resources_other)
#         cleaned_data['access_resources'] = ', '.join(access_resources_list)
        
#         # Personality traits
#         personality_traits_list = cleaned_data.get('personality_traits', [])
#         personality_traits_other = cleaned_data.get('personality_traits_other')
#         if personality_traits_other:
#             personality_traits_list.append(personality_traits_other)
#         cleaned_data['personality_traits'] = ', '.join(personality_traits_list)
        
#         return cleaned_data





# class StudentAcademicDataForm(forms.ModelForm):
#     YES_NO_CHOICES = [('yes', 'Yes'), ('no', 'No')]

#     is_working_student = forms.ChoiceField(
#         choices=YES_NO_CHOICES,
#         widget=forms.Select(attrs={'id': 'id_is_working_student'}),
#         label="Is the Student a Working Student?"
#     )
#     work_type = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Please specify work type', 'id': 'id_work_type'}),
#         label="Work Type"
#     )

#     is_sped = forms.ChoiceField(
#         choices=YES_NO_CHOICES,
#         widget=forms.Select(attrs={'id': 'id_is_sped'}),
#         label="Is the Student in Special Education Program (SPED)?"
#     )
#     sped_details = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Please specify SPED details', 'id': 'id_sped_details'}),
#         label="SPED Details"
#     )

#     class Meta:
#         model = StudentAcademicData
#         fields = [
#             'lrn',
#             'dost_exam_result',
#             # 'dost_result_file',
#             'report_card',
#             'mathematics',
#             'araling_panlipunan',
#             'english',
#             'edukasyon_pagpapakatao',
#             'science',
#             'edukasyon_pangkabuhayan',
#             'filipino',
#             'mapeh',
#             'overall_average',
#             'is_working_student',
#             'work_type',
#             'is_sped',
#             'sped_details',
#             'agreed_to_terms',
#         ]
#         widgets = {
#             'lrn': forms.TextInput(attrs={
#                 'maxlength': 12,
#                 'placeholder': 'Enter LRN (numbers only)',
#                 'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
#                 'readonly': True,
#             }),
#             'dost_exam_result': forms.Select(choices=StudentAcademicData.DOST_EXAM_RESULT_CHOICES),
#             # 'dost_result_file': forms.ClearableFileInput(),
#             'report_card': forms.ClearableFileInput(),
#             'mathematics': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'araling_panlipunan': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'english': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'edukasyon_pagpapakatao': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'science': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'edukasyon_pangkabuhayan': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'filipino': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'mapeh': forms.NumberInput(attrs={'min': 75, 'max': 100, 'step': 0.01, 'required': True, 'placeholder': 'Grade'}),
#             'overall_average': forms.NumberInput(attrs={'readonly': True, 'placeholder': 'Overall Average'}),
#             'agreed_to_terms': forms.CheckboxInput(attrs={'required': True}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()

#         # Calculate overall average from subject grades
#         subjects = [
#             'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
#             'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
#         ]
#         total = 0
#         count = 0
#         for subject in subjects:
#             grade = cleaned_data.get(subject)
#             if grade is not None:
#                 total += grade
#                 count += 1
#         if count > 0:
#             cleaned_data['overall_average'] = round(total / count, 2)
#         else:
#             cleaned_data['overall_average'] = None

#         # Clear work_type if not working student
#         if cleaned_data.get('is_working_student') != 'yes':
#             cleaned_data['work_type'] = ''

#         # Clear sped_details if not SPED
#         if cleaned_data.get('is_sped') != 'yes':
#             cleaned_data['sped_details'] = ''

#         return cleaned_data

#     def clean(self):
#         cleaned_data = super().clean()

#         # Calculate overall average from subject grades
#         subjects = [
#             'mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao',
#             'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
#         ]
#         total = 0
#         count = 0
#         for subject in subjects:
#             grade = cleaned_data.get(subject)
#             if grade is not None:
#                 total += grade
#                 count += 1
#         if count > 0:
#             cleaned_data['overall_average'] = round(total / count, 2)
#         else:
#             cleaned_data['overall_average'] = None

#         # Enable work_type only if is_working_student is yes
#         if cleaned_data.get('is_working_student') != 'yes':
#             cleaned_data['work_type'] = None

#         # Enable disability_type only if is_pwd is yes
#         if cleaned_data.get('is_pwd') != 'yes':
#             cleaned_data['disability_type'] = None

#         return cleaned_data
