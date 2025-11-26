from django import forms
from .models import StudentRequirements, Section, SectionSubjectAssignment
from django.contrib.auth import get_user_model
from .models import Teacher, AddUserLog, ChangeHistory, Subject, SchoolYear, Program
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
    admin_access = forms.BooleanField(required=False, label="Administrative Access")
    staff_expert_access = forms.BooleanField(required=False, label="Staff Administrative Access")
    subject_teacher_access = forms.BooleanField(required=False, label="Subject Teacher Access")
    adviser_access = forms.BooleanField(required=False, label="Adviser Access")
    userImage = forms.ImageField(required=False, label="User Image (Optional)", help_text="Upload a profile photo")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 'employee_id', 'position', 'department', 'userImage']  # Added userImage
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'e.g., john_doe'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None and self.data:
            email = self.data.get('email', '').strip()
            if email:
                self.instance.username = email  # Auto-set username from email if needed

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not email:
            raise ValidationError('Email is required.')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if not position:
            raise ValidationError('Position is required.')
        return position

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if username and email and username.lower() == email.lower():
            raise ValidationError("Username cannot be the same as the email address.")
        return cleaned_data

    def save(self, commit=True, created_by_user=None): 
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data.get('admin_access', False)
        user.is_staff_expert = self.cleaned_data.get('staff_expert_access', False)
        user.is_subject_teacher = self.cleaned_data.get('subject_teacher_access', False)
        user.is_adviser = self.cleaned_data.get('adviser_access', False)
        user.set_password(self.cleaned_data['password'])  # Set the temporary password

        if 'userImage' in self.cleaned_data and self.cleaned_data['userImage']:
            user.profile_photo = self.cleaned_data['userImage']

        if commit:
            user.save()
            
            # Create a detailed AddUserLog entry to record who created the user
            if created_by_user:
                AddUserLog.objects.create(
                    user=created_by_user,
                    action=f"Created a New User Account ({user.position})",
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    employee_id=user.employee_id,
                    is_admin=user.is_superuser,
                    is_staff_expert=user.is_staff_expert,
                    is_subject_teacher=user.is_subject_teacher,
                    is_adviser=user.is_adviser
                )

        return user




User = get_user_model()

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'adviser', 'building', 'room', 'max_students', 'avatar']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'sectionName',
                'class': 'form-control',
                'required': True
            }),
            'adviser': forms.Select(attrs={
                'id': 'adviserName',
                'class': 'form-control',
                'required': True
            }),
            'building': forms.Select(
                choices=[
                    (1, 'Building 1'),
                    (2, 'Building 2'),
                    (3, 'Building 3'),
                    (4, 'Building 4'),
                    (5, 'Building 5')
                ],
                attrs={
                    'id': 'buildingNumber',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'room': forms.TextInput(attrs={
                'id': 'roomNumber',
                'class': 'form-control',
                'required': True
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 40
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        exclude = ['program', 'current_students']

    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)

        if program:
            # Allow program access without showing in form
            self.program = program.upper()

        # ✅ FIX 1: Show ALL teachers (not only is_adviser)
        self.fields['adviser'].queryset = Teacher.objects.all().order_by('last_name', 'first_name')

        # ✅ Optional prefill when editing
        if self.instance.pk:
            self.fields['building'].initial = self.instance.building
            self.fields['room'].initial = self.instance.room


class SectionSubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = SectionSubjectAssignment
        fields = ['subject', 'teacher', 'day', 'start_time', 'end_time']
        widgets = {
            'subject': forms.Select(choices=SectionSubjectAssignment._meta.get_field('subject').choices, attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(choices=SectionSubjectAssignment._meta.get_field('day').choices, attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        section = kwargs.pop('section', None)
        super().__init__(*args, **kwargs)
        if section:
            self.instance.section = section
        # Limit teachers to subject teachers (CustomUser)
        self.fields['teacher'].queryset = User.objects.filter(is_subject_teacher=True).order_by('last_name', 'first_name')
        
class SubjectForm(forms.ModelForm):
    """Form for creating/updating subjects"""
    
    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code', 'description', 'display_order']
        widgets = {
            'subject_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Advanced Mathematics'
            }),
            'subject_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., MATH-101'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 0
            }),
        }
    
    def __init__(self, *args, **kwargs):
        # Accept program from the view
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)

        # Make order optional
        self.fields['display_order'].required = False

        # FIX: Set program on instance early, BEFORE validation
        if program:
            self.instance.program = program

    def clean_subject_code(self):
        subject_code = self.cleaned_data.get('subject_code')
        program = self.instance.program  # Program is always set now

        if not program:
            raise forms.ValidationError('Program is required.')

        qs = Subject.objects.filter(
            subject_code=subject_code,
            program=program
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                f'Subject code "{subject_code}" already exists for this program.'
            )

        return subject_code

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Program is already set properly in __init__
        if commit:
            instance.save()

        return instance

    
class ProgramForm(forms.ModelForm):
    """Form for creating and updating programs."""
    
    class Meta:
        model = Program
        fields = ['name', 'description', 'school_year', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., STE, SPFL, SPTVE'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Optional description of the program',
                'rows': 3
            }),
            'school_year': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active school years in dropdown
        self.fields['school_year'].queryset = SchoolYear.objects.filter(is_active=True)
        
        # Set default to current active school year if creating new
        if not self.instance.pk:
            current_sy = SchoolYear.objects.filter(is_active=True).first()
            if current_sy:
                self.fields['school_year'].initial = current_sy
    
    def clean_name(self):
        """Validate program name to be uppercase and unique."""
        name = self.cleaned_data.get('name', '').strip().upper()
        
        if not name:
            raise forms.ValidationError("Program name is required.")
        
        # Check for duplicates (excluding current instance if updating)
        existing = Program.objects.filter(name=name)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError(f"Program '{name}' already exists.")
        
        return name