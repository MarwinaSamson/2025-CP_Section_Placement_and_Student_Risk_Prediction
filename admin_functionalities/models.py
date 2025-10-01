from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from enrollmentprocess.models import Student



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name='', last_name='', middle_name='', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, first_name='', last_name='', middle_name='', **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)  # Required for admin permissions

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, email, password, first_name, last_name, middle_name, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)  # Required for admin permissions

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return full_name if full_name else self.username


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