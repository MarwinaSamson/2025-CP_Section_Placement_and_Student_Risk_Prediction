# admin_functionalities/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.middleware.csrf import get_token
from django.db import transaction, models
from django.db.models import Prefetch, Count
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie

# App-specific imports
from .models import Notification, StudentRequirements, CustomUser , AddUserLog, Section, SectionSubjectAssignment , Teacher
from .forms import AddUserForm, StudentRequirementsForm, SectionForm, SectionSubjectAssignmentForm
from admin_functionalities.services import SectionAssignmentService

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
import logging



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

logger = logging.getLogger(__name__)
@login_required
@require_http_methods(["GET", "POST"])
def student_edit_view(request, student_id):
    """
    Edit student details and auto-assign to section upon save.
    
    Flow:
    1. Admin reviews/edits all student details
    2. Admin clicks "Save All Changes"
    3. All forms validated and saved
    4. System automatically assigns student to a section based on:
       - Selected program (from SectionPlacementForm)
       - Academic merit (overall average)
       - Section availability and current load
    5. Success message shows assigned section
    """
    student = get_object_or_404(Student, id=student_id)

    if not request.user.is_staff:
        messages.error(request, 'Access denied: Admin only.')
        return render(request, 'admin_functionalities/error.html', {'error': 'Permission denied.'})

    # Get or create requirements record
    requirements, _ = StudentRequirements.objects.get_or_create(student=student)

    if request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES, instance=student, user=request.user)
        family_form = FamilyForm(request.POST, request.FILES, instance=get_family_or_create(student), user=request.user)
        non_academic_form = StudentNonAcademicForm(request.POST, instance=get_non_academic_or_create(student), user=request.user)
        academic_form = StudentAcademicForm(request.POST, request.FILES, instance=get_academic_or_create(student), user=request.user)
        placement_form = SectionPlacementForm(request.POST, instance=get_placement_or_create(student), user=request.user)
        requirements_form = StudentRequirementsForm(request.POST, instance=requirements)

        # A small helper: collect requirement fields that are unchecked
        def get_missing_requirements(req_cleaned):
            missing = []
            # names here match fields in StudentRequirementsForm
            for fname, friendly in [
                ('birth_certificate', 'Birth Certificate'),
                ('good_moral', 'Good Moral Certificate'),
                ('interview_done', 'Interview'),
                ('reading_assessment_done', 'Reading Assessment'),
            ]:
                if not req_cleaned.get(fname):
                    missing.append(friendly)
            return missing

        if all(form.is_valid() for form in [student_form, family_form, non_academic_form, academic_form, placement_form, requirements_form]):
            try:
                with transaction.atomic():
                    # Save forms first
                    student_form.save()
                    family_form.save()
                    non_academic_form.save()
                    academic_form.save()
                    placement_form.save()
                    requirements_form.save()

                    # Only auto-assign when status == 'approved'
                    placement_status = placement_form.cleaned_data.get('status', '').lower()
                    selected_program = placement_form.cleaned_data.get('selected_program', '') or ''
                    selected_program = selected_program.upper()

                    # If admin is trying to approve, ensure requirements are OK or admin confirmed override.
                    requirement_confirmed = request.POST.get('confirm_approve_incomplete') == '1'
                    missing_requirements = get_missing_requirements(requirements_form.cleaned_data)

                    if placement_status == 'approved':
                        if missing_requirements and not requirement_confirmed:
                            # Don't assign yet — render page with missing requirements so JS will ask the admin
                            messages.warning(request, f"Student marked as Approved but requirements incomplete.")
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                # flags for template/JS
                                "requirement_missing_list": missing_requirements,
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)

                        # Proceed to assign (either all requirements present OR admin confirmed override)
                        success, assigned_section, msg = SectionAssignmentService.assign_student_to_section(student, selected_program)

                        if success:
                            messages.success(
                                request,
                                f"✓ Student {student.first_name} {student.last_name} updated and assigned to {assigned_section.name} ({selected_program})"
                            )
                        else:
                            # If assignment failed because sections are full, provide contextual info to template
                            messages.warning(request, f"Student updated but section assignment failed: {msg}")
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                "section_assignment_error": msg,  # e.g., "All sections for X are already full"
                                "section_program": selected_program.lower(),
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)
                    else:
                        # Not approved: skip assignment
                        messages.success(request, f"Student {student.first_name} {student.last_name} updated. Section placement skipped (status: {placement_status}).")

                return redirect("admin_functionalities:student_edit", student_id=student.id)

            except Exception as e:
                logger.error(f"Error in student_edit_view for student {student.id}: {str(e)}")
                messages.error(request, f"Error saving data: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            logger.warning(f"Form validation failed for student {student.id}")
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

# @login_required
# @require_http_methods(["GET", "POST"])
# def student_edit_view(request, student_id):
#     student = get_object_or_404(Student, id=student_id)

#     if not request.user.is_staff:
#         messages.error(request, 'Access denied: Admin only.')
#         return render(request, 'admin_functionalities/error.html', {'error': 'Permission denied.'})

#     # get or create requirements record
#     requirements, _ = StudentRequirements.objects.get_or_create(student=student)

#     if request.method == "POST":
#         student_form = StudentForm(request.POST, request.FILES, instance=student, user=request.user)
#         family_form = FamilyForm(request.POST, request.FILES, instance=get_family_or_create(student), user=request.user)
#         non_academic_form = StudentNonAcademicForm(request.POST, instance=get_non_academic_or_create(student), user=request.user)
#         academic_form = StudentAcademicForm(request.POST, request.FILES, instance=get_academic_or_create(student), user=request.user)
#         placement_form = SectionPlacementForm(request.POST, instance=get_placement_or_create(student), user=request.user)
#         requirements_form = StudentRequirementsForm(request.POST, instance=requirements)

#         if all(form.is_valid() for form in [student_form, family_form, non_academic_form, academic_form, placement_form, requirements_form]):
#             try:
#                 with transaction.atomic():
#                     student_form.save()
#                     family_form.save()
#                     non_academic_form.save()
#                     academic_form.save()
#                     placement_form.save()
#                     requirements_form.save()
#                 messages.success(request, f"Student {student.first_name} {student.last_name} updated successfully!")
#                 return redirect("admin_functionalities:student_edit", student_id=student.id)
#             except Exception as e:
#                 messages.error(request, f"Error saving data: {e}")
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         student_form = StudentForm(instance=student, user=request.user)
#         family_form = FamilyForm(instance=get_family_or_create(student), user=request.user)
#         non_academic_form = StudentNonAcademicForm(instance=get_non_academic_or_create(student), user=request.user)
#         academic_form = StudentAcademicForm(instance=get_academic_or_create(student), user=request.user)
#         placement_form = SectionPlacementForm(instance=get_placement_or_create(student), user=request.user)
#         requirements_form = StudentRequirementsForm(instance=requirements)

#     context = {
#         "student": student,
#         "student_form": student_form,
#         "family_form": family_form,
#         "non_academic_form": non_academic_form,
#         "academic_form": academic_form,
#         "placement_form": placement_form,
#         "requirements_form": requirements_form,
#         "is_admin": request.user.is_staff,
#     }
#     return render(request, "admin_functionalities/student_edit.html", context)


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

# ALLVIEWS FOR SECTOIONS ARE HERE
@login_required
def sections_view(request):
    # Get initial program from URL params (e.g., ?program=TOP5)
    program = request.GET.get('program', 'STE')  # Default to STE
    
    # Fetch teachers where is_adviser=true or is_subject_teacher=true
    teachers = CustomUser.objects.filter(
        models.Q(is_adviser=True) | models.Q(is_subject_teacher=True)
    ).order_by('last_name', 'first_name')
    
    teachers_data = []  # Prepare data for the template
    for teacher in teachers:
        full_name = f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name}".strip()
        teachers_data.append({
            'id': teacher.id,
            'name': full_name if full_name else teacher.username,
        })
    
    context = {
        'active_page': 'sections',
        'initial_program': program,  # Pass to JS for initial load if needed
        'teachers': teachers_data,  # Pass the combined teachers for the dropdown
    }
    return render(request, 'admin_functionalities/sections.html', context)

@login_required
@require_http_methods(["GET"])
def get_teachers(request):
    """
    Returns all teachers who can be advisers and subject teachers.
    Includes availability status (if already assigned to a section).
    """
    teachers = Teacher.objects.filter(is_active=True)

    adviser_list = []
    subject_teacher_list = []

    # Get IDs of teachers already assigned as advisers in sections
    assigned_adviser_ids = set(
        Section.objects.exclude(adviser__isnull=True)
        .values_list('adviser_id', flat=True)
    )

    for t in teachers:
        # Adviser candidates
        if t.is_adviser:
            adviser_list.append({
                "id": t.id,
                "name": t.full_name,
                "isAssigned": t.id in assigned_adviser_ids
            })

        # Subject teacher candidates
        if t.is_subject_teacher:
            dept = (t.department or "").strip()
            if dept.lower().endswith("department"):
                dept = dept[:-len("department")].strip()
            subject_teacher_list.append({
                "id": t.id,
                "name": t.full_name,
                "department": dept.capitalize()
            })

    return JsonResponse({
        "advisers": adviser_list,
        "subject_teachers": subject_teacher_list
    })

def get_subject_teachers(request):
    """
    Returns all active subject teachers with cleaned, case-insensitive department names.
    Example: 'English Department' → 'English'
    """
    teachers = Teacher.objects.filter(is_subject_teacher=True, is_active=True)

    teacher_list = []
    for t in teachers:
        dept = (t.department or "").strip()
        # Normalize: remove "department" regardless of case, trim spaces
        if dept.lower().endswith("department"):
            dept = dept[:-len("department")].strip()

        # Capitalize cleanly (e.g., "english" → "English")
        clean_department = dept.capitalize()

        teacher_list.append({
            "id": t.id,
            "name": t.full_name,
            "department": clean_department,
        })

    return JsonResponse({"teachers": teacher_list})

@login_required
@require_http_methods(["GET"])
def get_buildings_rooms(request):
    """
    Returns building/room data for location dropdowns.
    Hardcoded for now; can be moved to DB model later.
    """
    rooms_data = {
        1: ['101', '102', '103', '104', '105'],
        2: ['201', '202', '203', '204', '205'],
        3: ['301', '302', '303', '304', '305'],
        4: ['Lab 1', 'Lab 2', 'Lab 3', 'Lecture 1', 'Lecture 2'],
        5: ['IT-101', 'IT-102', 'IT-201', 'IT-202', 'Server Room'],
    }
    
    return JsonResponse({
        'success': True,
        'rooms': rooms_data
    })


@login_required
@require_http_methods(["GET"])
def get_sections_by_program(request, program):
    try:
        sections = Section.objects.filter(program=program.upper()).select_related('adviser')
        sections_data = []
        for section in sections:
            adviser_name = "No Adviser"
            if section.adviser:
                adviser_name = f"{section.adviser.last_name}, {section.adviser.first_name}".strip()
                if adviser_name == ',':
                    adviser_name = section.adviser.user.username if hasattr(section.adviser, 'user') else adviser_name

            sections_data.append({
                'id': section.id,
                'name': section.name,
                'adviser': adviser_name,
                'adviserId': section.adviser.id if section.adviser else None,
                'building': section.building,
                'room': section.room,
                'location': section.location,
                'students': section.current_students,
                'maxStudents': section.max_students,
                'avatar': section.avatar.url if section.avatar else '/static/admin_functionalities/assets/default_section.png',
            })

        return JsonResponse({'success': True, 'sections': sections_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def add_section(request, program):
    try:
        # Program-specific defaults (can be moved to DB later)
        program_defaults = {
            'STE': 30,
            'SPFL': 30,
            'SPTVL': 30,
            'OHSP': 30,
            'SNED': 30,
            'TOP5': 50,
            'HETERO': 50,
            'REGULAR': 40,  # fallback default
        }

        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)
            section.program = program.upper()

            # If max_students not provided or <=0, use program default
            max_students = form.cleaned_data.get('max_students')
            if not max_students or int(max_students) <= 0:
                section.max_students = program_defaults.get(section.program, 40)

            section.save()
            return JsonResponse({'success': True, 'message': f'Section \"{section.name}\" added successfully to {section.program}!'})
        else:
            return JsonResponse({'success': False, 'message': 'Validation failed', 'errors': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error adding section: {str(e)}'}, status=500)


@login_required
@require_http_methods(["POST"])
def update_section(request, section_id):
    """
    Updates an existing section.
    Expects FormData with: name, adviser, building, room, max_students.
    """
    try:
        section = get_object_or_404(Section, id=section_id)
        form = SectionForm(request.POST, request.FILES, instance=section)
        
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': f'Section "{section.name}" updated successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Validation failed',
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating section: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_section(request, section_id):
    """
    Deletes a section (soft delete if you prefer; hard delete for now).
    """
    try:
        section = get_object_or_404(Section, id=section_id)
        section_name = section.name
        section.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Section "{section_name}" deleted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting section: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_section_students(request, section_id):
    """
    Returns students currently placed in this section (approved).
    """
    try:
        # Assuming SectionPlacement.section FK points to Section
        placements = SectionPlacement.objects.filter(section_id=section_id, status='approved').select_related('student').order_by('student__last_name')
        students = [{
            'id': p.student.id,
            'lrn': p.student.lrn,
            'name': f"{p.student.last_name}, {p.student.first_name} {p.student.middle_name or ''}".strip()
        } for p in placements]
        return JsonResponse({'success': True, 'students': students})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def section_masterlist(request, section_id):
    section = get_object_or_404(Section, pk=section_id)

    # Get all approved students assigned to this section
    students = Student.objects.filter(section_placements__section=section, section_placements__status='approved').select_related('studentacademic')

    total_students = students.count()
    available_slots = section.max_students - total_students
    is_full = total_students >= section.max_students

    context = {
        'section': section,
        'students': students,
        'total_students': total_students,
        'available_slots': available_slots,
        'is_full': is_full,
    }

    return render(request, 'admin_functionalities/masterlist.html', context)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def assign_subject_teachers(request, section_id):
    """Assigns teachers to subjects within a section, validating department and schedule."""
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Section not found.'}, status=404)

    try:
        body = json.loads(request.body)
        assignments = body.get('assignments', [])
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)

    subject_department_map = {
        'MATHEMATICS': 'Mathematics',
        'ENGLISH': 'English',
        'SCIENCE': 'Science',
        'FILIPINO': 'Filipino',
        'ARALING_PANLIPUNAN': 'Social Studies',
        'MAPEH': 'MAPEH',
        'EDUKASYON_SA_PAGPAPAKATAO': 'Values Education',
    }

    created_count = 0
    for a in assignments:
        subject = a.get('subject')
        teacher_id = a.get('teacher_id')
        day = a.get('day')
        start_time = a.get('start_time')
        end_time = a.get('end_time')

        if not (subject and teacher_id and day and start_time and end_time):
            return JsonResponse({'success': False, 'message': 'Missing required fields.'}, status=400)

        # Validate teacher existence
        try:
            teacher = Teacher.objects.get(id=teacher_id, is_active=True)
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'message': f'Teacher with ID {teacher_id} not found.'}, status=404)

        # Validate department match
        required_department = subject_department_map.get(subject)
        if not required_department:
            return JsonResponse({'success': False, 'message': f'Invalid subject: {subject}'}, status=400)

        if teacher.department != required_department:
            return JsonResponse({
                'success': False,
                'message': f'{teacher.full_name} belongs to {teacher.department} department, not {required_department}.'
            }, status=400)

        # Check for schedule conflict
        conflicts = SectionSubjectAssignment.objects.filter(
            teacher=teacher,
            day=day,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(section=section)

        if conflicts.exists():
            conflict_section = conflicts.first().section
            return JsonResponse({
                'success': False,
                'message': f'{teacher.full_name} already has a class ({subject}) in section {conflict_section.name} at that time.'
            }, status=400)

        # Create or update assignment
        assignment, created = SectionSubjectAssignment.objects.update_or_create(
            section=section,
            subject=subject,
            defaults={
                'teacher': teacher.user if teacher.user else None,  # Use linked user if any
                'day': day,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        created_count += 1 if created else 0

    return JsonResponse({
        'success': True,
        'message': f'Successfully assigned {created_count} subject teacher(s).'
    }, status=200)

@login_required
def enrollment_view(request):
    """
    Enrollment management view with proper filtering for both program and status.
    Supports all combinations:
    - All programs + All statuses
    - Specific program + All statuses
    - All programs + Specific status
    - Specific program + Specific status
    """
    # Get filters from URL params
    program_filter = request.GET.get('program', 'all')  # Default 'all'
    status_filter = request.GET.get('status', 'pending')  # Default 'pending'
    
    # Base query: All enrollments with related student data
    queryset = SectionPlacement.objects.select_related('student').order_by('-placement_date', '-id')
    
    # Apply program filter
    if program_filter and program_filter != 'all':
        queryset = queryset.filter(selected_program__iexact=program_filter)
    
    # Apply status filter
    if status_filter and status_filter != 'all':
        queryset = queryset.filter(status=status_filter)
    
    # Fetch enrollments as list of dicts for template
    enrollments = list(queryset.values(
        'id',
        'student__id',
        'student__lrn',
        'student__first_name',
        'student__middle_name',
        'student__last_name',
        'selected_program',
        'status',
        'placement_date'
    ))
    
    # Calculate stats based on CURRENT filters
    if program_filter and program_filter != 'all':
        # Stats for specific program
        stats_queryset = SectionPlacement.objects.filter(selected_program__iexact=program_filter)
        total_requests = stats_queryset.count()
        approved = stats_queryset.filter(status='approved').count()
        pending = stats_queryset.filter(status='pending').count()
        rejected = stats_queryset.filter(status='rejected').count()
    else:
        # Stats for all programs
        total_requests = SectionPlacement.objects.count()
        approved = SectionPlacement.objects.filter(status='approved').count()
        pending = SectionPlacement.objects.filter(status='pending').count()
        rejected = SectionPlacement.objects.filter(status='rejected').count()
    
    # Program display mapping
    PROGRAM_DISPLAY_NAMES = {
        'ste': 'STE',
        'spfl': 'SPFL',
        'sptve': 'SPTVE',
        'sned': 'SNED',
        'top5': 'TOP 5',
        'hetero': 'HETERO',
        'ohsp': 'OHSP',
        'regular': 'Regular',
    }
    
    # Determine display name
    if program_filter == 'all':
        display_name = 'All Programs'
    else:
        display_name = PROGRAM_DISPLAY_NAMES.get(program_filter.lower(), program_filter.upper())
    
    is_filtered = (program_filter != 'all' or status_filter != 'pending')
    
    context = {
        'enrollments': enrollments,
        'total_requests': total_requests,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'program_filter': program_filter,
        'status_filter': status_filter,
        'display_name': display_name,
        'is_filtered': is_filtered,
    }
    
    return render(request, 'admin_functionalities/enrollment-management.html', context)



# TEACHERS VIEWS
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teacher  # Ensure you import the Teacher model

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teacher

@login_required
def teachers_view(request):
    teachers = Teacher.objects.order_by('last_name', 'first_name')
    teachers_data = []  # Prepare detailed data for each teacher
    
    for t in teachers:
        teachers_data.append({
            'id': t.id,
            'fullName': t.full_name or f"{t.first_name} {t.last_name}".strip(),
            'sex': t.gender or 'N/A',
            'age': t.age or 'N/A',
            'position': t.position or 'N/A',
            'employeeId': t.employee_id or 'N/A',
            'lastName': t.last_name or 'N/A',
            'firstName': t.first_name or 'N/A',
            'middleName': t.middle_name or 'N/A',
            'dateOfBirth': t.date_of_birth.strftime('%B %d, %Y') if t.date_of_birth else 'N/A',
            'department': t.department or 'N/A',
            'email': t.email or 'N/A',
            'phone': t.phone or 'N/A',
            'address': t.address or 'N/A',
            'photo': t.profile_photo.url if t.profile_photo else '/static/admin_functionalities/assets/kakashi.webp',
            # Removed problematic fields; add back if they exist in your model
        })
    
    context = {
        'teachers': teachers_data,  # Pass the list with full details
    }
    
    return render(request, 'admin_functionalities/teachers.html', context)


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
class AddUserView(View):
    def get(self, request):
        # If someone directly visits the URL, just redirect them to the settings page
        return redirect(reverse('admin_functionalities:settings'))

    def post(self, request):
        print(f"=== DEBUG: POST received in AddUser View! Raw POST data: {dict(request.POST)} ===")
        print(f"=== DEBUG: FILES present: {bool(request.FILES)} (userImage: {request.FILES.get('userImage', 'None')}) ===")

        form = AddUserForm(request.POST, request.FILES)
        print(f"=== DEBUG: Form errors before validation: {form.errors} ===")

        if form.is_valid():
            print("=== DEBUG: Form VALID – Saving user... ===")
            try:
                # ✅ Fixed: pass created_by_user so AddUserLog will be created
                user = form.save(created_by_user=request.user)

                print(f"=== DEBUG: SUCCESS – User created! ID={user.id}, Position={user.position}, Roles: "
                      f"is_subject_teacher={user.is_subject_teacher}, is_adviser={user.is_adviser} ===")

                # AJAX response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'User added successfully!',
                        'user_id': user.id,
                        'position': user.position
                    })

                # Non-AJAX: redirect back to settings
                return redirect(reverse('admin_functionalities:settings'))

            except Exception as save_err:
                print(f"=== DEBUG: Save ERROR: {save_err} ===")

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': str(save_err)}, status=500)

                # Non-AJAX: Redirect with error
                from django.contrib import messages
                messages.error(request, f"Error saving user: {save_err}")
                return redirect(reverse('admin_functionalities:settings'))

        else:
            print("=== DEBUG: Form INVALID – Returning JSON errors ===")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                    'message': 'Please correct the errors below.'
                }, status=400)

            # Non-AJAX: Redirect with message
            from django.contrib import messages
            messages.error(request, 'Form errors occurred. Please check and try again.')
            return redirect(reverse('admin_functionalities:settings'))

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

@login_required
def get_users_data(request):
    users = CustomUser.objects.filter(is_active=True).order_by('-id')[:20]
    users_html = render_to_string('admin_functionalities/partials/users_table.html', {'users': users})  # Render partial HTML
    return JsonResponse({'users_html': users_html})

@login_required
def get_logs_data(request):
    logs = AddUserLog.objects.select_related('user').order_by('-date', '-time')[:20]
    
    # Prepare logs with combined activity
    logs_data = []
    for log in logs:
        # Determine the role for the affected user
        role = "admin" if log.affected_is_admin else \
               "administrative staff" if log.affected_is_staff_expert else \
               "teacher" if log.affected_is_adviser or log.affected_is_teacher or log.affected_is_subject_teacher else "user"
        
        # Combined activity string: "Username performed action for Role"
        combined_activity = f"{log.user.username} {log.action} for {role}"
        
        logs_data.append({
            'combined_activity': combined_activity,  # New combined field
            'date': log.date.strftime('%B %d, %Y') if log.date else 'N/A',
            'time': log.time.strftime('%I:%M %p') if log.time else 'N/A',
        })
    
    logs_html = render_to_string('admin_functionalities/partials/history_table.html', {'logs': logs_data})  # Pass the new data
    return JsonResponse({'logs_html': logs_html})




