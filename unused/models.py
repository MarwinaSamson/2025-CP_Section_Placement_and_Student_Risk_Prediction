# from django.db import models
# from django.core.exceptions import ValidationError



# class FamilyData(models.Model):
#     # Father's Information
#     father_family_name = models.CharField(max_length=100)
#     father_first_name = models.CharField(max_length=100)
#     father_middle_name = models.CharField(max_length=100, blank=True, null=True)
#     father_age = models.PositiveIntegerField()
#     father_occupation = models.CharField(max_length=100)
#     father_dob = models.DateField()
#     father_contact_number = models.CharField(max_length=20)
#     father_email = models.EmailField(blank=True, null=True)

#     # Mother's Information
#     mother_family_name = models.CharField(max_length=100)
#     mother_first_name = models.CharField(max_length=100)
#     mother_middle_name = models.CharField(max_length=100, blank=True, null=True)
#     mother_age = models.PositiveIntegerField()
#     mother_occupation = models.CharField(max_length=100)
#     mother_dob = models.DateField()
#     mother_contact_number = models.CharField(max_length=20)
#     mother_email = models.EmailField(blank=True, null=True)

#     # Guardian Information (if not staying with parents)
#     guardian_family_name = models.CharField(max_length=100)
#     guardian_first_name = models.CharField(max_length=100)
#     guardian_middle_name = models.CharField(max_length=100, blank=True, null=True)
#     guardian_age = models.PositiveIntegerField()
#     guardian_occupation = models.CharField(max_length=100)
#     guardian_dob = models.DateField()
#     guardian_address = models.CharField(max_length=255)
#     guardian_relationship = models.CharField(max_length=100)
#     guardian_contact_number = models.CharField(max_length=20)
#     guardian_email = models.EmailField(blank=True, null=True)

#     # Parent photo (optional)
#     parent_photo = models.ImageField(upload_to='parent_photos/', blank=True, null=True)

#     def __str__(self):
#         return f"Family of {self.father_family_name} / {self.mother_family_name}"


# class StudentData(models.Model):
#     # LRN Number: 12-digit numeric string
#     lrn = models.CharField(max_length=12, unique=True)

#     # Checkboxes: Boolean fields, default False
#     is_4ps_member = models.BooleanField(default=False)
#     is_retained = models.BooleanField(default=False)
#     is_balik_aral = models.BooleanField(default=False)
#     is_transferee = models.BooleanField(default=False)

#     # Special Education Program
#     is_sped = models.BooleanField()
#     sped_details = models.CharField(max_length=255, blank=True, null=True)

#     # Working Student
#     is_working_student = models.BooleanField()
#     working_details = models.CharField(max_length=255, blank=True, null=True)

#     # Photo upload
#     photo = models.ImageField(upload_to='student_photos/')

#     # Student's Name
#     last_name = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     middle_name = models.CharField(max_length=100, blank=True, null=True)

#     # Address
#     address = models.CharField(max_length=255)

#     # Age
#     age = models.PositiveIntegerField()

#     # Gender choices
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Non-binary', 'Non-binary'),
#         ('Prefer not to say', 'Prefer not to say'),
#         ('Other', 'Other'),
#     ]
#     gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

#     # Date of Birth
#     date_of_birth = models.DateField()

#     # Place of Birth
#     place_of_birth = models.CharField(max_length=255)

#     # Religion choices
#     RELIGION_CHOICES = [
#         ('christianity', 'Christianity'),
#         ('islam', 'Islam'),
#         ('hinduism', 'Hinduism'),
#         ('buddhism', 'Buddhism'),
#         ('judaism', 'Judaism'),
#         ('atheism', 'Atheism'),
#         ('agnosticism', 'Agnosticism'),
#         ('other', 'Other'),
#     ]
#     religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)

#     # Dialect Spoken choices
#     DIALECT_CHOICES = [
#         ('Chavacano', 'Chavacano'),
#         ('Tagalog', 'Tagalog'),
#         ('Cebuano', 'Cebuano'),
#         ('Ilocano', 'Ilocano'),
#         ('Tausug', 'Tausug'),
#         ('Sama', 'Sama'),
#         ('Other', 'Other'),
#     ]
#     dialect_spoken = models.CharField(max_length=20, choices=DIALECT_CHOICES)

#     # Ethnic Tribe choices
#     ETHNIC_TRIBE_CHOICES = [
#         ('tagalog', 'Tagalog'),
#         ('cebuano', 'Cebuano'),
#         ('ilokano', 'Ilokano'),
#         ('bisaya', 'Bisaya'),
#         ('bicolano', 'Bicolano'),
#         ('hiligaynon', 'Hiligaynon'),
#         ('kapampangan', 'Kapampangan'),
#         ('moros', 'Moros'),
#         ('other', 'Other'),
#     ]
#     ethnic_tribe = models.CharField(max_length=20, choices=ETHNIC_TRIBE_CHOICES)

#     # Last school attended
#     last_school_attended = models.CharField(max_length=255)

#     # Previous grade and section
#     previous_grade_section = models.CharField(max_length=100)

#     # School year last attended
#     last_school_year = models.CharField(max_length=20)
    
#     family = models.ForeignKey(FamilyData, on_delete=models.PROTECT, related_name='students', null=True, blank=True)

#     def __str__(self):
#         return f"{self.last_name}, {self.first_name} ({self.lrn})"



# # class StudentNonAcademicData(models.Model):
# #     student = models.OneToOneField('StudentData', on_delete=models.CASCADE, related_name='non_academic_data')

# #     # STUDY HABITS
# #     STUDY_HOURS_CHOICES = [
# #         ('less_than_1', 'Less than 1 hour'),
# #         ('1_2_hours', '1-2 hours'),
# #         ('2_3_hours', '2-3 hours'),
# #         ('more_than_3', 'More than 3 hours'),
# #     ]
# #     study_hours = models.CharField(max_length=20, choices=STUDY_HOURS_CHOICES)

# #     # study_place: multiple checkboxes, store as comma-separated string
# #     # Possible values: 'Bedroom', 'Living room', 'Library', 'Other'
# #     study_place = models.CharField(max_length=255, help_text="Comma-separated study places")
# #     study_place_other = models.CharField(max_length=255, blank=True, null=True)

# #     STUDY_WITH_CHOICES = [
# #         ('never', 'Never'),
# #         ('sometimes', 'Sometimes'),
# #         ('often', 'Often'),
# #         ('always', 'Always'),
# #     ]
# #     study_with = models.CharField(max_length=20, choices=STUDY_WITH_CHOICES)

# #     # FAMILY SUPPORT
# #     # live_with: multiple checkboxes, comma-separated string
# #     live_with = models.CharField(max_length=255, help_text="Comma-separated live with options")
# #     live_with_other = models.CharField(max_length=255, blank=True, null=True)

# #     PARENT_HELP_CHOICES = [
# #         ('never', 'Never'),
# #         ('sometimes', 'Sometimes'),
# #         ('often', 'Often'),
# #         ('always', 'Always'),
# #     ]
# #     parent_help = models.CharField(max_length=20, choices=PARENT_HELP_CHOICES)

# #     HIGHEST_EDUCATION_CHOICES = [
# #         ('did_not_finish_hs', 'Did not finish high school'),
# #         ('high_school_graduate', 'High school graduate'),
# #         ('college_graduate', 'College graduate'),
# #         ('other', 'Other'),
# #     ]
# #     highest_education = models.CharField(max_length=30, choices=HIGHEST_EDUCATION_CHOICES)
# #     highest_education_other = models.CharField(max_length=255, blank=True, null=True)

# #     MARITAL_STATUS_CHOICES = [
# #         ('married', 'Married'),
# #         ('separated', 'Separated'),
# #         ('other', 'Other'),
# #     ]
# #     marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
# #     marital_status_other = models.CharField(max_length=255, blank=True, null=True)

# #     # LIVING ENVIRONMENT
# #     HOUSE_TYPE_CHOICES = [
# #         ('apartment', 'Apartment'),
# #         ('house', 'House'),
# #         ('shared_housing', 'Shared housing'),
# #         ('other', 'Other'),
# #     ]
# #     house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)
# #     house_type_other = models.CharField(max_length=255, blank=True, null=True)

# #     QUIET_PLACE_CHOICES = [
# #         ('yes', 'Yes'),
# #         ('no', 'No'),
# #     ]
# #     quiet_place = models.CharField(max_length=3, choices=QUIET_PLACE_CHOICES)

# #     STUDY_AREA_CHOICES = [
# #         ('very_quiet', 'Very quiet'),
# #         ('somewhat_quiet', 'Somewhat quiet'),
# #         ('noisy', 'Noisy'),
# #     ]
# #     study_area = models.CharField(max_length=20, choices=STUDY_AREA_CHOICES)

# #     # TRANSPORTATION
# #     TRANSPORT_MODE_CHOICES = [
# #         ('walk', 'Walk'),
# #         ('bicycle', 'Bicycle'),
# #         ('public_transport', 'Public transport'),
# #         ('family_vehicle', 'Family vehicle'),
# #         ('other', 'Other'),
# #     ]
# #     transport_mode = models.CharField(max_length=20, choices=TRANSPORT_MODE_CHOICES)
# #     transport_mode_other = models.CharField(max_length=255, blank=True, null=True)

# #     TRAVEL_TIME_CHOICES = [
# #         ('less_than_15', 'Less than 15 minutes'),
# #         ('15_30_minutes', '15-30 minutes'),
# #         ('30_60_minutes', '30-60 minutes'),
# #         ('more_than_1_hour', 'More than 1 hour'),
# #     ]
# #     travel_time = models.CharField(max_length=20, choices=TRAVEL_TIME_CHOICES)

# #     # ACCESS TO LEARNING RESOURCES
# #     # access_resources: multiple checkboxes, comma-separated string
# #     access_resources = models.CharField(max_length=255, help_text="Comma-separated access resources")

# #     COMPUTER_USE_CHOICES = [
# #         ('never', 'Never'),
# #         ('sometimes', 'Sometimes'),
# #         ('often', 'Often'),
# #         ('always', 'Always'),
# #     ]
# #     computer_use = models.CharField(max_length=20, choices=COMPUTER_USE_CHOICES)

# #     # PERSONALITY TRAITS AND INTERESTS
# #     hobbies = models.CharField(max_length=255)

# #     # personality_traits: multiple checkboxes, comma-separated string
# #     personality_traits = models.CharField(max_length=255, help_text="Comma-separated personality traits")
# #     personality_traits_other = models.CharField(max_length=255, blank=True, null=True)

# #     CONFIDENCE_LEVEL_CHOICES = [
# #         ('yes', 'Yes'),
# #         ('sometimes', 'Sometimes'),
# #         ('no', 'No'),
# #     ]
# #     confidence_level = models.CharField(max_length=10, choices=CONFIDENCE_LEVEL_CHOICES)

# #     def __str__(self):
# #         return f"Non-Academic Data for {self.student.first_name} {self.student.last_name}"




# class StudentNonAcademicData(models.Model):
#     """
#     Model to store non-academic data for a student.
#     Uses TextField for multi-select fields to store comma-separated values.
#     """
#     student = models.OneToOneField(
#         'StudentData',
#         on_delete=models.CASCADE,
#         related_name='non_academic_data'
#     )

#     # STUDY HABITS
#     STUDY_HOURS_CHOICES = [
#         ('less_than_1', 'Less than 1 hour'),
#         ('1_2_hours', '1-2 hours'),
#         ('2_3_hours', '2-3 hours'),
#         ('more_than_3', 'More than 3 hours'),
#     ]
#     study_hours = models.CharField(max_length=20, choices=STUDY_HOURS_CHOICES)

#     # Use TextField for multi-select and 'other' input to be combined
#     study_place = models.TextField(
#         max_length=255,
#         help_text="Comma-separated study places",
#         blank=True,
#         default=''
#     )

#     STUDY_WITH_CHOICES = [
#         ('never', 'Never'),
#         ('sometimes', 'Sometimes'),
#         ('often', 'Often'),
#         ('always', 'Always'),
#     ]
#     study_with = models.CharField(max_length=20, choices=STUDY_WITH_CHOICES)

#     # FAMILY SUPPORT
#     live_with = models.TextField(
#         max_length=255,
#         help_text="Comma-separated live with options",
#         blank=True,
#         default=''
#     )

#     PARENT_HELP_CHOICES = [
#         ('never', 'Never'),
#         ('sometimes', 'Sometimes'),
#         ('often', 'Often'),
#         ('always', 'Always'),
#     ]
#     parent_help = models.CharField(max_length=20, choices=PARENT_HELP_CHOICES)

#     HIGHEST_EDUCATION_CHOICES = [
#         ('did_not_finish_hs', 'Did not finish high school'),
#         ('high_school_graduate', 'High school graduate'),
#         ('college_graduate', 'College graduate'),
#         ('other', 'Other'),
#     ]
#     highest_education = models.CharField(max_length=30, choices=HIGHEST_EDUCATION_CHOICES)

#     MARITAL_STATUS_CHOICES = [
#         ('married', 'Married'),
#         ('separated', 'Separated'),
#         ('other', 'Other'),
#     ]
#     marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)

#     # LIVING ENVIRONMENT
#     HOUSE_TYPE_CHOICES = [
#         ('apartment', 'Apartment'),
#         ('house', 'House'),
#         ('shared_housing', 'Shared housing'),
#         ('other', 'Other'),
#     ]
#     house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)

#     QUIET_PLACE_CHOICES = [
#         ('yes', 'Yes'),
#         ('no', 'No'),
#     ]
#     quiet_place = models.CharField(max_length=3, choices=QUIET_PLACE_CHOICES)

#     STUDY_AREA_CHOICES = [
#         ('very_quiet', 'Very quiet'),
#         ('somewhat_quiet', 'Somewhat quiet'),
#         ('noisy', 'Noisy'),
#     ]
#     study_area = models.CharField(max_length=20, choices=STUDY_AREA_CHOICES)

#     # TRANSPORTATION
#     TRANSPORT_MODE_CHOICES = [
#         ('walk', 'Walk'),
#         ('bicycle', 'Bicycle'),
#         ('public_transport', 'Public transport'),
#         ('family_vehicle', 'Family vehicle'),
#         ('other', 'Other'),
#     ]
#     transport_mode = models.CharField(max_length=20, choices=TRANSPORT_MODE_CHOICES)

#     TRAVEL_TIME_CHOICES = [
#         ('less_than_15', 'Less than 15 minutes'),
#         ('15_30_minutes', '15-30 minutes'),
#         ('30_60_minutes', '30-60 minutes'),
#         ('more_than_1_hour', 'More than 1 hour'),
#     ]
#     travel_time = models.CharField(max_length=20, choices=TRAVEL_TIME_CHOICES)

#     # ACCESS TO LEARNING RESOURCES
#     access_resources = models.TextField(
#         max_length=255,
#         help_text="Comma-separated access resources",
#         blank=True,
#         default=''
#     )

#     COMPUTER_USE_CHOICES = [
#         ('never', 'Never'),
#         ('sometimes', 'Sometimes'),
#         ('often', 'Often'),
#         ('always', 'Always'),
#     ]
#     computer_use = models.CharField(max_length=20, choices=COMPUTER_USE_CHOICES)

#     # PERSONALITY TRAITS AND INTERESTS
#     hobbies = models.CharField(max_length=255, blank=True)

#     personality_traits = models.TextField(
#         max_length=255,
#         help_text="Comma-separated personality traits",
#         blank=True,
#         default=''
#     )

#     CONFIDENCE_LEVEL_CHOICES = [
#         ('yes', 'Yes'),
#         ('sometimes', 'Sometimes'),
#         ('no', 'No'),
#     ]
#     confidence_level = models.CharField(max_length=10, choices=CONFIDENCE_LEVEL_CHOICES)

#     def __str__(self):
#         return f"Non-Academic Data for {self.student.first_name} {self.student.last_name}"

#     def clean(self):
#         # Basic validation to ensure at least one choice is made for multi-select fields
#         if not self.study_place:
#             raise ValidationError({'study_place': 'Please select at least one study place.'})
#         if not self.live_with:
#             raise ValidationError({'live_with': 'Please select at least one person you live with.'})
#         if not self.access_resources:
#             raise ValidationError({'access_resources': 'Please select at least one resource you have access to.'})
#         if not self.personality_traits:
#             raise ValidationError({'personality_traits': 'Please select at least one personality trait.'})



# class StudentAcademicData(models.Model):
#     student = models.OneToOneField('StudentData', on_delete=models.CASCADE, related_name='academic_data')

#     # Basic Information
#     lrn = models.CharField(max_length=12)  # You may want to validate this matches StudentData.lrn
#     DOST_EXAM_RESULT_CHOICES = [
#         ('passed', 'Passed'),
#         ('failed', 'Failed'),
#         ('not-taken', 'Not Taken'),
#     ]
#     dost_exam_result = models.CharField(max_length=10, choices=DOST_EXAM_RESULT_CHOICES)

#     # File upload for Grade 6 Report Card
#     report_card = models.FileField(upload_to='report_cards/')

#     # Grade 6 Academic Data (grades)
#     mathematics = models.DecimalField(max_digits=5, decimal_places=2)
#     araling_panlipunan = models.DecimalField(max_digits=5, decimal_places=2)
#     english = models.DecimalField(max_digits=5, decimal_places=2)
#     edukasyon_pagpapakatao = models.DecimalField(max_digits=5, decimal_places=2)
#     science = models.DecimalField(max_digits=5, decimal_places=2)
#     edukasyon_pangkabuhayan = models.DecimalField(max_digits=5, decimal_places=2)
#     filipino = models.DecimalField(max_digits=5, decimal_places=2)
#     mapeh = models.DecimalField(max_digits=5, decimal_places=2)

#     overall_average = models.DecimalField(max_digits=5, decimal_places=2)

#     # Other Details
#     IS_WORKING_STUDENT_CHOICES = [
#         ('yes', 'Yes'),
#         ('no', 'No'),
#     ]
#     is_working_student = models.CharField(max_length=3, choices=IS_WORKING_STUDENT_CHOICES)

#     WORK_TYPE_CHOICES = [
#         ('fulltime', 'Full Time'),
#         ('self-employed', 'Self Employed'),
#         ('family-business', 'Family Business'),
#     ]
#     work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES, blank=True, null=True)

#     IS_PWD_CHOICES = [
#         ('yes', 'Yes'),
#         ('no', 'No'),
#     ]
#     is_pwd = models.CharField(max_length=3, choices=IS_PWD_CHOICES)

#     DISABILITY_TYPE_CHOICES = [
#         ('visual-impairment', 'Visual Impairment'),
#         ('physical-disability', 'Physical Disability'),
#         ('learning-disability', 'Learning Disability'),
#         ('deaf-hard-hearing', 'Deaf/Hard of Hearing'),
#         ('intellectual-disability', 'Intellectual Disability'),
#         ('autism', 'Autism Spectrum Disorder'),
#         ('multiple-disabilities', 'Multiple Disabilities'),
#         ('others', 'Others'),
#     ]
#     disability_type = models.CharField(max_length=30, choices=DISABILITY_TYPE_CHOICES, blank=True, null=True)

#     # Terms agreement
#     agreed_to_terms = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Academic Data for {self.student.first_name} {self.student.last_name}"
