from django.db import models

class Family(models.Model):
    # Father's Information
    father_family_name = models.CharField(max_length=100, verbose_name="Father's Family Name")
    father_first_name = models.CharField(max_length=100, verbose_name="Father's First Name")
    father_middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Father's Middle Name")
    father_age = models.IntegerField(verbose_name="Father's Age")
    father_occupation = models.CharField(max_length=100, verbose_name="Father's Occupation")
    father_dob = models.DateField(verbose_name="Father's Date of Birth")
    father_contact_number = models.CharField(max_length=20, verbose_name="Father's Contact Number")
    father_email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Father's Email Address")

    # Mother's Information
    mother_family_name = models.CharField(max_length=100, verbose_name="Mother's Family Maiden Name")
    mother_first_name = models.CharField(max_length=100, verbose_name="Mother's First Name")
    mother_middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mother's Middle Name")
    mother_age = models.IntegerField(verbose_name="Mother's Age")
    mother_occupation = models.CharField(max_length=100, verbose_name="Mother's Occupation")
    mother_dob = models.DateField(verbose_name="Mother's Date of Birth")
    mother_contact_number = models.CharField(max_length=20, verbose_name="Mother's Contact Number")
    mother_email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Mother's Email Address")

    # Guardian's Information (if not staying with parents)
    guardian_family_name = models.CharField(max_length=100, verbose_name="Guardian's Family Name")
    guardian_first_name = models.CharField(max_length=100, verbose_name="Guardian's First Name")
    guardian_middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Guardian's Middle Name")
    guardian_age = models.IntegerField(verbose_name="Guardian's Age")
    guardian_occupation = models.CharField(max_length=100, verbose_name="Guardian's Occupation")
    guardian_dob = models.DateField(verbose_name="Guardian's Date of Birth")
    guardian_address = models.TextField(verbose_name="Guardian's Complete Home Address")
    guardian_relationship = models.CharField(max_length=100, verbose_name="Relationship with the student")
    guardian_contact_number = models.CharField(max_length=20, verbose_name="Guardian's Contact Number")
    guardian_email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Guardian's Email Address")

    parent_photo = models.ImageField(upload_to='parent_photos/', blank=True, null=True, verbose_name="Parent 1x1 Picture")

    def __str__(self):
        return f"Family of {self.father_family_name} & {self.mother_family_name}"

    class Meta:
        verbose_name_plural = "Families"


class Student(models.Model):
    # Initial Enrollment Data
    lrn = models.CharField(max_length=12, unique=True, verbose_name="LRN Number")
    enrolling_as = models.CharField(max_length=255, blank=True, null=True, verbose_name="Enrolling As") # Stores comma-separated choices
    is_sped = models.BooleanField(default=False, verbose_name="Needs Special Education Program")
    sped_details = models.CharField(max_length=255, blank=True, null=True, verbose_name="SPED Details")
    is_working_student = models.BooleanField(default=False, verbose_name="Is a Working Student")
    working_details = models.CharField(max_length=255, blank=True, null=True, verbose_name="Working Student Details")
    photo = models.ImageField(upload_to='student_photos/', verbose_name="Student 1x1 Picture")

    # Student's Information Data
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Middle Name")
    address = models.TextField(verbose_name="Present Home Address")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=50, verbose_name="Gender")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    place_of_birth = models.CharField(max_length=255, verbose_name="Place of Birth")
    religion = models.CharField(max_length=100, verbose_name="Religion")
    dialect_spoken = models.CharField(max_length=100, verbose_name="Dialect Spoken")
    ethnic_tribe = models.CharField(max_length=100, verbose_name="Ethnic Tribe")
    last_school_attended = models.CharField(max_length=255, verbose_name="Name of Last School Attended")
    previous_grade_section = models.CharField(max_length=100, verbose_name="Previous Grade and Section")
    last_school_year = models.CharField(max_length=20, verbose_name="School Year Last Attended")

    # Relationships
    family_data = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Family Information")
    section_placement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Assigned Section/Program")

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.lrn})"

    class Meta:
        verbose_name_plural = "Students"


class StudentNonAcademic(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True, verbose_name="Student")

    # Student's Study Habits
    study_hours = models.CharField(max_length=50, verbose_name="Hours spent studying/homework each day")
    study_place = models.TextField(verbose_name="Where student usually studies") # Stores comma-separated choices including 'other'
    study_with = models.CharField(max_length=50, verbose_name="How often student studies with friends/classmates")

    # Student's Family Support
    live_with = models.TextField(verbose_name="Who student lives with") # Stores comma-separated choices including 'other'
    parent_help = models.CharField(max_length=50, verbose_name="Do parents/guardians help with schoolwork")
    highest_education = models.CharField(max_length=100, verbose_name="Highest education level of parents/guardians") # Stores 'other' input
    marital_status = models.CharField(max_length=50, verbose_name="Parents' marital status") # Stores 'other' input

    # Student's Living Environment
    house_type = models.CharField(max_length=100, verbose_name="Type of house student lives in") # Stores 'other' input
    quiet_place = models.CharField(max_length=10, verbose_name="Has a quiet place to study at home")
    study_area = models.CharField(max_length=50, verbose_name="Description of study area at home")

    # Transportation
    transport_mode = models.CharField(max_length=100, verbose_name="How student usually gets to school") # Stores 'other' input
    travel_time = models.CharField(max_length=50, verbose_name="Time taken to get to school")

    # Student's Access to Learning Resources
    access_resources = models.TextField(verbose_name="Access to learning resources at home") # Stores comma-separated choices
    computer_use = models.CharField(max_length=50, verbose_name="How often computer/tablet is used for schoolwork")

    # Student's Personality Traits and Interests
    hobbies = models.TextField(verbose_name="Free time activities/hobbies")
    personality_traits = models.TextField(verbose_name="Student's personality traits") # Stores comma-separated choices including 'other'
    confidence_level = models.CharField(max_length=50, verbose_name="Confidence about doing well in school")

    def __str__(self):
        return f"Non-Academic Data for {self.student.first_name} {self.student.last_name}"

    class Meta:
        verbose_name_plural = "Student Non-Academic Data"


class StudentAcademic(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True, verbose_name="Student")

    # Basic Information
    lrn = models.CharField(max_length=12, verbose_name="LRN Number") # Redundant but kept for form mapping
    dost_exam_result = models.CharField(max_length=50, verbose_name="DOST Exam Result")
    report_card = models.FileField(upload_to='report_cards/', verbose_name="Grade 6 Report Card")

    # Grade 6 Academic Data
    mathematics = models.FloatField(verbose_name="Mathematics Grade")
    araling_panlipunan = models.FloatField(verbose_name="Araling Panlipunan Grade")
    english = models.FloatField(verbose_name="English Grade")
    edukasyon_pagpapakatao = models.FloatField(verbose_name="Edukasyon sa Pagpapakatao Grade")
    science = models.FloatField(verbose_name="Science Grade")
    edukasyon_pangkabuhayan = models.FloatField(verbose_name="Edukasyon Pampahalagang Pangkabuhayang Grade")
    filipino = models.FloatField(verbose_name="Filipino Grade")
    mapeh = models.FloatField(verbose_name="MAPEH Grade")
    overall_average = models.FloatField(verbose_name="Overall Average")

    # Other Details (populated from Student model)
    is_working_student = models.BooleanField(default=False, verbose_name="Is a Working Student")
    work_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Work Type")
    is_pwd = models.BooleanField(default=False, verbose_name="Is a Person With Disability")
    disability_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type of Disability")
    agreed_to_terms = models.BooleanField(default=False, verbose_name="Agreed to School Policies and Terms")

    def __str__(self):
        return f"Academic Data for {self.student.first_name} {self.student.last_name}"

    class Meta:
        verbose_name_plural = "Student Academic Data"


class SectionPlacement(models.Model):
    PROGRAM_CHOICES = [
        ('STE', 'Science Technology and Engineering'),
        ('SPFL', 'Special Program in Foreign Language'),
        ('SPTVL', 'Special Program in Technical Vocational Livelihood'),
        ('TOP5', 'Top 5 Regular Class'),
        ('HETERO', 'Hetero Regular class'),
        ('OHSP', 'Open High School Program'),
        ('SNED', 'Special Needs Education Program'),
        
    ]
    
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)


    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='section_placements')
    selected_program = models.CharField(max_length=10, choices=PROGRAM_CHOICES, verbose_name="Selected Program/Section")
    placement_date = models.DateTimeField(auto_now_add=True, verbose_name="Placement Date")
    # eligibility_snapshot = models.JSONField(blank=True, null=True, verbose_name="Eligibility Data Snapshot")
    # notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes")

    class Meta:
        verbose_name = "Section Placement"
        verbose_name_plural = "Section Placements"
        ordering = ['-placement_date']
        unique_together = ('student', 'selected_program')  # Optional: prevent duplicate placements for same program

    def __str__(self):
        return f"{self.student} - {self.get_selected_program_display()} ({self.placement_date.strftime('%Y-%m-%d')})"
