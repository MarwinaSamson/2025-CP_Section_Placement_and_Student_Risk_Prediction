from django.db import models

# Choices for common fields (optional but good practice)
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

DOST_EXAM_CHOICES = [
    ('passed', 'Passed'),
    ('failed', 'Failed'),
    ('not-taken', 'Not Taken'),
]

DISABILITY_TYPE_CHOICES = [
    ('not-applicable', 'Not Applicable'),
    ('deaf-hard-hearing', 'Deaf/Hard of Hearing'),
    ('physical-disability', 'Physical Disability'),
    ('learning-disability', 'Learning Disability'),
    ('visual-impairment', 'Visual Impairment'),
    ('intellectual-disability', 'Intellectual Disability'),
    ('autism', 'Autism Spectrum Disorder'),
    ('multiple-disabilities', 'Multiple Disabilities'),
]

# --- Core Models ---

class Person(models.Model):
    """
    An abstract base class for common fields shared by Parent and Guardian.
    This helps reduce redundancy.
    """
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to='person_pictures/', blank=True, null=True) # Generic picture field

    class Meta:
        abstract = True # This model won't create a table in the database

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Parent(Person):
    """
    Represents a biological or adoptive parent.
    A parent can have multiple children (students).
    """
    pass

class Guardian(Person):
    """
    Represents a guardian who may or may not be a parent.
    A guardian can be responsible for multiple students.
    """
    home_address = models.CharField(max_length=255, blank=True, null=True)
    relationship_to_student = models.CharField(max_length=100, blank=True, null=True) # e.g., "Aunt", "Uncle", "Legal Guardian"

    def __str__(self):
        return f"Guardian: {self.first_name} {self.last_name}"

class Student(models.Model):
    # From studentData.html
    lrn_number = models.CharField(max_length=20, unique=True)
    is_4ps_member = models.BooleanField(default=False)
    is_retained = models.BooleanField(default=False)
    is_balik_aral = models.BooleanField(default=False)
    is_transferee = models.BooleanField(default=False)
    needs_sped = models.BooleanField(default=False)
    sped_details = models.CharField(max_length=255, blank=True, null=True)
    is_working_student = models.BooleanField(default=False)
    working_student_details = models.CharField(max_length=255, blank=True, null=True)
    student_picture = models.ImageField(upload_to='student_pictures/', blank=True, null=True)

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    present_home_address = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    religion = models.CharField(max_length=100)
    dialect_spoken = models.CharField(max_length=100)
    ethnic_tribe = models.CharField(max_length=100)
    last_school_attended = models.CharField(max_length=255)
    previous_grade_section = models.CharField(max_length=100)
    school_year_last_attended = models.CharField(max_length=20)

    # Relationships to Parent and Guardian
    father = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_father')
    mother = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='children_as_mother')

    guardians = models.ManyToManyField(Guardian, blank=True, related_name='students_under_guardianship')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.lrn_number})"

class AcademicData(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='academic_data')

    # From studentAcademic.html
    dost_exam_result = models.CharField(max_length=20, choices=DOST_EXAM_CHOICES)
    report_card = models.FileField(upload_to='report_cards/', blank=True, null=True)

    # Grade 6 Academic Data
    mathematics_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    araling_panlipunan_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    english_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    edukasyon_pagpapakatao_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    science_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    edukasyon_pangkabuhayan_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    filipino_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mapeh_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    overall_average = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Other Details (from studentAcademic.html and studentAcademic2.html)
    # Note: is_working_student is already in Student model, so removed here to avoid redundancy
    is_pwd = models.BooleanField(default=False)
    disability_type = models.CharField(max_length=50, blank=True, null=True, choices=DISABILITY_TYPE_CHOICES) # From studentAcademic2.html
    agreed_to_terms = models.BooleanField(default=False)

    # Additional field from studentAcademic2.html
    birth_certificate = models.FileField(upload_to='birth_certificates/', blank=True, null=True)

    def __str__(self):
        return f"Academic Data for {self.student.first_name} {self.student.last_name}"

class NonAcademicSurvey(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='non_academic_survey')

    study_hours_per_day = models.CharField(max_length=50, blank=True, null=True)
    study_location = models.CharField(max_length=255, blank=True, null=True)
    study_with_friends_frequency = models.CharField(max_length=50, blank=True, null=True)

    parent_help_schoolwork = models.CharField(max_length=50, blank=True, null=True)
    parent_highest_education = models.CharField(max_length=100, blank=True, null=True)
    parent_marital_status = models.CharField(max_length=50, blank=True, null=True)

    house_type = models.CharField(max_length=100, blank=True, null=True)
    has_quiet_study_place = models.BooleanField(default=False)
    study_area_description = models.CharField(max_length=50, blank=True, null=True)

    transportation_mode = models.CharField(max_length=255, blank=True, null=True)
    travel_time_to_school = models.CharField(max_length=50, blank=True, null=True)

    access_to_resources = models.CharField(max_length=255, blank=True, null=True)
    computer_use_frequency = models.CharField(max_length=50, blank=True, null=True)

    free_time_activities = models.TextField(blank=True, null=True)
    personality_traits = models.CharField(max_length=255, blank=True, null=True)
    confidence_in_school = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Non-Academic Survey for {self.student.first_name} {self.student.last_name}"

