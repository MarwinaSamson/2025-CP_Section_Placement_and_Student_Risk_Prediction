from django.db import models

# ---------------------
# Primary Student Table
# ---------------------
class Student(models.Model):
    lrn = models.CharField(max_length=12, unique=True)   # LRN Number
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    dialect_spoken = models.CharField(max_length=50, blank=True, null=True)
    ethnic_tribe = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()

    # Enrollment-related info
    last_school_attended = models.CharField(max_length=150, blank=True, null=True)
    previous_grade_section = models.CharField(max_length=50, blank=True, null=True)
    last_school_year = models.CharField(max_length=20, blank=True, null=True)
    is_4ps_member = models.BooleanField(default=False)
    is_retained = models.BooleanField(default=False)
    is_balik_aral = models.BooleanField(default=False)
    is_transferee = models.BooleanField(default=False)

    # Flags
    is_sped = models.BooleanField(default=False)
    sped_details = models.CharField(max_length=150, blank=True, null=True)
    is_working_student = models.BooleanField(default=False)
    working_details = models.CharField(max_length=150, blank=True, null=True)

    photo = models.ImageField(upload_to="student_photos/", blank=True, null=True)

    def __str__(self):
        return f"{self.lrn} - {self.last_name}, {self.first_name}"


# ---------------------
# Family / Guardian Info
# ---------------------
class Guardian(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

    # Link to students (guardian can have multiple children)
    students = models.ManyToManyField(Student, related_name="guardians")

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# ---------------------
# Academic Info
# ---------------------
class AcademicRecord(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="academic")
    dost_exam_result = models.CharField(max_length=20, choices=[("passed", "Passed"), ("failed", "Failed"), ("not-taken", "Not Taken")])

    # Grades
    mathematics = models.DecimalField(max_digits=5, decimal_places=2)
    araling_panlipunan = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    edukasyon_pagpapakatao = models.DecimalField(max_digits=5, decimal_places=2)
    science = models.DecimalField(max_digits=5, decimal_places=2)
    edukasyon_pangkabuhayan = models.DecimalField(max_digits=5, decimal_places=2)
    filipino = models.DecimalField(max_digits=5, decimal_places=2)
    mapeh = models.DecimalField(max_digits=5, decimal_places=2)
    overall_average = models.DecimalField(max_digits=5, decimal_places=2)

    report_card = models.FileField(upload_to="report_cards/", blank=True, null=True)
    dost_result_file = models.FileField(upload_to="dost_results/", blank=True, null=True)

    def __str__(self):
        return f"Academic Record for {self.student}"


# ---------------------
# Non-Academic Info
# ---------------------
class NonAcademicRecord(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="nonacademic")

    study_hours = models.CharField(max_length=50, blank=True, null=True)
    study_place = models.CharField(max_length=100, blank=True, null=True)
    study_with = models.CharField(max_length=50, blank=True, null=True)

    family_support = models.CharField(max_length=50, blank=True, null=True)
    highest_education = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)

    house_type = models.CharField(max_length=50, blank=True, null=True)
    quiet_place = models.BooleanField(default=False)
    study_area = models.CharField(max_length=50, blank=True, null=True)

    transport_mode = models.CharField(max_length=50, blank=True, null=True)
    travel_time = models.CharField(max_length=50, blank=True, null=True)

    access_resources = models.CharField(max_length=100, blank=True, null=True)
    computer_use = models.CharField(max_length=50, blank=True, null=True)

    hobbies = models.TextField(blank=True, null=True)
    personality_traits = models.CharField(max_length=100, blank=True, null=True)
    confidence_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Non-Academic Record for {self.student}"


# ---------------------
# Qualified Programs (from ML model)
# ---------------------
class QualifiedProgram(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="qualified_programs")

    ste = models.BooleanField(default=False)
    spfl = models.BooleanField(default=False)
    sptvl = models.BooleanField(default=False)
    ohsp = models.BooleanField(default=False)
    sned = models.BooleanField(default=False)   # For disabilities
    top5 = models.BooleanField(default=False)
    regular = models.BooleanField(default=True)

    def __str__(self):
        return f"Programs for {self.student}"
