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
from django.db.models import Count
from django.http import JsonResponse
from django.db import models

from admin_functionalities.models import (
    Section, 
    Teacher, 
    SectionSubjectAssignment,
    Program,
    Subject
)
from admin_functionalities.forms import SectionForm, SubjectForm, ProgramForm
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
    """
    Assigns teachers to subjects within a section.
    Now works with Subject model instead of hardcoded subjects.
    """
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Section not found.'
        }, status=404)

    try:
        body = json.loads(request.body)
        assignments = body.get('assignments', [])
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)

    created_count = 0
    updated_count = 0
    
    for a in assignments:
        subject_id = a.get('subject_id')
        teacher_id = a.get('teacher_id')
        day = a.get('day')
        start_time = a.get('start_time')
        end_time = a.get('end_time')

        if not (subject_id and teacher_id and day and start_time and end_time):
            continue  # Skip incomplete assignments

        try:
            subject = Subject.objects.get(id=subject_id, is_active=True)
            teacher = Teacher.objects.get(id=teacher_id, is_active=True)
        except (Subject.DoesNotExist, Teacher.DoesNotExist):
            continue  # Skip if subject or teacher not found

        # Check for scheduling conflicts
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
                'message': f'{teacher.full_name} already has a class in section {conflict_section.name} at that time.'
            }, status=400)

        assignment, created = SectionSubjectAssignment.objects.update_or_create(
            section=section,
            subject=subject,
            defaults={
                'teacher': teacher,
                'day': day,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        
        if created:
            created_count += 1
        else:
            updated_count += 1
    
    log_activity(
        request.user,
        "Sections",
        f"Assigned/updated {created_count + updated_count} subject teacher(s) to section {section.name}"
    )

    return JsonResponse({
        'success': True,
        'message': f'Successfully assigned {created_count} and updated {updated_count} subject teacher(s).'
    }, status=200)
    
@login_required
@require_http_methods(["GET"])
def get_subjects_by_program(request, program):
    """
    Fetch all subjects for a specific program.
    Used by the Manage Subjects modal.
    """
    try:
        program_name = program.upper()
        
        try:
            program_instance = Program.objects.get(name=program_name, is_active=True)
        except Program.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Program "{program_name}" not found or inactive'
            }, status=404)
        
        subjects = Subject.objects.filter(
            program=program_instance,
            is_active=True
        ).order_by('display_order', 'subject_name')
        
        subjects_data = [{
            'id': subject.id,
            'name': subject.subject_name,
            'code': subject.subject_code,
            'description': subject.description,
            'display_order': subject.display_order,
            'program': program_name
        } for subject in subjects]
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data,
            'program': program_name
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_subjects_by_program: {error_details}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
        
@login_required
@require_http_methods(["POST"])
def add_subject(request, program):
    """
    Add a new subject to a specific program.
    """
    try:
        program_name = program.upper()
        
        try:
            program_instance = Program.objects.get(name=program_name, is_active=True)
        except Program.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Program "{program_name}" does not exist.'
            }, status=400)
        
        # Pass program instance to form
        form = SubjectForm(request.POST, program=program_instance)
        
        if form.is_valid():
            subject = form.save(commit=False)
            subject.program = program_instance
            
            # Set display_order if not provided
            if not subject.display_order:
                max_order = Subject.objects.filter(
                    program=program_instance
                ).aggregate(models.Max('display_order'))['display_order__max']
                subject.display_order = (max_order or 0) + 1
            
            subject.save()
            
            log_activity(
                request.user,
                "Subjects",
                f"Added subject {subject.subject_name} to {program_name} program"
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Subject "{subject.subject_name}" added successfully!',
                'subject': {
                    'id': subject.id,
                    'name': subject.subject_name,
                    'code': subject.subject_code,
                    'description': subject.description,
                    'display_order': subject.display_order,
                    'program': program_name
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
        print(f"ERROR in add_subject: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error adding subject: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_subject(request, subject_id):
    """
    Update an existing subject.
    """
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        original_program = subject.program
        
        form = SubjectForm(request.POST, instance=subject, program=original_program)
        
        if form.is_valid():
            updated_subject = form.save(commit=False)
            updated_subject.program = original_program  # Ensure program doesn't change
            updated_subject.save()
            
            log_activity(
                request.user,
                "Subjects",
                f"Updated subject {updated_subject.subject_name} in {original_program.name}"
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Subject "{updated_subject.subject_name}" updated successfully!',
                'subject': {
                    'id': updated_subject.id,
                    'name': updated_subject.subject_name,
                    'code': updated_subject.subject_code,
                    'description': updated_subject.description,
                    'display_order': updated_subject.display_order,
                    'program': original_program.name
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
        print(f"ERROR in update_subject: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error updating subject: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_subject(request, subject_id):
    """
    Delete a subject.
    Checks if subject is assigned to any sections before deleting.
    """
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        subject_name = subject.subject_name
        program_name = subject.program.name
        
        # Check if subject is assigned to any sections
        assignments = SectionSubjectAssignment.objects.filter(subject=subject)
        
        if assignments.exists():
            sections = [a.section.name for a in assignments[:5]]
            section_list = ", ".join(sections)
            more_text = f" and {assignments.count() - 5} more" if assignments.count() > 5 else ""
            
            return JsonResponse({
                'success': False,
                'message': f'Cannot delete "{subject_name}". It is currently assigned to sections: {section_list}{more_text}. Please remove these assignments first.'
            }, status=400)
        
        subject.delete()
        
        log_activity(
            request.user,
            "Subjects",
            f"Deleted subject {subject_name} from {program_name} program"
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Subject "{subject_name}" deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error deleting subject: {str(e)}'
        }, status=500)
        
@login_required
@require_http_methods(["GET"])
def get_section_subjects(request, section_id):
    """
    Get all subjects for a section's program.
    Used when opening the Assign Teacher modal.
    """
    try:
        section = get_object_or_404(Section, id=section_id)
        program = section.program
        
        subjects = Subject.get_subjects_for_program(program)
        
        subjects_data = [{
            'id': subject.id,
            'name': subject.subject_name,
            'code': subject.subject_code,
            'key': subject.subject_code.lower().replace('-', '').replace(' ', '')
        } for subject in subjects]
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data,
            'section': {
                'id': section.id,
                'name': section.name,
                'program': program.name
            }
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_section_subjects: {error_details}")
        
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# Manage program@login_required
@require_http_methods(["GET"])
def get_school_years(request):
    """
    Fetch all school years for dropdown selections.
    """
    try:
        from admin_functionalities.models import SchoolYear
        
        school_years = SchoolYear.objects.all().order_by('-start_date')
        
        school_years_data = []
        for sy in school_years:
            school_years_data.append({
                'id': sy.id,
                'name': str(sy),
                'start_date': sy.start_date.strftime('%Y-%m-%d'),
                'end_date': sy.end_date.strftime('%Y-%m-%d'),
                'is_active': sy.is_active
            })
        
        return JsonResponse({
            'success': True,
            'school_years': school_years_data
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_school_years: {error_details}")
        
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# Program management@login_required
@require_http_methods(["GET"])
def get_all_programs(request):
    """
    Fetch all programs with section counts.
    """
    try:
        programs = Program.objects.annotate(
            section_count=Count('sections', distinct=True)
        ).order_by('name')
        
        programs_data = []
        for program in programs:
            programs_data.append({
                'id': program.id,
                'name': program.name,
                'description': program.description,
                'school_year': {
                    'id': program.school_year.id,
                    'name': str(program.school_year)
                },
                'is_active': program.is_active,
                'section_count': program.section_count,
                'created_at': program.created_at.strftime('%Y-%m-%d'),
                'updated_at': program.updated_at.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({
            'success': True,
            'programs': programs_data
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in get_all_programs: {error_details}")
        
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def add_program(request):
    """
    Add a new program.
    """
    try:
        form = ProgramForm(request.POST)
        
        if form.is_valid():
            program = form.save()
            
            log_activity(
                request.user,
                "Programs",
                f"Added new program: {program.name}"
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Program "{program.name}" added successfully!',
                'program': {
                    'id': program.id,
                    'name': program.name,
                    'description': program.description,
                    'school_year': {
                        'id': program.school_year.id,
                        'name': str(program.school_year)
                    },
                    'is_active': program.is_active,
                    'section_count': 0
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
        print(f"ERROR in add_program: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error adding program: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_program(request, program_id):
    """
    Update an existing program.
    """
    try:
        program = get_object_or_404(Program, id=program_id)
        
        form = ProgramForm(request.POST, instance=program)
        
        if form.is_valid():
            updated_program = form.save()
            
            log_activity(
                request.user,
                "Programs",
                f"Updated program: {updated_program.name}"
            )
            
            # Get section count
            section_count = Section.objects.filter(program=updated_program).count()
            
            return JsonResponse({
                'success': True,
                'message': f'Program "{updated_program.name}" updated successfully!',
                'program': {
                    'id': updated_program.id,
                    'name': updated_program.name,
                    'description': updated_program.description,
                    'school_year': {
                        'id': updated_program.school_year.id,
                        'name': str(updated_program.school_year)
                    },
                    'is_active': updated_program.is_active,
                    'section_count': section_count
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
        print(f"ERROR in update_program: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error updating program: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_program(request, program_id):
    """
    Delete a program.
    Checks if program has active sections before deleting.
    """
    try:
        program = get_object_or_404(Program, id=program_id)
        program_name = program.name
        
        # Check if program has active sections
        sections = Section.objects.filter(program=program, is_active=True)
        
        if sections.exists():
            section_names = [s.name for s in sections[:5]]
            section_list = ", ".join(section_names)
            more_text = f" and {sections.count() - 5} more" if sections.count() > 5 else ""
            
            return JsonResponse({
                'success': False,
                'message': f'Cannot delete "{program_name}". It has active sections: {section_list}{more_text}. Please remove or deactivate these sections first.'
            }, status=400)
        
        # Check if program has any sections (active or inactive)
        all_sections = Section.objects.filter(program=program)
        if all_sections.exists():
            return JsonResponse({
                'success': False,
                'message': f'Cannot delete "{program_name}". It has {all_sections.count()} section(s) in the database. Please remove all sections first or contact the system administrator.'
            }, status=400)
        
        program.delete()
        
        log_activity(
            request.user,
            "Programs",
            f"Deleted program: {program_name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Program "{program_name}" deleted successfully!'
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in delete_program: {error_details}")
        
        return JsonResponse({
            'success': False,
            'message': f'Error deleting program: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def toggle_program_status(request, program_id):
    """
    Toggle program active status (activate/deactivate).
    """
    try:
        program = get_object_or_404(Program, id=program_id)
        
        if program.is_active:
            program.deactivate()
            status = "deactivated"
        else:
            program.activate()
            status = "activated"
        
        log_activity(
            request.user,
            "Programs",
            f"{status.capitalize()} program: {program.name}"
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Program "{program.name}" {status} successfully!',
            'program': {
                'id': program.id,
                'name': program.name,
                'is_active': program.is_active
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error toggling program status: {str(e)}'
        }, status=500)
        
