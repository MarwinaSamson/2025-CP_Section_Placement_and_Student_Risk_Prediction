from django import forms
from .models import StudentRequirements
from django.contrib.auth import get_user_model
from .models import Teacher, AddUserLog, ChangeHistory
from django.core.exceptions import ValidationError




class StudentRequirementsForm(forms.ModelForm):
    class Meta:
        model = StudentRequirements
        fields = [
            'birth_certificate',
            'good_moral',
            'interview_done',
            'reading_assessment_done',
        ]
        widgets = {
            'birth_certificate': forms.CheckboxInput(),
            'good_moral': forms.CheckboxInput(),
            'interview_done': forms.CheckboxInput(),
            'reading_assessment_done': forms.CheckboxInput(),
        }


CustomUser = get_user_model()

class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Temporary Password *", required=True)
    position = forms.ChoiceField(
        choices=[
            ('', 'Select Position'),
            ('Administrative', 'Administrative'),
            ('Staff Administrative', 'Staff Administrative'),
            ('Teacher', 'Teacher'),  # Umbrella – subtypes via checkboxes
        ],
        required=True,
        error_messages={'required': 'Please select a position.'}
    )
    department = forms.ChoiceField(
        choices=[
            ('', 'Select Department'),
            ('English Department', 'English Department'),
            ('Mathematics Department', 'Mathematics Department'),
            ('Filipino Department', 'Filipino Department'),
            ('Science Department', 'Science Department'),
            ('MAPEH Department', 'MAPEH Department'),
            ('ARPAN Department', 'ARPAN Department'),
            ('Values Department', 'Values Department'),
            ('TLE Department', 'TLE Department'),
        ],
        required=False
    )
    # Access checkboxes: Core + subtypes for teachers
    admin_access = forms.BooleanField(required=False, label="Administrative Access")
    staff_expert_access = forms.BooleanField(required=False, label="Staff Administrative Access")
    subject_teacher_access = forms.BooleanField(required=False, label="Subject Teacher Access")
    adviser_access = forms.BooleanField(required=False, label="Adviser Access")

    class Meta:
        model = CustomUser  
        fields = ['first_name', 'last_name', 'email', 'employee_id', 'position', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            # No HiddenInput needed – ChoiceField renders <select>
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # NEW: Pre-set username = email on instance to pass clean() (before validation)
        if self.instance.pk is None and self.data:  # New instance + POST data
            email = self.data.get('email', '').strip()
            if email:
                self.instance.username = email  # Sync for clean()

    def clean_email(self):
        email = self.cleaned_data['email'].strip() if self.cleaned_data.get('email') else ''
        if not email:
            raise ValidationError('Email is required.')
        if CustomUser  .objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with this email already exists.')
        # Sync username again for safety
        self.instance.username = email
        return email

    def clean_position(self):
        position = self.cleaned_data.get('position', '').strip()
        if not position or position == '':
            raise ValidationError('Position is required.')
        return position

    def clean_department(self):
        dept = self.cleaned_data.get('department', '').strip()
        return dept or ''

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        if len(password) < 6:  # Keep 6; or change to 5 for '01111'
            raise ValidationError('Password must be at least 6 characters long.')
        return password

    def save(self, created_by_user=None):
        cleaned_data = self.cleaned_data
        position = cleaned_data['position']
        print(f"=== Admin Creation: Position={position}, Email={cleaned_data['email']} ===")

        # Ensure username synced (manager will override, but safe)
        self.instance.username = cleaned_data['email']

        # Create user with new fields (no personal data yet)
        user = CustomUser  .objects.create_user(
            username=cleaned_data['email'],  # Manager sets it
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            middle_name='',  # Empty for now
            employee_id=cleaned_data.get('employee_id', ''),
            position=position,  # New field
            department=cleaned_data.get('department', ''),
            # Roles: Auto-set based on position + checkboxes
            is_superuser=cleaned_data.get('admin_access', False),
            is_staff=cleaned_data.get('staff_expert_access', False) or cleaned_data.get('admin_access', False),
            is_staff_expert=cleaned_data.get('staff_expert_access', False),
            is_teacher=(position == 'Teacher'),  # Auto for Teacher position
            is_subject_teacher=(position == 'Teacher' and cleaned_data.get('subject_teacher_access', False)),
            is_adviser=(position == 'Teacher' and cleaned_data.get('adviser_access', False)),
            force_password_change=True,  # Always for new users
        )
        user.save()
        print(f"CustomUser   created: {user.email} (Position: {position}, is_teacher: {user.is_teacher}, is_subject_teacher: {user.is_subject_teacher}, is_adviser: {user.is_adviser})")

        # Log (assuming AddUser Log exists)
        
        action = f"Created a New User Account ({position})"
        AddUserLog.objects.create(user=created_by_user or user, action=action)
        print(f"Log created: {action}")

        return {'user': user}
