# ============================================================================
# 4. admin_functionalities/views/section_views.py
# ============================================================================
"""
Section management views.
"""

import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import models

from admin_functionalities.models import (
    Section, 
    Teacher, 
    SectionSubjectAssignment,
    Program,
)
from admin_functionalities.forms import SectionForm
from admin_functionalities.utils import log_activity
from enrollmentprocess.models import SectionPlacement, Student
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@login_required
def sections_view(request):
    """Main sections management page."""
    program = request.GET.get('program', 'STE')
    
    teachers = CustomUser.objects.filter(
        models.Q(is_adviser=True) | models.Q(is_subject_teacher=True)
    ).order_by('last_name', 'first_name')
    
    teachers_data = []
    for teacher in teachers:
        full_name = f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name}".strip()
        teachers_data.append({
            'id': teacher.id,
            'name': full_name if full_name else teacher.username,
        })
    
    context = {
        'active_page': 'sections',
        'initial_program': program,
        'teachers': teachers_data,
    }
    return render(request, 'admin_functionalities/sections.html', context)


@login_required
@require_http_methods(["GET"])
def get_teachers(request):
    """Returns all teachers who can be advisers and subject teachers."""
    teachers = Teacher.objects.filter(is_active=True)

    adviser_list = []
    subject_teacher_list = []

    assigned_adviser_ids = set(
        Section.objects.exclude(adviser__isnull=True)
        .values_list('adviser_id', flat=True)
    )

    for t in teachers:
        if t.is_adviser:
            adviser_list.append({
                "id": t.id,
                "name": t.full_name,
                "isAssigned": t.id in assigned_adviser_ids
            })

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


@login_required
@require_http_methods(["GET"])
def get_subject_teachers(request):
    """Returns all active subject teachers with cleaned department names."""
    teachers = Teacher.objects.filter(is_subject_teacher=True, is_active=True)

    teacher_list = []
    for t in teachers:
        dept = (t.department or "").strip()
        if dept.lower().endswith("department"):
            dept = dept[:-len("department")].strip()

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
    """Returns building/room data for location dropdowns."""
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
    """Fetch all sections for a specific program."""
    try:
        program_name = program.upper()
        try:
            program_instance = Program.objects.get(name=program_name, is_active=True)
        except Program.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': f'Program "{program_name}" not found or inactive'
            }, status=404)
        
        sections = Section.objects.filter(
            program=program_instance,
            is_active=True
        ).select_related('adviser')
        
        sections_data = []
        for section in sections:
            adviser_name = "No Adviser"
            if section.adviser:
                adviser_name = f"{section.adviser.last_name}, {section.adviser.first_name}".strip()
                if adviser_name == ',':
                    adviser_name = section.adviser.user.username if hasattr(section.adviser, 'user') else "Unnamed Adviser"

            sections_data.append({
                'id': section.id,
                'name': section.name,
                'adviser': adviser_name,
                'adviserId': section.adviser.id if section.adviser else None,
                'building': section.building,
                'room': section.room,
                'location': f"Building {section.building} - Room {section.room}",
                'students': section.current_students,
                'maxStudents': section.max_students,
                'avatar': section.avatar.url if section.avatar else '/static/admin_functionalities/assets/spongebob.jpg',
            })

        return JsonResponse({'success': True, 'sections': sections_data})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_sections_by_program: {error_details}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def add_section(request, program):
    """Add a new section under the current program tab."""
    try:
        program_defaults = {
            'STE': 30,
            'SPFL': 30,
            'SPTVL': 30,
            'OHSP': 30,
            'SNED': 30,
            'TOP5': 50,
            'HETERO': 50,
            'REGULAR': 40,
        }

        program_name = program.upper()
        try:
            program_instance = Program.objects.get(name=program_name, is_active=True)
        except Program.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': f'Program "{program_name}" does not exist in the database.'
            }, status=400)

        form = SectionForm(request.POST, request.FILES)
        
        if form.is_valid():
            section = form.save(commit=False)
            section.program = program_instance
            
            max_students = form.cleaned_data.get('max_students')
            if not max_students or int(max_students) <= 0:
                section.max_students = program_defaults.get(program_name, 40)
            
            section.save()
            
            log_activity(
                request.user, 
                "Sections", 
                f"Added section {section.name} under {program_name} program"
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Section "{section.name}" added successfully to {program_name}!',
                'section': {
                    'id': section.id,
                    'name': section.name,
                    'program': program_name,
                    'max_students': section.max_students,
                    'current_students': section.current_students,
                }
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Validation failed. Please check the form fields.', 
                'errors': form.errors
            }, status=400)
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in add_section: {error_details}")
        
        return JsonResponse({
            'success': False, 
            'message': f'Error adding section: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_section(request, section_id):
    """Updates an existing section."""
    try:
        section = get_object_or_404(Section, id=section_id)
        original_program = section.program
        
        form = SectionForm(request.POST, request.FILES, instance=section)
        
        if form.is_valid():
            updated_section = form.save(commit=False)
            updated_section.program = original_program
            updated_section.save()
            
            log_activity(
                request.user, 
                "Sections", 
                f"Updated section {updated_section.name} in {original_program.name}"
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Section "{updated_section.name}" updated successfully!',
                'section': {
                    'id': updated_section.id,
                    'name': updated_section.name,
                    'adviser': updated_section.adviser.full_name if updated_section.adviser else 'No Adviser',
                    'building': updated_section.building,
                    'room': updated_section.room,
                    'max_students': updated_section.max_students,
                    'current_students': updated_section.current_students,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Validation failed',
                'errors': form.errors
            }, status=400)
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in update_section: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error updating section: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_section(request, section_id):
    """Deletes a section."""
    try:
        section = get_object_or_404(Section, id=section_id)
        section_name = section.name
        section.delete()
        log_activity(request.user, "Sections", f"Deleted section {section_name}")
        
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
    """Returns students currently placed in this section."""
    try:
        placements = SectionPlacement.objects.filter(
            section_id=section_id, 
            status='approved'
        ).select_related('student').order_by('student__last_name')
        
        students = [{
            'id': p.student.id,
            'lrn': p.student.lrn,
            'name': f"{p.student.last_name}, {p.student.first_name} {p.student.middle_name or ''}".strip()
        } for p in placements]
        
        return JsonResponse({'success': True, 'students': students})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def section_masterlist(request, section_id):
    """Display masterlist of students in a section."""
    section = get_object_or_404(Section, pk=section_id)

    students = Student.objects.filter(
        section_placements__section=section, 
        section_placements__status='approved'
    ).select_related('studentacademic')

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
    """Assigns teachers to subjects within a section."""
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

        try:
            teacher = Teacher.objects.get(id=teacher_id, is_active=True)
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'message': f'Teacher with ID {teacher_id} not found.'}, status=404)

        required_department = subject_department_map.get(subject)
        if not required_department:
            return JsonResponse({'success': False, 'message': f'Invalid subject: {subject}'}, status=400)

        if teacher.department != required_department:
            return JsonResponse({
                'success': False,
                'message': f'{teacher.full_name} belongs to {teacher.department} department, not {required_department}.'
            }, status=400)

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

        assignment, created = SectionSubjectAssignment.objects.update_or_create(
            section=section,
            subject=subject,
            defaults={
                'teacher': teacher.user if teacher.user else None,
                'day': day,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        created_count += 1 if created else 0
        
    log_activity(request.user, "Sections", f"Assigned subject teachers to section {section.name}")

    return JsonResponse({
        'success': True,
        'message': f'Successfully assigned {created_count} subject teacher(s).'
    }, status=200)