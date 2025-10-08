# admin_functionalities/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.middleware.csrf import get_token
from django.db import transaction
from django.db.models import Prefetch, Count
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView

# App-specific imports
from .models import Notification, StudentRequirements, CustomUser , AddUserLog, Teacher
from .forms import AddUserForm, StudentRequirementsForm

from enrollmentprocess.models import (
    Student,
    Family,
    StudentNonAcademic,
    StudentAcademic,
    SectionPlacement,
)

from enrollmentprocess.forms import (
    StudentForm,
    FamilyForm,
    StudentNonAcademicForm,
    StudentAcademicForm,
    SectionPlacementForm,
)

# Standard library
import json
from django.http import JsonResponse



# NEW: Generic helper (unchanged)
def get_or_create_related(model, student, defaults=None):
    """Generic helper: Get or create related instance."""
    if defaults is None:
        defaults = {}
    try:
        instance, created = model.objects.get_or_create(student=student, defaults=defaults)
        return instance
    except Exception as e:
        print(f"Error in get_or_create for {model.__name__}: {e}")  # Temp debug
        return model(student=student)  # Fallback empty instance

# UPDATED: Family helper (based on FamilyForm fields)
def get_family_or_create(student):
    return get_or_create_related(Family, student, defaults={
        # Father fields
        'father_family_name': '',
        'father_first_name': '',
        'father_middle_name': '',
        'father_age': 0,
        'father_occupation': '',
        'father_dob': None,
        'father_contact_number': '',
        'father_email': '',
        
        # Mother fields
        'mother_family_name': '',
        'mother_first_name': '',
        'mother_middle_name': '',
        'mother_age': 0,
        'mother_occupation': '',
        'mother_dob': None,
        'mother_contact_number': '',
        'mother_email': '',
        
        # Guardian fields
        'guardian_family_name': '',
        'guardian_first_name': '',
        'guardian_middle_name': '',
        'guardian_age': 0,
        'guardian_occupation': '',
        'guardian_dob': None,
        'guardian_address': '',
        'guardian_relationship': '',
        'guardian_contact_number': '',
        'guardian_email': '',
        
        # File field
        'parent_photo': None,
        
        # Any other Family fields (e.g., if you have more like 'student_address' or relations, add here)
    })

CustomUser = get_user_model()

# UPDATED: StudentNonAcademic helper (based on StudentNonAcademicForm fields; 'other' fields processed in form clean)
def get_non_academic_or_create(student):
    return get_or_create_related(StudentNonAcademic, student, defaults={
        # Choice/Radio fields (use '' as default; form choices will handle)
        'study_hours': '',  # e.g., 'less_than_1'
        'study_place': '',  # Comma-separated after clean (e.g., 'Bedroom,Library')
        'study_with': '',   # e.g., 'never'
        'live_with': '',    # Comma-separated (e.g., 'Parents,Siblings')
        'parent_help': '',  # e.g., 'never'
        'highest_education': '',  # e.g., 'Did not finish high school'
        'marital_status': '',     # e.g., 'Married'
        'house_type': '',         # e.g., 'Apartment'
        'quiet_place': '',        # e.g., 'Yes'
        'study_area': '',         # e.g., 'Very_quiet'
        'transport_mode': '',     # e.g., 'Walk'
        'travel_time': '',        # e.g., 'Less than 15 minutes'
        'access_resources': '',   # Comma-separated (e.g., 'books & materials,Internet')
        'computer_use': '',       # e.g., 'Never'
        'confidence_level': '',   # e.g., 'Very_confident'
        
        # Text fields
        'hobbies': '',
        'personality_traits': '',  # Comma-separated (e.g., 'shy,outgoing')
        
        # Any other fields (e.g., if model has more like 'internet_access', add here)
    })

# UPDATED: StudentAcademic helper (based on StudentAcademicForm fields; grades default to 0.0, overall_average computed)
def get_academic_or_create(student):
    return get_or_create_related(StudentAcademic, student, defaults={
        # Copied from student
        'lrn': student.lrn if hasattr(student, 'lrn') else '',
        
        # Choice/Select fields
        'dost_exam_result': '',  # e.g., 'passed'
        
        # File field
        'report_card': None,
        
        # Grade fields (NumberInput, default 0.0; form clean validates 75-100 on edit)
        'mathematics': 0.0,
        'araling_panlipunan': 0.0,
        'english': 0.0,
        'edukasyon_pagpapakatao': 0.0,
        'science': 0.0,
        'edukasyon_pangkabuhayan': 0.0,
        'filipino': 0.0,
        'mapeh': 0.0,
        
        # Checkbox
        'agreed_to_terms': False,
        
        # Computed (not in defaults; set in form clean)
        # 'overall_average': 0.0,  # Handled in StudentAcademicForm.clean()
        
        # Any other fields (e.g., if model has 'is_working_student' or 'work_type', add: 'is_working_student': False, 'work_type': '')
    })

# UPDATED: SectionPlacement helper (based on SectionPlacementForm fields; placement_date auto-set in view)
def get_placement_or_create(student):
       try:
           # Try get first (assumes unique, but if multiples, take latest)
           placement = SectionPlacement.objects.filter(student=student).latest('id')  # Or .order_by('-created_at')
        #    print(f"DEBUG: Found existing placement {placement.id} for student {student.id}")
           return placement
       except SectionPlacement.DoesNotExist:
           pass
       
       # Create if none
       placement = SectionPlacement.objects.create(
           student=student,
           status='pending',
           selected_program='regular'  # Defaults
       )
       print(f"DEBUG: Created new placement {placement.id} for student {student.id}")
       return placement
   
   # Do similar for other helpers (get_family_or_create, etc.) if they error too.
   

   # NEW: Main edit view for modal (add this function)

@login_required
@require_http_methods(["GET", "POST"])
def student_edit_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if not request.user.is_staff:
        messages.error(request, 'Access denied: Admin only.')
        return render(request, 'admin_functionalities/error.html', {'error': 'Permission denied.'})

    # get or create requirements record
    requirements, _ = StudentRequirements.objects.get_or_create(student=student)

    if request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES, instance=student, user=request.user)
        family_form = FamilyForm(request.POST, request.FILES, instance=get_family_or_create(student), user=request.user)
        non_academic_form = StudentNonAcademicForm(request.POST, instance=get_non_academic_or_create(student), user=request.user)
        academic_form = StudentAcademicForm(request.POST, request.FILES, instance=get_academic_or_create(student), user=request.user)
        placement_form = SectionPlacementForm(request.POST, instance=get_placement_or_create(student), user=request.user)
        requirements_form = StudentRequirementsForm(request.POST, instance=requirements)

        if all(form.is_valid() for form in [student_form, family_form, non_academic_form, academic_form, placement_form, requirements_form]):
            try:
                with transaction.atomic():
                    student_form.save()
                    family_form.save()
                    non_academic_form.save()
                    academic_form.save()
                    placement_form.save()
                    requirements_form.save()
                messages.success(request, f"Student {student.first_name} {student.last_name} updated successfully!")
                return redirect("admin_functionalities:student_edit", student_id=student.id)
            except Exception as e:
                messages.error(request, f"Error saving data: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        student_form = StudentForm(instance=student, user=request.user)
        family_form = FamilyForm(instance=get_family_or_create(student), user=request.user)
        non_academic_form = StudentNonAcademicForm(instance=get_non_academic_or_create(student), user=request.user)
        academic_form = StudentAcademicForm(instance=get_academic_or_create(student), user=request.user)
        placement_form = SectionPlacementForm(instance=get_placement_or_create(student), user=request.user)
        requirements_form = StudentRequirementsForm(instance=requirements)

    context = {
        "student": student,
        "student_form": student_form,
        "family_form": family_form,
        "non_academic_form": non_academic_form,
        "academic_form": academic_form,
        "placement_form": placement_form,
        "requirements_form": requirements_form,
        "is_admin": request.user.is_staff,
    }
    return render(request, "admin_functionalities/student_edit.html", context)

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_functionalities:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_functionalities:dashboard')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'admin_functionalities/login.html', context)
    else:
        return render(request, 'admin_functionalities/login.html')
    
@login_required
def custom_logout(request):
    # Fix: Use username directly (avoids get_full_name() error)
    admin_name = request.user.username
    
    last_login = request.user.last_login  # Assumes your CustomUser  has this field
    # Example session duration placeholder; replace with real calculation if needed
    session_duration = "2h 0m"
    
    logout(request)  # Log out the user (clears session)
    
    context = {
        'admin_name': admin_name,
        'last_login': last_login,
        'session_duration': session_duration,
    }
    return render(request, 'admin_functionalities/logout.html', context)

@login_required
def admin_dashboard(request):
    # Debug prints (remove after fixing)
    print("\n=== DEBUG: Complete Students Check ===")
    total_students = Student.objects.count()
    print(f"Total Students: {total_students}")

    # Check partial completions
    with_family = Student.objects.filter(family_data__isnull=False).count()
    print(f"With Family Form: {with_family}")

    with_academic = Student.objects.filter(studentacademic__isnull=False).count()
    print(f"With Academic Form: {with_academic}")

    with_non_academic = Student.objects.filter(studentnonacademic__isnull=False).count()
    print(f"With Non-Academic Form: {with_non_academic}")

    with_program_model = Student.objects.filter(section_placements__isnull=False).count()
    print(f"With Program (SectionPlacement Model): {with_program_model}")

    with_program_field = Student.objects.filter(section_placement__isnull=False).count()
    print(f"With Program (section_placement CharField): {with_program_field}")

    # OPTION 1: Complete = All forms + SectionPlacement model (strict, for placed students)
    complete_students_model = Student.objects.filter(
        family_data__isnull=False,  # Family form filled
        studentacademic__isnull=False,  # Academic form filled
        studentnonacademic__isnull=False,  # Non-academic form filled
        section_placements__isnull=False  # Program chosen (via model)
    ).prefetch_related(
        Prefetch('studentacademic'),
        Prefetch('studentnonacademic'),
        Prefetch('section_placements', queryset=SectionPlacement.objects.order_by('-placement_date'))
    ).order_by('-section_placements__placement_date')[:50]  # Newest first, limit 50

    complete_count_model = complete_students_model.count()
    print(f"Complete (Using Model): {complete_count_model}")

    # OPTION 2: Complete = All forms + section_placement CharField (if no separate model used)
    complete_students_field = Student.objects.filter(
        family_data__isnull=False,  # Family form filled
        studentacademic__isnull=False,  # Academic form filled
        studentnonacademic__isnull=False,  # Non-academic form filled
        section_placement__isnull=False  # Program chosen (via CharField)
    ).prefetch_related(
        Prefetch('studentacademic'),
        Prefetch('studentnonacademic')
    ).order_by('-id')[:50]  # Order by ID (newest), limit 50

    complete_count_field = complete_students_field.count()
    print(f"Complete (Using CharField): {complete_count_field}")
 
 # NEW: Program mapping for friendly names
    PROGRAM_DISPLAY_NAMES = {
        'ste': 'STE program',
        'spfl': 'SPFL program',
        'sptve': 'SPTVE program',
        'sned': 'SNED program',
        'top5': 'TOP 5 Regular class',  # Matches your example
        'regular': 'Regular class',
        # Add more as needed, e.g., 'top5': 'TOP 5 Section'
    }
    
    unread_enrollments = Notification.objects.filter(
        notification_type='student_enrollment',
        is_read=False
    ).values('program').annotate(count=Count('id')).order_by('-count')
    
    notifications = []
    for item in unread_enrollments:
        program_code = item['program'].lower()  # Normalize to lowercase for mapping
        count = item['count']
        
        # Get friendly display name (fallback to "program" if not mapped)
        display_name = PROGRAM_DISPLAY_NAMES.get(program_code, f"{program_code.upper()} program")
        
        # Get sample message (latest student) – Use __iexact for case-insensitivity
        latest_notif = Notification.objects.filter(
            program__iexact=program_code,  # FIXED: Case-insensitive
            is_read=False
        ).order_by('-created_at').first()
        
        # Get IDs – Use __iexact
        notification_ids = list(Notification.objects.filter(
            program__iexact=program_code,  # FIXED: Case-insensitive
            is_read=False
        ).values_list('id', flat=True))
        
        notifications.append({
            'title': 'New Enrollment Requests',
            'message': f'{count} new enrollment request{"s" if count > 1 else ""} for {display_name}',
            'type': 'student_enrollment',
            'program': program_code,
            'display_program': display_name,
            'count': count,
            'icon': 'fas fa-user-plus',
            'sample_message': latest_notif.message if latest_notif else '',
            'notification_ids': notification_ids,  # List for join in template
            'program_slug': program_code,  # NEW/FIXED: Add this for data-program-slug (e.g., 'ste')
        })
    
    total_unread = sum(item['count'] for item in unread_enrollments)

    
    context = {
        'total_students': total_students,
        'complete_students': complete_students_model,  # Change to complete_students_field if needed
        'complete_count': complete_count_model,  # For template display
         'notifications': notifications,
        'total_unread': total_unread,
    }

    print("=== END DEBUG ===\n")
    return render(request, 'admin_functionalities/admin-dashboard.html', context)


@login_required
def sections_view(request):
    # Add context if needed
    return render(request, 'admin_functionalities/sections.html', {'active_page': 'sections'})

@login_required
def enrollment_view(request):
    # Get filters from URL params
    program_filter = request.GET.get('program', None)  # e.g., 'ste' or None (all)
    status_filter = request.GET.get('status', 'pending')  # Default pending; can expand later
    
    # Base query: All enrollments (not just pending – for full filtering)
    queryset = SectionPlacement.objects.select_related('student').order_by('-id')  # Or '-placement_date'
    
    # Apply program filter if specified
    if program_filter:
        queryset = queryset.filter(selected_program__iexact=program_filter)
    
    # Apply status filter (for future; now defaults to pending but passes all for JS)
    if status_filter != 'all':
        queryset = queryset.filter(status=status_filter)
    
    # Fetch data as list of dicts for template
    enrollments = list(queryset.values(
        'id',
        'student__id',
        'student__lrn',
        'student__first_name',
        'student__middle_name',
        'student__last_name',
        'selected_program',
        'status',  # For data-status
        'placement_date'  # Or 'placement_date' if exists
    ))
    
    # Stats (overall across all programs; adjust to filtered if needed)
    total_requests = SectionPlacement.objects.count()
    approved = SectionPlacement.objects.filter(status='approved').count()
    pending = SectionPlacement.objects.filter(status='pending').count()
    rejected = SectionPlacement.objects.filter(status='rejected').count()
    
    # Program display mapping
    PROGRAM_DISPLAY_NAMES = {
        'ste': 'STE',
        'spfl': 'SPFL',
        'sptve': 'SPTVE',
        'top5': 'TOP 5',
        'hetero': 'HETERO',  # Assuming 'hetero' for regular/hetero
        'ohsp': 'OHSP',
        'regular': 'Regular',
        # Add more as needed
    }
    display_name = PROGRAM_DISPLAY_NAMES.get(program_filter.lower() if program_filter else None, 'All Programs')
    is_filtered = bool(program_filter)
    
    context = {
        'enrollments': enrollments,
        'total_requests': total_requests,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'program_filter': program_filter or 'all',
        'status_filter': status_filter,
        'display_name': display_name,
        'is_filtered': is_filtered,
    }
    return render(request, 'admin_functionalities/enrollment-management.html', context)



def teachers_view(request):
    # Add context if needed
    return render(request, 'admin_functionalities/teachers.html')

@csrf_exempt
def mark_notification_read(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            if ids:
                Notification.objects.filter(id__in=ids).update(is_read=True)
                return JsonResponse({'success': True, 'marked': len(ids)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=400)


# NEW VIEWS SEPARATED
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class StudentAcademicUpdateView(AdminRequiredMixin, UpdateView):
    model = StudentAcademic
    form_class = StudentAcademicForm
    template_name = 'enrollmentprocess/studentAcademic.html'  # reuse same template

    def get_object(self, queryset=None):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        return get_object_or_404(StudentAcademic, student=student)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form for permissions
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form = context['form']

        # Pre-fill LRN and lock it
        form.fields['lrn'].initial = student.lrn
        form.fields['lrn'].widget.attrs['readonly'] = True

        # Pass student info to template
        context['student_id'] = self.kwargs['student_id']
        context['is_working_student'] = "YES" if student.is_working_student else "NO"
        context['working_details'] = student.working_details or "N/A"
        context['is_pwd'] = "YES" if student.is_sped else "NO"
        context['disability_type'] = student.sped_details or "N/A"
        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student

        # Enforce values from Student model
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped
        form.instance.disability_type = student.sped_details if student.is_sped else None

        # Ensure LRN matches
        if form.cleaned_data['lrn'] != student.lrn:
            form.add_error('lrn', "LRN does not match the student's record.")
            return self.form_invalid(form)

        # Compute overall average if applicable
        form.instance.overall_average = form.cleaned_data.get('overall_average', 0.0)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')  # or wherever admin should go after editing


# ALL SETTINGS RELATED VIEWS ARE HERE
@method_decorator(login_required, name='dispatch')
# class AddUserView(View):
#       def get(self, request):  # NEW: Handle GET (if direct access to /add-user/, redirect to settings)
#         return redirect('admin_functionalities:settings')

#       def post(self, request):
#         print(f"=== DEBUG: POST received in AddUser View! Raw POST data: {dict(request.POST)} ===")  # KEY: Shows all form data (e.g., position='Administrative')
#         print(f"=== DEBUG: FILES present: {bool(request.FILES)} (userImage: {request.FILES.get('userImage', 'None')}) ===")  # Check file if needed

#         form = AddUserForm(request.POST, request.FILES)  # Process form
#         print(f"=== DEBUG: Form errors: {form.errors} ===")  # KEY: Exact validation errors (e.g., {'position': ['This field is required.']})
#         print(f"=== DEBUG: Form cleaned_data (if partial): {form.cleaned_data} ===")  # Shows valid fields

#         if form.is_valid():
#             print("=== DEBUG: Form VALID – Saving user... ===")
#             try:
#                 result = form.save(created_by_user=request.user)
#                 print(f"=== DEBUG: SUCCESS – User created! ID={result['user'].id}, Position={result['user'].position}, Roles: is_teacher={result['user'].is_teacher}, is_subject_teacher={result['user'].is_subject_teacher}, is_adviser={result['user'].is_adviser} ===")
#                 messages.success(request, 'User  added successfully! Please refresh the page to see the new user.')
#                 return redirect('admin_functionalities:settings')  # Redirect to settings (reloads table, closes modal implicitly)
#             except Exception as save_err:
#                 print(f"=== DEBUG: Save ERROR: {save_err} ===")
#                 messages.error(request, f'Error saving user: {str(save_err)}')
#                 return redirect('admin_functionalities:settings')
#         else:
#             print("=== DEBUG: Form INVALID – Redirecting with errors ===")
#             # For regular form, show errors via messages (terminal + browser flash)
#             error_msg = 'Please correct the form errors (check terminal for details).'
#             for field, errs in form.errors.items():
#                 error_msg += f' {field}: {", ".join(errs)}'
#             messages.error(request, error_msg)
#             # Re-fetch context for redirect
#             users = CustomUser .objects.filter(is_active=True).order_by('-id')[:20]
#             logs = AddUserLog.objects.select_related('user').order_by('-date', '-time')[:20]
#             context = {
#                 'active_page': 'settings',
#                 'users': users,
#                 'logs': logs,
#                 'form': form,  # Pass form (errors bound; but modal needs JS to show – terminal has details)
#             }
#             return render(request, 'admin_functionalities/settings.html', context) 
class AddUserView(View):
    def get(self, request):  # Handle direct GET (redirect to settings)
        return redirect('admin_functionalities:settings')

    def post(self, request):
        print(f"=== DEBUG: POST received in AddUser  View! Raw POST data: {dict(request.POST)} ===")
        print(f"=== DEBUG: FILES present: {bool(request.FILES)} (userImage: {request.FILES.get('userImage', 'None')}) ===")

        form = AddUserForm(request.POST, request.FILES)
        print(f"=== DEBUG: Form errors: {form.errors} ===")
        print(f"=== DEBUG: Form cleaned_data (if partial): {form.cleaned_data} ===")

        if form.is_valid():
            print("=== DEBUG: Form VALID – Saving user... ===")
            try:
                result = form.save(created_by_user=request.user)
                print(f"=== DEBUG: SUCCESS – User created! ID={result['user'].id}, Position={result['user'].position}, Roles: is_teacher={result['user'].is_teacher}, is_subject_teacher={result['user'].is_subject_teacher}, is_adviser={result['user'].is_adviser} ===")
                # JSON for AJAX: Success + data for JS (e.g., reload table)
                return JsonResponse({
                    'success': True, 
                    'message': 'User  added successfully!', 
                    'user_id': result['user'].id,
                    'position': result['user'].position  # Optional for JS
                })
            except Exception as save_err:
                print(f"=== DEBUG: Save ERROR: {save_err} ===")
                return JsonResponse({'success': False, 'error': str(save_err)}, status=500)
        else:
            print("=== DEBUG: Form INVALID – Returning JSON errors ===")
            # JSON for AJAX: Errors dict (JS can show field-specific alerts)
            return JsonResponse({
                'success': False, 
                'errors': form.errors,  # e.g., {'password': ['Must be 8+ chars'], '__all__': ['Username mismatch']}
                'message': 'Please correct the errors below.'
            }, status=400)


@login_required
def settings_view(request):
    # Dynamic context for tables
    users = CustomUser .objects.filter(is_active=True).order_by('-id')[:20]  # Last 20 active users
    logs = AddUserLog.objects.select_related('user').order_by('-date', '-time')[:20]  # Last 20 logs
    context = {
        'active_page': 'settings',
        'users': users,
        'logs': logs,
    }
    return render(request, 'admin_functionalities/settings.html', context)

@login_required
def get_user_profile(request, user_id):
    try:
        user = CustomUser .objects.get(id=user_id, is_active=True)
        teacher = getattr(user, 'teacher_profile', None)  # None OK

        profile_data = {
            'full_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'employee_id': user.employee_id or 'Not provided',
            'position': user.position or 'Not specified',
            'department': user.department or 'Not provided',
            'profile_photo': (teacher.profile_photo.url if teacher and teacher.profile_photo else None),
            'date_of_birth': (teacher.date_of_birth.strftime('%B %d, %Y') if teacher and teacher.date_of_birth else 'Not provided – Update your profile'),
            'gender': (teacher.gender if teacher else 'Not provided – Update your profile'),
            'phone_number': (teacher.phone if teacher and teacher.phone else user.phone_number or 'Not provided – Update your profile'),  # Fallback if added to CustomUser  later
            'address': (teacher.address if teacher and teacher.address else user.address or 'Not provided – Update your profile'),  # Same
            'age': (teacher.age if teacher and teacher.age else 'Not provided – Update your profile'),
            'is_subject_teacher': user.is_subject_teacher,  # NEW: Direct from model
            'is_adviser': user.is_adviser,  # NEW
            'roles_summary': f"Subject Teacher: {'Yes' if user.is_subject_teacher else 'No'} | Adviser: {'Yes' if user.is_adviser else 'No'}" if user.is_teacher else 'N/A (Non-Teacher Role)',  # NEW: For modal
            'subjects_taught': (teacher.subjects_taught if teacher else 'To be assigned – Update your profile'),
            'classes_handled': (teacher.classes_handled if teacher else 'To be assigned – Update your profile'),
            'change_history': list(AddUserLog.objects.filter(user=user).values('action', 'date', 'time')[:3]) or [
                {'action': 'Account Created', 'date': user.date_joined.strftime('%m/%d/%Y'), 'time': user.date_joined.strftime('%I:%M %p')}
            ],
        }
        return JsonResponse({'success': True, 'data': profile_data})
    except CustomUser .DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User  not found'}, status=404)
