from django import forms
from .models import StudentRequirements
from django.contrib.auth import get_user_model
from .models import Teacher, AddUserLog, ChangeHistory



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

CustomUser = get_user_model()  # Gets your CustomUser

class AddUserForm(forms.Form):
    """
    Form for adding users via modal. Creates CustomUser + optional Teacher + AddUserLog.
    """
    # User fields
    first_name = forms.CharField(max_length=30, label="First Name", required=True)
    last_name = forms.CharField(max_length=30, label="Last Name", required=True)
    email = forms.EmailField(label="Email Address", required=True)
    password = forms.CharField(  # Renamed from temp_password
        widget=forms.PasswordInput,
        label="Password *",
        required=True,
        help_text="Admin-provided password. User must change it on first login."
    )
    employee_id = forms.CharField(max_length=20, required=False, label="Employee ID")
    position = forms.ChoiceField(
        choices=[
            ('', 'Select Position'),
            ('Administrator', 'Administrator'),
            ('Subject Teacher', 'Subject Teacher'),
            ('Class Adviser', 'Class Adviser'),
            ('Staff', 'Staff'),
        ],
        label="Position",
        required=True
    )
    department = forms.ChoiceField(
        choices=[
            ('', 'Select Department'),
            ('STE', 'STE'),
            ('SPFL', 'SPFL'),
            ('SPTVE', 'SPTVE'),
            ('Regular', 'Regular'),
        ],
        required=False,
        label="Department"
    )
    user_image = forms.ImageField(required=False, label="User Image")

    # Permissions (checkboxes)
    admin_access = forms.BooleanField(required=False, label="Administrator Access")
    staff_expert_access = forms.BooleanField(required=False, label="Staff Expert Access")
    adviser_access = forms.BooleanField(required=False, label="Adviser Access")
    teacher_access = forms.BooleanField(required=False, label="Teacher Access")

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(username=email).exists():  # username = email
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_employee_id(self):
        emp_id = self.cleaned_data['employee_id']
        if emp_id and Teacher.objects.filter(employee_id=emp_id).exists():
            raise forms.ValidationError("Employee ID already in use.")
        return emp_id

    def save(self, created_by_user=None):
        cleaned_data = self.cleaned_data
        # Create CustomUser (username = email, password hashed automatically)
        user = CustomUser.objects.create_user(
            username=cleaned_data['email'],
            email=cleaned_data['email'],
            password=cleaned_data['password'],  # Plain text → hashed via set_password()
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            middle_name='',  # Not in modal
            is_staff=cleaned_data['admin_access'] or cleaned_data['staff_expert_access'],
            is_superuser=cleaned_data['admin_access'],
            is_active=True
        )
        user.save()

        # Force password change on first login
        user.force_password_change = True
        user.save(update_fields=['force_password_change'])

        teacher = None
        position = cleaned_data['position']
        # Create Teacher if teacher-related position
        if position in ['Subject Teacher', 'Class Adviser']:
            teacher = Teacher.objects.create(
                user=user,
                employee_id=cleaned_data['employee_id'] or '',
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name'],
                middle_name='',
                email=cleaned_data['email'],
                position=position,
                department=cleaned_data['department'] or '',
                is_subject_teacher=(position == 'Subject Teacher' or cleaned_data['teacher_access']),
                is_adviser=(position == 'Class Adviser' or cleaned_data['adviser_access']),
                profile_photo=cleaned_data.get('user_image'),
                # Other fields blank: gender, DOB, phone, address
            )
            # Log to ChangeHistory
            ChangeHistory.objects.create(
                teacher=teacher,
                action='created',
                description=f'Created by admin {created_by_user.username if created_by_user else "Unknown"}'
            )

        # Log to AddUserLog with role booleans
        AddUserLog.objects.create(
            user=created_by_user,  # Admin who added
            action=f"Created a New User Account ({position})",
            description=f'Added by admin {created_by_user.username if created_by_user else "Unknown"}',
            affected_first_name=user.first_name,
            affected_last_name=user.last_name,
            affected_email=user.email,
            affected_employee_id=cleaned_data['employee_id'] or '',
            affected_is_admin=cleaned_data['admin_access'],
            affected_is_staff_expert=cleaned_data['staff_expert_access'],
            affected_is_adviser=cleaned_data['adviser_access'],
            affected_is_teacher=cleaned_data['teacher_access']
        )

        return {'user': user, 'teacher': teacher}
