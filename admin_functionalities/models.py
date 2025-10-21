# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.core.validators import MinValueValidator, MaxValueValidator
# from enrollmentprocess.models import Student
# from django.db import models
# from django.utils import timezone
# from datetime import date



# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, first_name='', last_name='', middle_name='', **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')

#         email = self.normalize_email(email)
#         user = self.model(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             middle_name=middle_name,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password, first_name='', last_name='', middle_name='', **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', True)  # Required for admin permissions

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')

#         return self.create_user(username, email, password, first_name, last_name, middle_name, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     id = models.BigAutoField(primary_key=True)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     middle_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     is_staff = models.BooleanField(default=False)  # Required for admin permissions

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = CustomUserManager()

#     def __str__(self):
#         full_name = f"{self.first_name} {self.middle_name} {self.last_name}".strip()
#         return full_name if full_name else self.username


# class Notification(models.Model):
#     NOTIFICATION_TYPES = [
#         ('student_enrollment', 'Student Enrollment'),  # Light blue
#         # ... other types for future (teacher, danger) ...
#     ]
    
#     title = models.CharField(max_length=200, default="New Enrollment Submission")
#     message = models.TextField()  # E.g., "Jane Doe confirmed STE placement"
#     notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='student_enrollment')
#     program = models.CharField(max_length=50, blank=True)  # E.g., "STE"
#     related_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_read = models.BooleanField(default=False)
    
#     class Meta:
#         ordering = ['-created_at']
    
#     def __str__(self):
#         return f"{self.title} - {self.program}"

# # Requirements model
# class StudentRequirements(models.Model):
#     student = models.OneToOneField('enrollmentprocess.Student', on_delete=models.CASCADE, related_name='requirements')
#     birth_certificate = models.BooleanField(default=False)
#     good_moral = models.BooleanField(default=False)
#     interview_done = models.BooleanField(default=False)
#     reading_assessment_done = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f"Requirements for {self.student}"
    

# class Teacher(models.Model):
#     """
#     Core model for teacher profiles (personal, contact, position, roles).
#     Supports table (Full Name, Sex, Age, Position) and modal (Teacher Data, Contact).
#     """
#     # Personal Data
#     employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True, verbose_name="Linked User Account")
#     last_name = models.CharField(max_length=50, verbose_name="Last Name")
#     first_name = models.CharField(max_length=50, verbose_name="First Name")
#     middle_name = models.CharField(max_length=50, blank=True, verbose_name="Middle Name")
#     full_name = models.CharField(max_length=150, blank=True, editable=False)  # Auto-generated for table

#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#     ]
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sex/Gender")
    
#     date_of_birth = models.DateField(verbose_name="Date of Birth")
#     age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], blank=True, editable=False, verbose_name="Age")  # Auto-computed

#     # Position/Department
#     POSITION_CHOICES = [
#         ('Teacher I', 'Teacher I'),
#         ('Teacher II', 'Teacher II'),
#         ('Teacher III', 'Teacher III'),
#         ('Head Teacher', 'Head Teacher'),
#         ('Principal', 'Principal'),
#         # Add more as needed
#     ]
#     position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name="Position")
    
#     DEPARTMENT_CHOICES = [
#         ('Science', 'Science'),
#         ('Mathematics', 'Mathematics'),
#         ('English', 'English'),
#         ('Filipino', 'Filipino'),
#         ('Social Studies', 'Social Studies'),
#         ('MAPEH', 'MAPEH'),
#         ('TLE', 'Technology and Livelihood Education'),
#         ('Values Education', 'Values Education'),
#         # Add more
#     ]
#     department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, verbose_name="Department")

#     # Roles (for adviser/subject teacher)
#     is_adviser = models.BooleanField(default=False, verbose_name="Can be Adviser")
#     is_subject_teacher = models.BooleanField(default=True, verbose_name="Can be Subject Teacher")  # Default True as most are

#     # Contact Data
#     email = models.EmailField(unique=True, verbose_name="Email")
#     phone = models.CharField(max_length=20, verbose_name="Phone")
#     address = models.TextField(blank=True, verbose_name="Address")

#     # Profile Image
#     profile_photo = models.ImageField(upload_to='teachers/profiles/', blank=True, null=True, verbose_name="Profile Photo")

#     # Status/Audit
#     is_active = models.BooleanField(default=True, verbose_name="Is Active")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         # Auto-generate full_name (e.g., "Ackerman, Mikasa Armin")
#         self.full_name = f"{self.last_name}, {self.first_name} {self.middle_name}".strip()
#         # Auto-compute age from DOB
#         if self.date_of_birth:
#             today = date.today()
#             self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.full_name

#     class Meta:
#         ordering = ['last_name', 'first_name']
#         verbose_name = "Teacher"
#         verbose_name_plural = "Teachers"
#         indexes = [models.Index(fields=['last_name', 'first_name'])]  # For search


# class ChangeHistory(models.Model):
#     """
#     Audit log for teacher changes (e.g., "Record Created", "Updated Profile").
#     Populates modal's Change History table.
#     """
#     ACTION_CHOICES = [
#         ('created', 'Record Created'),
#         ('updated', 'Profile Updated'),
#         ('role_changed', 'Role Changed'),
#         ('deactivated', 'Deactivated'),
#         ('reactivated', 'Reactivated'),
#         # Add more as needed
#     ]
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='change_history', verbose_name="Teacher")
#     action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Action")
#     description = models.TextField(blank=True, help_text="Details of the change (e.g., 'Email updated to new@deped.gov.ph')")
#     date = models.DateField(auto_now_add=True, verbose_name="Date")
#     time = models.TimeField(auto_now_add=True, verbose_name="Time")

#     def __str__(self):
#         return f"{self.get_action_display()} - {self.teacher.full_name} ({self.date})"

#     class Meta:
#         ordering = ['-date', '-time']
#         verbose_name = "Change History"
#         verbose_name_plural = "Change Histories"

# class AddUser Log(models.Model):
#     """
#     Specific log for user addition activities (e.g., "Created a New User Account" in settings.html History Logs).
#     Includes details of the added user for auditing without needing to join to User/Teacher models.
#     """
#     # Who performed the action (admin/user)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='add_user_logs', verbose_name="Admin/User Who Added")
    
#     # Action details
#     action = models.CharField(max_length=100, verbose_name="Activity")  # e.g., "Created a New User Account"
#     date = models.DateField(auto_now_add=True, verbose_name="Date")
#     time = models.TimeField(auto_now_add=True, verbose_name="Time")
#     description = models.TextField(blank=True, verbose_name="Additional Description")
    
#     # Details of the AFFECTED/NEW user (populated only for add actions)
#     affected_first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="New User's First Name")
#     affected_last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="New User's Last Name")
#     affected_email = models.EmailField(blank=True, null=True, verbose_name="New User's Email")
#     affected_employee_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="New User's Employee ID")
    
#     # Role access booleans (set True if selected in modal, False otherwise)
#     affected_is_admin = models.BooleanField(default=False, verbose_name="New User Has Administrator Access")
#     affected_is_staff_expert = models.BooleanField(default=False, verbose_name="New User Has Staff Expert Access")
#     affected_is_adviser = models.BooleanField(default=False, verbose_name="New User Has Adviser Access")
#     affected_is_teacher = models.BooleanField(default=False, verbose_name="New User Has Teacher Access")

#     def __str__(self):
#         return f"{self.action} by {self.user.username} on {self.date} (for {self.affected_first_name} {self.affected_last_name})"

#     class Meta:
#         ordering = ['-date', '-time']
#         verbose_name = "Add User Log"
#         verbose_name_plural = "Add User Logs"
#         indexes = [models.Index(fields=['user', 'date'])]  # For efficient querying

from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from enrollmentprocess.models import Student
from django.db import models
from django.utils import timezone
from datetime import date



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = email
        username = username  # Set username to email for simplicity (unique via email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser (AbstractBaseUser , PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)  # Set to email in create_user
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)  # Required for admin permissions
    force_password_change = models.BooleanField(default=False, verbose_name="Force Password Change on First Login")

    # NEW: Essentials for admin creation (position/department for all users)
    employee_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Employee ID")
    position = models.CharField(max_length=100, blank=True, verbose_name="Position")  # e.g., 'Teacher', 'Administrative'
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Department")  # Optional

    # NEW: Role flags for subtypes (especially teachers)
    is_staff_expert = models.BooleanField(default=False, verbose_name="Staff Expert Access")  # For Staff Administrative
    is_teacher = models.BooleanField(default=False, verbose_name="General Teacher Role")  # Umbrella for Teacher position
    is_subject_teacher = models.BooleanField(default=False, verbose_name="Subject Teacher Access")  # Subtype
    is_adviser = models.BooleanField(default=False, verbose_name="Adviser Access")  # Subtype



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def clean(self):
         super().clean()

    def __str__(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    class Meta:
        verbose_name = "User "
        verbose_name_plural = "Users"



class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('student_enrollment', 'Student Enrollment'),  # Light blue
        # ... other types for future (teacher, danger) ...
    ]
    
    title = models.CharField(max_length=200, default="New Enrollment Submission")
    message = models.TextField()  # E.g., "Jane Doe confirmed STE placement"
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='student_enrollment')
    program = models.CharField(max_length=50, blank=True)  # E.g., "STE"
    related_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.program}"

# Requirements model
class StudentRequirements(models.Model):
    student = models.OneToOneField('enrollmentprocess.Student', on_delete=models.CASCADE, related_name='requirements')
    birth_certificate = models.BooleanField(default=False)
    good_moral = models.BooleanField(default=False)
    interview_done = models.BooleanField(default=False)
    reading_assessment_done = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Requirements for {self.student}"
    

class Teacher(models.Model):
    """
    Core model for teacher profiles (personal, contact, position, roles).
    Supports table (Full Name, Sex, Age, Position) and modal (Teacher Data, Contact).
    """
    # Personal Data
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True, verbose_name="Linked User Account")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Middle Name")
    full_name = models.CharField(max_length=150, blank=True, editable=False)  # Auto-generated for table

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Sex/Gender")
    
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], null=True, blank=True, editable=False, verbose_name="Age")  # Auto-computed

    # Position/Department
    POSITION_CHOICES = [
        ('Teacher I', 'Teacher I'),
        ('Teacher II', 'Teacher II'),
        ('Teacher III', 'Teacher III'),
        ('Master Teacher I', 'Master Teacher I'),
        ('Master Teacher II', 'Master Teacher II'),
        ('Master Teacher III', 'Master Teacher III'),
        ('Head Teacher I', 'Head Teacher I'),
        ('Head Teacher II', 'Head Teacher II'),
        ('Head Teacher III', 'Head Teacher III'),
        ('Principal I', 'Principal I'),
        ('Principal II', 'Principal II'),
        ('Principal III', 'Principal III'),
        ('School Head', 'School Head'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name="Position")
    
    DEPARTMENT_CHOICES = [
        ('Science', 'Science'),
        ('Mathematics', 'Mathematics'),
        ('English', 'English'),
        ('Filipino', 'Filipino'),
        ('Social Studies', 'Social Studies'),
        ('MAPEH', 'MAPEH'),
        ('TLE', 'Technology and Livelihood Education'),
        ('Values Education', 'Values Education'),
        # Add more
    ]
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, verbose_name="Department")

    # Roles (for adviser/subject teacher)
    is_adviser = models.BooleanField(default=False, verbose_name="Can be Adviser")
    is_subject_teacher = models.BooleanField(default=True, verbose_name="Can be Subject Teacher")  # Default True as most are

    # Contact Data
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    address = models.TextField(blank=True, verbose_name="Address")

    # Profile Image
    profile_photo = models.ImageField(upload_to='teachers/profiles/', blank=True, null=True, verbose_name="Profile Photo")

    # Status/Audit
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate full_name (e.g., "Ackerman, Mikasa Armin")
        self.full_name = f"{self.last_name}, {self.first_name} {self.middle_name}".strip()
        # Auto-compute age from DOB
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)
    
    # @property
    # def age(self):
    #     if self.date_of_birth:
    #         today = date.today()
    #         age = today.year - self.date_of_birth.year - (
    #             (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
    #         )
    #         return age
    #     return None

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        indexes = [models.Index(fields=['last_name', 'first_name'])]  # For search


class ChangeHistory(models.Model):
    """
    Audit log for teacher changes (e.g., "Record Created", "Updated Profile").
    Populates modal's Change History table.
    """
    ACTION_CHOICES = [
        ('created', 'Record Created'),
        ('updated', 'Profile Updated'),
        ('role_changed', 'Role Changed'),
        ('deactivated', 'Deactivated'),
        ('reactivated', 'Reactivated'),
        # Add more as needed
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='change_history', verbose_name="Teacher")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Action")
    description = models.TextField(blank=True, help_text="Details of the change (e.g., 'Email updated to new@deped.gov.ph')")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    time = models.TimeField(auto_now_add=True, verbose_name="Time")

    def __str__(self):
        return f"{self.get_action_display()} - {self.teacher.full_name} ({self.date})"

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Change History"
        verbose_name_plural = "Change Histories"

class AddUserLog(models.Model):
    """
    Specific log for user addition activities (e.g., "Created a New User Account" in settings.html History Logs).
    Includes details of the added user for auditing without needing to join to User/Teacher models.
    """
    # Who performed the action (admin/user)
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='add_user_logs', verbose_name="Admin/User Who Added")
    
    # Action details
    action = models.CharField(max_length=100, verbose_name="Activity")  # e.g., "Created a New User Account"
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    time = models.TimeField(auto_now_add=True, verbose_name="Time")
    description = models.TextField(blank=True, verbose_name="Additional Description")
    
    # Details of the AFFECTED/NEW user (populated only for add actions)
    affected_first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="New User's First Name")
    affected_last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="New User's Last Name")
    affected_email = models.EmailField(blank=True, null=True, verbose_name="New User's Email")
    affected_employee_id = models.CharField(max_length=20, blank=True, null=True, verbose_name="New User's Employee ID")
    
    # Role access booleans (set True if selected in modal, False otherwise)
    affected_is_admin = models.BooleanField(default=False, verbose_name="New User Has Administrator Access")
    affected_is_staff_expert = models.BooleanField(default=False, verbose_name="New User Has Staff Expert Access")
    affected_is_adviser = models.BooleanField(default=False, verbose_name="New User Has Adviser Access")
    affected_is_teacher = models.BooleanField(default=False, verbose_name="New User Has Teacher Access")

    def __str__(self):
        return f"{self.action} by {self.user.username} on {self.date} (for {self.affected_first_name} {self.affected_last_name})"

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Add User Log"
        verbose_name_plural = "Add User Logs"
        indexes = [models.Index(fields=['user', 'date'])]  # For efficient querying



# Sections
User = get_user_model()

# Choices for programs (matching your tabs)
PROGRAM_CHOICES = [
    ('STE', 'Science Technology and Engineering'),
    ('SPFL', 'Special Program in Foreign Language'),
    ('SPTVL', 'Special Program in Technical Vocational Livelihood'),
    ('TOP5', 'Top 5 Regular Class'),
    ('HETERO', 'Hetero Regular class'),
    ('OHSP', 'Open High School Program'),
    ('SNED', 'Special Needs Education Program'),
]

# Common subjects (expand as needed)
SUBJECT_CHOICES = [
    ('MATHEMATICS', 'Mathematics'),
    ('ENGLISH', 'English'),
    ('SCIENCE', 'Science'),
    ('FILIPINO', 'Filipino'),
    ('ARALING_PANLIPUNAN', 'Araling Panlipunan'),
    ('EDUKASYON_SA_PAGPAPAKATAO', 'Edukasyon sa Pagpapakatao'),
    ('MAPEH', 'MAPEH'),
    ('EDUKASYONG_PANGKABUHAYAN', 'Edukasyong Pangkabuhayan'),
]

class Section(models.Model):
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES, verbose_name="Program")
    name = models.CharField(max_length=100, verbose_name="Section Name")
    adviser = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    building = models.PositiveIntegerField(verbose_name="Building Number")
    room = models.CharField(max_length=10, verbose_name="Room Number")
    current_students = models.PositiveIntegerField(default=0, verbose_name="Current Students")
    max_students = models.PositiveIntegerField(default=40, verbose_name="Max Students")
    avatar = models.ImageField(upload_to='section_avatars/', blank=True, null=True, verbose_name="Section Avatar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['program', 'name']  # Prevent duplicate section names per program
        ordering = ['name']

    def __str__(self):
        return f"{self.program} - {self.name}"

    @property
    def location(self):
        return f"Bldg {self.building} Room {self.room}"

# For the "Add Subject Teacher" modal. Stores per-subject assignments.
class SectionSubjectAssignment(models.Model): 
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, verbose_name="Subject")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_subjects', limit_choices_to={'is_teacher': True}, verbose_name="Teacher")
    day = models.CharField(max_length=10, choices=[('DAILY', 'Daily'), ('MWF', 'MWF'), ('TTH', 'TTH')], verbose_name="Day")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['section', 'subject']  # One teacher per subject per section

    def __str__(self):
        return f"{self.section} - {self.subject} ({self.teacher})"
