from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Case, When, IntegerField
from admin_functionalities.models import Teacher, Section, SectionSubjectAssignment
from enrollmentprocess.models import Student, StudentAcademic
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from teacher.models import Intervention, InterventionUpdate


@login_required
def adviser_view(request):
    """
    Adviser Dashboard Detail View - Shows detailed stats and student categories
    """
    user = request.user
    
    # Get teacher profile
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return redirect('login')
    
    # Get advisory section
    advisory_section = Section.objects.filter(adviser=teacher).first()
    
    if not advisory_section:
        # Teacher doesn't have an advisory class
        context = {
            'teacher': teacher,
            'teacher_full_name': f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name}".strip(),
            'teacher_position': teacher.position if teacher.position else 'Teacher',
            'teacher_photo': teacher.profile_photo.url if teacher.profile_photo else None,
            'teacher_initials': _get_initials(teacher),
            'has_advisory_class': False,
            'error_message': 'You do not have an assigned advisory class.',
        }
        return render(request, 'teacher/adviser/adviser_view.html', context)
    
    # Get students in this section
    section_name = advisory_section.name
    subject_assignments = SectionSubjectAssignment.objects.filter(
    teacher=teacher
    ).select_related('section')

    section_ids = subject_assignments.values_list('section_id', flat=True).distinct()
    students = Student.objects.filter(section_placement=section_name)
    
    # Count total students
    total_students = sum(
        Section.objects.filter(id__in=section_ids).values_list('current_students', flat=True)
    )
    
    # Gender breakdown (gender field stores "Male" or "Female")
    male_count = students.filter(gender='Male').count()
    female_count = students.filter(gender='Female').count()
    
    # Students on probation (STATIC for now - will use ML model later)
    # TODO: Replace with ML model prediction when ready
    probation_count = 1  # Static placeholder
    probation_male = 1   # Static placeholder
    probation_female = 0 # Static placeholder
    
    # Get sample probation students for display (static data for now)
    probation_students = []  # Empty for now, will be populated by ML model
    
    # Students at risk (STATIC for now - will use ML model later)
    atrisk_count = 0  # Static placeholder
    
    # Transfer-in students (STATIC - no field in model yet)
    transfer_in_count = 0
    
    # Repeaters (STATIC - no field in model yet)
    repeaters_count = 0
    
    # Get probation students with details for the detail panel
    probation_students_list = []
    for student in probation_students:
        try:
            academic = student.studentacademic
            probation_students_list.append({
                'id': student.id,
                'lrn': student.lrn,
                'full_name': f"{student.last_name}, {student.first_name} {student.middle_name}".strip(),
                'gender': student.gender,
                'overall_average': academic.overall_average,
                'photo': student.photo.url if student.photo else None,
                'subjects': {
                    'Mathematics': academic.mathematics,
                    'English': academic.english,
                    'Science': academic.science,
                    'Filipino': academic.filipino,
                    'Araling Panlipunan': academic.araling_panlipunan,
                    'Edukasyon sa Pagpapakatao': academic.edukasyon_pagpapakatao,
                    'MAPEH': academic.mapeh,
                }
            })
        except StudentAcademic.DoesNotExist:
            continue
    
    context = {
        'teacher': teacher,
        'teacher_full_name': f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name}".strip(),
        'teacher_position': teacher.position if teacher.position else 'Teacher',
        'teacher_photo': teacher.profile_photo.url if teacher.profile_photo else None,
        'teacher_initials': _get_initials(teacher),
        'has_advisory_class': True,
        
        # Section info
        'program': advisory_section.get_program_display(),
        'program_code': advisory_section.program,
        'section_name': advisory_section.name,
        'full_section_name': f"{advisory_section.program}-{advisory_section.name}", 
        
        # Stats
        'total_students': total_students,
        'male_count': male_count,
        'female_count': female_count,
        'probation_count': probation_count,
        'probation_male': probation_male,
        'probation_female': probation_female,
        'atrisk_count': atrisk_count,
        'transfer_in_count': transfer_in_count,
        'repeaters_count': repeaters_count,
        
        # Student lists
        'probation_students': probation_students_list,
        
        # Current quarter (can be made dynamic later)
        'current_quarter': 'Q1',
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
    }
    
    return render(request, 'teacher/adviser/adviser_view.html', context)


def _get_initials(teacher):
    """Helper function to generate teacher initials"""
    if teacher.first_name and teacher.last_name:
        return f"{teacher.first_name[0]}{teacher.last_name[0]}".upper()
    elif teacher.first_name:
        return teacher.first_name[0].upper()
    elif teacher.last_name:
        return teacher.last_name[0].upper()
    return "T"


@login_required
@require_http_methods(["GET"])
def get_interventions(request):
    """
    Get all interventions for the logged-in teacher's advisory class
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    # Get advisory section
    advisory_section = Section.objects.filter(adviser=teacher).first()
    if not advisory_section:
        return JsonResponse({'interventions': []})
    
    # Get quarter filter
    quarter = request.GET.get('quarter', 'Q1')
    
    # Get students in this section
    section_name = advisory_section.name
    students = Student.objects.filter(section_placement=section_name)
    student_ids = students.values_list('id', flat=True)
    
    # Get interventions for these students
    interventions = Intervention.objects.filter(
        student_id__in=student_ids,
        quarter=quarter,
        is_active=True
    ).select_related('student', 'created_by').prefetch_related('updates')
    
    # Serialize interventions
    data = []
    for intervention in interventions:
        updates = []
        for update in intervention.updates.all():
            updates.append({
                'id': update.id,
                'date': update.date.strftime('%Y-%m-%d'),
                'status': update.status,
                'note': update.note,
                'created_at': update.created_at.isoformat()
            })
        
        data.append({
            'id': intervention.id,
            'student': f"{intervention.student.last_name}, {intervention.student.first_name}",
            'student_id': intervention.student.id,
            'quarter': intervention.quarter,
            'start_date': intervention.start_date.strftime('%Y-%m-%d') if intervention.start_date else '',
            'review_date': intervention.review_date.strftime('%Y-%m-%d') if intervention.review_date else '',
            'reason': intervention.reason,
            'smart_goal': intervention.smart_goal,
            'last_status': intervention.last_status,
            'created_at': intervention.created_at.isoformat(),
            'updates': updates
        })
    
    return JsonResponse({'interventions': data})


@login_required
@require_http_methods(["POST"])
def create_intervention(request):
    """
    Create a new intervention
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('student_name'):
            return JsonResponse({'error': 'Student name is required'}, status=400)
        
        # Parse student name (format: "LastName, FirstName")
        student_name = data.get('student_name', '').strip()
        name_parts = student_name.split(',')
        if len(name_parts) != 2:
            return JsonResponse({'error': 'Invalid student name format'}, status=400)
        
        last_name = name_parts[0].strip()
        first_name = name_parts[1].strip()
        
        # Find student
        student = Student.objects.filter(
            last_name=last_name,
            first_name__startswith=first_name
        ).first()
        
        if not student:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
        # Parse dates
        start_date = None
        review_date = None
        if data.get('start_date'):
            try:
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        if data.get('review_date'):
            try:
                review_date = datetime.strptime(data['review_date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Create intervention
        intervention = Intervention.objects.create(
            student=student,
            created_by=teacher,
            quarter=data.get('quarter', 'Q1'),
            start_date=start_date,
            review_date=review_date,
            reason=data.get('reason', ''),
            smart_goal=data.get('smart_goal', ''),
            intervention_type='General',  # Default type
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'intervention': {
                'id': intervention.id,
                'student': f"{intervention.student.last_name}, {intervention.student.first_name}",
                'quarter': intervention.quarter,
                'start_date': intervention.start_date.strftime('%Y-%m-%d') if intervention.start_date else '',
                'review_date': intervention.review_date.strftime('%Y-%m-%d') if intervention.review_date else '',
                'reason': intervention.reason,
                'smart_goal': intervention.smart_goal,
                'last_status': intervention.last_status,
                'created_at': intervention.created_at.isoformat(),
                'updates': []
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def add_intervention_update(request, intervention_id):
    """
    Add an update to an existing intervention
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        intervention = Intervention.objects.get(id=intervention_id)
    except Intervention.DoesNotExist:
        return JsonResponse({'error': 'Intervention not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        
        # Parse date
        update_date = datetime.now().date()
        if data.get('date'):
            try:
                update_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Create update
        update = InterventionUpdate.objects.create(
            intervention=intervention,
            date=update_date,
            status=data.get('status', 'No change'),
            note=data.get('note', ''),
            created_by=teacher
        )
        
        # Refresh intervention to get updated last_status
        intervention.refresh_from_db()
        
        return JsonResponse({
            'success': True,
            'update': {
                'id': update.id,
                'date': update.date.strftime('%Y-%m-%d'),
                'status': update.status,
                'note': update.note,
                'created_at': update.created_at.isoformat()
            },
            'intervention_status': intervention.last_status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_intervention(request, intervention_id):
    """
    Delete (soft delete) an intervention
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        intervention = Intervention.objects.get(id=intervention_id, created_by=teacher)
        
        # Soft delete by setting is_active to False
        intervention.is_active = False
        intervention.save()
        
        return JsonResponse({'success': True})
        
    except Intervention.DoesNotExist:
        return JsonResponse({'error': 'Intervention not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_intervention_update(request, update_id):
    """
    Delete an intervention update
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        update = InterventionUpdate.objects.get(id=update_id)
        intervention = update.intervention
        
        # Check if this teacher created the intervention
        if intervention.created_by != teacher:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        # Delete the update
        update.delete()
        
        # Recalculate last_status from remaining updates
        latest_update = intervention.updates.order_by('-date').first()
        intervention.last_status = latest_update.status if latest_update else ''
        intervention.save()
        
        return JsonResponse({
            'success': True,
            'intervention_status': intervention.last_status
        })
        
    except InterventionUpdate.DoesNotExist:
        return JsonResponse({'error': 'Update not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)