

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
    
    def get_full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(filter(None, parts)).strip()

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
        ('History', 'History'),
        # Add more
    ]
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('Full-time', 'Full-time Employee'),
        ('Part-time', 'Part-time Employee'),
        ('Temporary', 'Temporary Worker'),
    ]
    
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='Full-time', verbose_name="Employment Status")
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

# This is for section table
class Section(models.Model):
    program = models.ForeignKey(
    'admin_functionalities.Program',
    on_delete=models.CASCADE,
    related_name='sections'
   )
    name = models.CharField(max_length=255)
    adviser = models.ForeignKey(
        'Teacher',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='adviser_sections'
    )

    max_students = models.PositiveIntegerField()
    current_students = models.PositiveIntegerField(default=0)

    building = models.CharField(max_length=255)
    room = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='section_pics/', null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    # def __str__(self):
    #     return f"{self.name} - {self.program.name}"
    
    def clean(self):
        """
        Validate that current_students doesn't exceed max_students.
        This runs during form validation and model.save(full_clean=True).
        """
        super().clean()
        
        if self.current_students > self.max_students:
            raise ValidationError({
                'current_students': f'Current students ({self.current_students}) cannot exceed maximum capacity ({self.max_students}). '
                                   f'Please increase max_students or remove students from this section.'
            })
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure current_students is never greater than max_students.
        """
        # Auto-correct if somehow exceeded (defensive programming)
        if self.current_students > self.max_students:
            raise ValidationError(
                f"Cannot save: Section {self.name} would exceed capacity "
                f"({self.current_students}/{self.max_students})"
            )
        
        super().save(*args, **kwargs)
    
    def has_available_space(self):
        """Check if section has space for more students."""
        return self.current_students < self.max_students
    
    def available_slots(self):
        """Return number of available slots."""
        return max(0, self.max_students - self.current_students)
    
    def capacity_percentage(self):
        """Return capacity usage as percentage."""
        if self.max_students == 0:
            return 0
        return round((self.current_students / self.max_students) * 100, 1)
    
    def is_full(self):
        """Check if section is at full capacity."""
        return self.current_students >= self.max_students
    
    class Meta:
        ordering = ['name']
        # Add database constraint to enforce capacity
        constraints = [
            models.CheckConstraint(
                check=models.Q(current_students__lte=models.F('max_students')),
                name='current_students_cannot_exceed_max'
            )
        ]
    
    def __str__(self):
        return f"{self.name} - {self.program.name} ({self.current_students}/{self.max_students})"



# For the "Add Subject Teacher" modal. Stores per-subject assignments.
class SectionSubjectAssignment(models.Model): 
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey('admin_functionalities.Subject',on_delete=models.CASCADE,  related_name='section_assignments',verbose_name="Subject")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='assigned_subjects', limit_choices_to={'is_teacher': True}, verbose_name="Teacher")
    day = models.CharField(max_length=10, choices=[('DAILY', 'Daily'), ('MWF', 'MWF'), ('TTH', 'TTH')], verbose_name="Day")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['section', 'subject']  # One teacher per subject per section

    def __str__(self):
        return f"{self.section} - {self.subject} ({self.teacher})"

CustomUser = get_user_model()

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Make these regular methods instead of properties
    def get_date(self):
        return self.timestamp.strftime("%B %d, %Y")
    
    def get_time(self):
        return self.timestamp.strftime("%I:%M %p")
    
    def get_combined_activity(self):
        return f"{self.user.get_full_name()} - {self.action}"
    


# Add this to your existing models.py

class Subject(models.Model):
    """
    Subject model to handle program-specific subjects.
    Each subject belongs to a specific program.
    """
    
    # Basic Information
    subject_code = models.CharField(
        max_length=20,
        verbose_name="Subject Code",
        help_text="Unique code (e.g., MATH7, ENG7, RESEARCH7)"
    )
    
    subject_name = models.CharField(
        max_length=100,
        verbose_name="Subject Name",
        help_text="Name of the subject (e.g., Mathematics, English, Research)"
    )
    
    # Program Association (REQUIRED - each subject belongs to one program)
    program = models.ForeignKey(
        'Program',
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="Program",
        help_text="Program this subject belongs to"
    )
    
    # Display & Other Details
    description = models.TextField(
        blank=True,
        help_text="Optional subject description"
    )
    
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive subjects won't appear in dropdowns"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['program', 'display_order', 'subject_name']
        unique_together = ['program', 'subject_code']  # Unique per program
        indexes = [
            models.Index(fields=['program', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.subject_name} ({self.program.name})"
    
    def get_full_name(self):
        return f"{self.subject_name} - {self.subject_code}"
    
    @classmethod
    def get_subjects_for_program(cls, program):
        """
        Returns active subjects for a given program.
        """
        return cls.objects.filter(
            program=program,
            is_active=True
        ).order_by('display_order', 'subject_name')

class SchoolYear(models.Model):
    """
    Manages school year configuration with flexible quarter date ranges.
    Example: 2025-2026 school year with 4 quarters.
    """
    name = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="School Year",
        help_text="Format: 2025-2026"
    )
    start_date = models.DateField(
        verbose_name="School Year Start Date",
        help_text="First day of classes"
    )
    end_date = models.DateField(
        verbose_name="School Year End Date",
        help_text="Last day of classes"
    )
    
    # Quarter 1
    q1_start = models.DateField(verbose_name="Q1 Start Date")
    q1_end = models.DateField(verbose_name="Q1 End Date")
    
    # Quarter 2
    q2_start = models.DateField(verbose_name="Q2 Start Date")
    q2_end = models.DateField(verbose_name="Q2 End Date")
    
    # Quarter 3
    q3_start = models.DateField(verbose_name="Q3 Start Date")
    q3_end = models.DateField(verbose_name="Q3 End Date")
    
    # Quarter 4
    q4_start = models.DateField(verbose_name="Q4 Start Date")
    q4_end = models.DateField(verbose_name="Q4 End Date")
    
    # Status
    is_current = models.BooleanField(
        default=False,
        verbose_name="Is Current School Year",
        help_text="Only one school year should be current at a time"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "School Year"
        verbose_name_plural = "School Years"
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['is_current', 'is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def clean(self):
        """Validate date ranges"""
        super().clean()
        
        # Check school year dates
        if self.start_date >= self.end_date:
            raise ValidationError("School year end date must be after start date")
        
        # Check quarter dates
        quarters = [
            (self.q1_start, self.q1_end, "Quarter 1"),
            (self.q2_start, self.q2_end, "Quarter 2"),
            (self.q3_start, self.q3_end, "Quarter 3"),
            (self.q4_start, self.q4_end, "Quarter 4"),
        ]
        
        for start, end, name in quarters:
            if start >= end:
                raise ValidationError(f"{name} end date must be after start date")
            if start < self.start_date or end > self.end_date:
                raise ValidationError(f"{name} must be within school year dates")
    
    def save(self, *args, **kwargs):
        """Ensure only one current school year"""
        if self.is_current:
            SchoolYear.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_current(cls):
        """Get the current active school year"""
        return cls.objects.filter(is_current=True, is_active=True).first()
    
    def get_quarter_dates(self, quarter):
        """Get start and end dates for a specific quarter"""
        quarter_map = {
            'Q1': (self.q1_start, self.q1_end),
            'Q2': (self.q2_start, self.q2_end),
            'Q3': (self.q3_start, self.q3_end),
            'Q4': (self.q4_start, self.q4_end),
            '1': (self.q1_start, self.q1_end),
            '2': (self.q2_start, self.q2_end),
            '3': (self.q3_start, self.q3_end),
            '4': (self.q4_start, self.q4_end),
        }
        return quarter_map.get(quarter)
    
    def get_months_in_quarter(self, quarter):
        """Get list of (year, month) tuples for a quarter"""
        start_date, end_date = self.get_quarter_dates(quarter)
        if not start_date or not end_date:
            return []
        
        months = []
        current = start_date.replace(day=1)
        end = end_date.replace(day=1)
        
        while current <= end:
            months.append((current.year, current.month))
            # Move to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        
        return months
    
    def get_quarter_for_date(self, date):
        """Determine which quarter a date falls in"""
        if self.q1_start <= date <= self.q1_end:
            return 'Q1'
        elif self.q2_start <= date <= self.q2_end:
            return 'Q2'
        elif self.q3_start <= date <= self.q3_end:
            return 'Q3'
        elif self.q4_start <= date <= self.q4_end:
            return 'Q4'
        return None
    
# NEW MODEL CLASS
class Program(models.Model):
    """
    Model to manage various educational programs.
    Programs can be added, removed, and modified as needed for different school years.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Program Name")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Optional description of the program.")

    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='programs', verbose_name="School Year")

    is_active = models.BooleanField(default=True, verbose_name="Is Active", help_text="Only active programs will be displayed.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"
        ordering = ['name']

    def __str__(self):
        return self.name

    def deactivate(self):
        """Deactivate the program, making it inactive."""
        self.is_active = False
        self.save()

    def activate(self):
        """Activate the program, making it active for the current school year."""
        self.is_active = True
        self.save()