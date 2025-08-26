from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError


class EnrollingOption(models.Model):
    """Lookup table for 'Enrolling As' options"""
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class StudentInformation(models.Model):
    """Main student profile (personal info only)"""

    lrn = models.CharField(max_length=20, unique=True)
    enrolling_as = models.ManyToManyField(EnrollingOption, blank=True)

    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    bday = models.DateField()
    address = models.TextField()
    place_of_birth = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    dialect = models.CharField(max_length=50)
    ethnic = models.CharField(max_length=50)
    previous_school = models.CharField(max_length=100)
    previous_grade_section = models.CharField(max_length=50)
    last_attended_sy = models.CharField(max_length=20)

    def clean(self):
        """Custom validation for 'enrolling_as' rules."""
        options = list(self.enrolling_as.values_list("name", flat=True))

        if len(options) > 2:
            raise ValidationError("You can select at most 2 enrolling options.")

        if "4ps" in options:
            if len(options) > 2:
                raise ValidationError("If 4Ps is selected, only one more option can be chosen.")
        else:
            if len(options) > 1:
                raise ValidationError("Only 4Ps can be combined with another option.")

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.lrn})"


class AcademicData(models.Model):
    """Academic data of a student"""
    student = models.OneToOneField(StudentInformation, on_delete=models.CASCADE, related_name="academic")

    dost_result = models.CharField(max_length=20)
    math_grade = models.DecimalField(max_digits=5, decimal_places=2)
    eng_grade = models.DecimalField(max_digits=5, decimal_places=2)
    fil_grade = models.DecimalField(max_digits=5, decimal_places=2)
    sci_grade = models.DecimalField(max_digits=5, decimal_places=2)
    arpan_grade = models.DecimalField(max_digits=5, decimal_places=2)
    esp_grade = models.DecimalField(max_digits=5, decimal_places=2)
    epp_grade = models.DecimalField(max_digits=5, decimal_places=2)
    mapeh_grade = models.DecimalField(max_digits=5, decimal_places=2)
    dost_img = models.ImageField(upload_to="dost_results/", blank=True, null=True)
    reportcard_img = models.ImageField(upload_to="report_cards/", blank=True, null=True)

    def __str__(self):
        return f"Academic Data - {self.student.lrn}"


class NonAcademicData(models.Model):
    """Non-academic survey data"""
    student = models.OneToOneField(StudentInformation, on_delete=models.CASCADE, related_name="non_academic")

    hours_of_study = models.CharField(max_length=50)
    place_of_study = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    study_with_friends = models.CharField(max_length=50)
    who_do_you_live_with = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    parents_help_schoolwork = models.CharField(max_length=50)
    highest_parent_educ = models.CharField(max_length=100)
    parent_status = models.CharField(max_length=50)
    type_of_house = models.CharField(max_length=50)
    quiet_place_to_study = models.BooleanField(default=False)
    study_area_desc = models.CharField(max_length=50)

    transportation_type = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    travel_time_to_school = models.CharField(max_length=50)

    access_to_resources = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    computer_usage = models.CharField(max_length=50)

    hobbies = models.TextField(blank=True, null=True)
    self_description = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    confident_in_school = models.CharField(max_length=50)
    agree_to_regulations = models.BooleanField(default=True)

    def __str__(self):
        return f"Non-Academic Data - {self.student.lrn}"


class FamilyInformation(models.Model):
    """Family info linked to student"""
    student = models.OneToOneField(StudentInformation, on_delete=models.CASCADE, related_name="family")

    guardian_pic = models.ImageField(upload_to="guardians/", blank=True, null=True)

    # Father
    father_firstname = models.CharField(max_length=50)
    father_lastname = models.CharField(max_length=50)
    father_middlename = models.CharField(max_length=50, blank=True, null=True)
    father_age = models.IntegerField()
    father_occupation = models.CharField(max_length=100)
    father_bday = models.DateField()
    father_contact_number = models.CharField(max_length=20, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)

    # Mother
    mother_firstname = models.CharField(max_length=50)
    mother_lastname = models.CharField(max_length=50)
    mother_middlename = models.CharField(max_length=50, blank=True, null=True)
    mother_age = models.IntegerField()
    mother_occupation = models.CharField(max_length=100)
    mother_bday = models.DateField()
    mother_contactnumber = models.CharField(max_length=20, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)

    # Guardian
    guardian_firstname = models.CharField(max_length=50)
    guardian_lastname = models.CharField(max_length=50)
    guardian_middlename = models.CharField(max_length=50, blank=True, null=True)
    guardian_age = models.IntegerField()
    guardian_occupation = models.CharField(max_length=100)
    guardian_bday = models.DateField()
    guardian_address = models.TextField()
    guardian_relationship = models.CharField(max_length=50)
    guardian_contactnumber = models.CharField(max_length=20, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Family Info - {self.student.lrn}"
