# teacher/views/adviser_subintervention_views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from datetime import datetime, timedelta
import json

from enrollmentprocess.models import Student
from admin_functionalities.models import Teacher, Subject, Section, SchoolYear, SectionSubjectAssignment
from teacher.models import (
    InterventionPlan, InterventionAction, InterventionNote,
    StudentGrade, StudentAttendance, AttendanceRecord
)


@login_required
def adviser_sub_intervention(request):
    """
    Main intervention system page.
    Shows all students with interventions for the adviser's sections.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return render(request, 'teacher/error.html', {
            'message': 'Teacher profile not found'
        })
    
    # Get adviser's sections
    sections = Section.objects.filter(adviser=teacher, is_active=True)
    
    # Get current school year
    current_sy = SchoolYear.get_current()
    
    # Get all active subjects (since SectionSubjectAssignment uses CharField for subject, not FK)
    # We'll filter by teacher's assigned subjects if needed
    subjects = Subject.objects.filter(is_active=True)
    
    # Optionally filter to only subjects this teacher teaches
    # Get subject codes/names from SectionSubjectAssignment
    from admin_functionalities.models import SectionSubjectAssignment
    taught_subject_codes = SectionSubjectAssignment.objects.filter(
        teacher=teacher
    ).values_list('subject', flat=True).distinct()
    
    if taught_subject_codes:
        # Match by subject name or code
        subjects = subjects.filter(
            Q(subject_code__in=taught_subject_codes) | 
            Q(subject_name__in=taught_subject_codes)
        )
    
    context = {
        'teacher': teacher,
        'sections': sections,
        'subjects': subjects,
        'current_sy': current_sy,
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
    }
    
    return render(request, 'teacher/adviser/subject_Intervention.html', context)


@login_required
@require_http_methods(["GET"])
def get_intervention_students(request):
    """
    API endpoint to get students with intervention data for a section/quarter.
    Returns student list with risk levels and intervention info.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    section_id = request.GET.get('section_id')
    quarter = request.GET.get('quarter', 'Q1')
    subject_id = request.GET.get('subject_id')
    
    if not section_id:
        return JsonResponse({'success': False, 'error': 'Section ID required'})
    
    section = get_object_or_404(Section, id=section_id)
    current_sy = SchoolYear.get_current()
    
    # Get all students in section
    students = Student.objects.filter(
        masterlist_entries__masterlist__section=section,
        masterlist_entries__is_active=True
    ).distinct()
    
    students_data = []
    
    for student in students:
        # Get intervention plan if exists
        intervention = InterventionPlan.objects.filter(
            student=student,
            quarter=quarter,
            school_year=current_sy,
            is_active=True
        ).first()
        
        # If no intervention, check if student needs one
        if not intervention:
            # Check attendance
            attendance_records = StudentAttendance.objects.filter(
                student=student,
                attendance_record__section=section,
                attendance_record__quarter=quarter
            )
            total_absences = sum(rec.total_absences for rec in attendance_records)
            
            # Check grades if subject specified
            missing_ww = 0
            missing_pt = 0
            current_grade = 0
            missed_qa = False
            
            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                student_grades = StudentGrade.objects.filter(
                    student=student,
                    class_record__section=section,
                    class_record__subject=subject,
                    class_record__quarter=quarter
                ).first()
                
                if student_grades:
                    current_grade = student_grades.quarterly_grade
                    
                    # Count missing works (scores = 0)
                    ww_scores = student_grades.get_ww_scores_list()
                    pt_scores = student_grades.get_pt_scores_list()
                    
                    missing_ww = sum(1 for score in ww_scores if score == 0)
                    missing_pt = sum(1 for score in pt_scores if score == 0)
                    
                    # Check if QA was given but student has 0
                    if student_grades.class_record.qa_hps_1 > 0 and student_grades.qa_score_1 == 0:
                        missed_qa = True
            
            # Determine if intervention needed
            needs_intervention = False
            risk_level = 'On Track'
            
            # Critical conditions
            if total_absences >= 7 or missed_qa or missing_ww >= 4 or missing_pt >= 3:
                needs_intervention = True
                risk_level = 'Critical'
            # At Risk conditions
            elif total_absences >= 5 or missing_ww >= 2 or missing_pt >= 2:
                needs_intervention = True
                risk_level = 'At Risk'
            elif missing_ww >= 1 and missing_pt >= 1:
                needs_intervention = True
                risk_level = 'At Risk'
            
            # Create intervention if needed
            if needs_intervention and subject_id:
                intervention = InterventionPlan.objects.create(
                    student=student,
                    section=section,
                    subject_id=subject_id,
                    created_by=teacher,
                    quarter=quarter,
                    school_year=current_sy,
                    risk_level=risk_level,
                    current_grade=current_grade,
                    total_absences=total_absences,
                    missing_written_works=missing_ww,
                    missing_performance_tasks=missing_pt,
                    missed_quarterly_assessment=missed_qa
                )
                intervention.update_risk_assessment()
        
        # Build student data
        if intervention:
            student_data = {
                'id': student.id,
                'lrn': student.lrn,
                'name': f"{student.last_name}, {student.first_name} {student.middle_name}".strip(),
                'sex': student.gender,
                'age': student.age,
                'current_grade': intervention.current_grade,
                'absences': intervention.total_absences,
                'missing_work': intervention.missing_written_works + intervention.missing_performance_tasks,
                'missing_ww': intervention.missing_written_works,
                'missing_pt': intervention.missing_performance_tasks,
                'missed_qa': intervention.missed_quarterly_assessment,
                'risk_level': intervention.risk_level,
                'intervention_tier': intervention.current_tier,
                'intervention_id': intervention.id,
                'has_intervention': True,
                'is_resolved': intervention.is_resolved,
            }
        else:
            # Student without intervention (on track)
            student_data = {
                'id': student.id,
                'lrn': student.lrn,
                'name': f"{student.last_name}, {student.first_name} {student.middle_name}".strip(),
                'sex': student.gender,
                'age': student.age,
                'current_grade': 0,
                'absences': 0,
                'missing_work': 0,
                'missing_ww': 0,
                'missing_pt': 0,
                'missed_qa': False,
                'risk_level': 'On Track',
                'intervention_tier': 'None',
                'intervention_id': None,
                'has_intervention': False,
                'is_resolved': False,
            }
        
        students_data.append(student_data)
    
    # Calculate statistics
    stats = {
        'total': len(students_data),
        'critical': len([s for s in students_data if s['risk_level'] == 'Critical']),
        'at_risk': len([s for s in students_data if s['risk_level'] == 'At Risk']),
        'on_track': len([s for s in students_data if s['risk_level'] == 'On Track']),
    }
    
    return JsonResponse({
        'success': True,
        'students': students_data,
        'stats': stats
    })


@login_required
@require_http_methods(["GET"])
def get_student_intervention_details(request, student_id):
    """
    Get detailed intervention information for a specific student.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    quarter = request.GET.get('quarter', 'Q1')
    subject_id = request.GET.get('subject_id')
    
    student = get_object_or_404(Student, id=student_id)
    current_sy = SchoolYear.get_current()
    
    # Get intervention plan
    intervention = InterventionPlan.objects.filter(
        student=student,
        quarter=quarter,
        school_year=current_sy
    ).first()
    
    if not intervention:
        return JsonResponse({'success': False, 'error': 'No intervention plan found'})
    
    # Get all actions for this intervention
    actions = InterventionAction.objects.filter(
        intervention_plan=intervention
    ).select_related('handled_by')
    
    actions_data = [{
        'id': action.id,
        'tier': action.tier,
        'action_type': action.action_type,
        'action_name': action.action_name,
        'description': action.description,
        'start_date': action.start_date.strftime('%Y-%m-%d'),
        'target_date': action.target_date.strftime('%Y-%m-%d') if action.target_date else '',
        'completion_date': action.completion_date.strftime('%Y-%m-%d') if action.completion_date else '',
        'status': action.status,
        'progress_notes': action.progress_notes,
        'teacher_notes': action.teacher_notes,
        'handled_by': action.handled_by.full_name,
        'was_successful': action.was_successful,
        'outcome_notes': action.outcome_notes,
    } for action in actions]
    
    # Get notes
    notes = InterventionNote.objects.filter(
        intervention_plan=intervention
    ).select_related('created_by')
    
    notes_data = [{
        'id': note.id,
        'note': note.note,
        'date': note.note_date.strftime('%Y-%m-%d'),
        'created_by': note.created_by.full_name,
    } for note in notes]
    
    data = {
        'success': True,
        'intervention': {
            'id': intervention.id,
            'risk_level': intervention.risk_level,
            'current_tier': intervention.current_tier,
            'current_grade': intervention.current_grade,
            'total_absences': intervention.total_absences,
            'missing_ww': intervention.missing_written_works,
            'missing_pt': intervention.missing_performance_tasks,
            'missed_qa': intervention.missed_quarterly_assessment,
            'risk_factors': intervention.get_risk_factors(),
            'is_resolved': intervention.is_resolved,
        },
        'actions': actions_data,
        'notes': notes_data,
    }
    
    return JsonResponse(data)


@login_required
@require_POST
def create_intervention_action(request):
    """
    Create a new intervention action.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    try:
        data = json.loads(request.body)
        intervention_id = data.get('intervention_id')
        
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        action = InterventionAction.objects.create(
            intervention_plan=intervention,
            tier=data.get('tier'),
            action_type=data.get('action_type', 'Other'),
            action_name=data.get('action_name'),
            description=data.get('description'),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
            target_date=datetime.strptime(data.get('target_date'), '%Y-%m-%d').date() if data.get('target_date') else None,
            status=data.get('status', 'Planned'),
            progress_notes=data.get('progress_notes', ''),
            teacher_notes=data.get('teacher_notes', ''),
            handled_by=teacher
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention action created successfully',
            'action_id': action.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def update_intervention_action(request, action_id):
    """
    Update an existing intervention action.
    """
    try:
        teacher = request.user.teacher_profile
        data = json.loads(request.body)
        action = get_object_or_404(InterventionAction, id=action_id)
        
        # Verify teacher has permission to update
        if action.handled_by != teacher and action.intervention_plan.created_by != teacher:
            return JsonResponse({'success': False, 'error': 'You do not have permission to update this action'})
        
        # Update fields
        if 'action_name' in data:
            action.action_name = data['action_name']
        if 'action_type' in data:
            action.action_type = data['action_type']
        if 'tier' in data:
            action.tier = data['tier']
        if 'description' in data:
            action.description = data['description']
        if 'start_date' in data and data['start_date']:
            action.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'target_date' in data and data['target_date']:
            action.target_date = datetime.strptime(data['target_date'], '%Y-%m-%d').date()
        if 'status' in data:
            action.status = data['status']
        if 'progress_notes' in data:
            action.progress_notes = data['progress_notes']
        if 'teacher_notes' in data:
            action.teacher_notes = data['teacher_notes']
        if 'completion_date' in data and data['completion_date']:
            action.completion_date = datetime.strptime(data['completion_date'], '%Y-%m-%d').date()
        if 'was_successful' in data:
            action.was_successful = data['was_successful']
        if 'outcome_notes' in data:
            action.outcome_notes = data['outcome_notes']
        
        action.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention action updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def add_intervention_note(request):
    """
    Add a progress note to an intervention plan.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    try:
        data = json.loads(request.body)
        intervention_id = data.get('intervention_id')
        
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        note = InterventionNote.objects.create(
            intervention_plan=intervention,
            note=data.get('note'),
            note_date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else timezone.now().date(),
            created_by=teacher
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Note added successfully',
            'note_id': note.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def resolve_intervention(request, intervention_id):
    """
    Mark an intervention as resolved.
    """
    try:
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        intervention.is_resolved = True
        intervention.is_active = False
        intervention.resolved_date = timezone.now()
        intervention.risk_level = 'Resolved'
        intervention.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention marked as resolved'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def reactivate_intervention(request, intervention_id):
    """
    Reactivate a resolved intervention.
    """
    try:
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        intervention.is_resolved = False
        intervention.is_active = True
        intervention.resolved_date = None
        intervention.update_risk_assessment()
        intervention.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention reactivated'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def escalate_to_tier_3(request, intervention_id):
    """
    Escalate intervention to Tier 3 (adviser intervention).
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    try:
        data = json.loads(request.body)
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        # Update tier
        intervention.current_tier = 'Tier 3'
        intervention.save()
        
        # Create Tier 3 action
        action = InterventionAction.objects.create(
            intervention_plan=intervention,
            tier='Tier 3',
            action_type='Parent Contact',
            action_name='Tier 3 Escalation - Parent Conference Required',
            description=data.get('reason', 'Student has not responded to Tier 2 interventions. Requires adviser and parent involvement.'),
            start_date=timezone.now().date(),
            status='Planned',
            handled_by=teacher
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention escalated to Tier 3',
            'action_id': action.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_http_methods(["GET"])
def get_intervention_action(request, action_id):
    """
    Get details of a single intervention action for editing.
    """
    try:
        action = get_object_or_404(InterventionAction, id=action_id)
        
        data = {
            'success': True,
            'action': {
                'id': action.id,
                'tier': action.tier,
                'action_type': action.action_type,
                'action_name': action.action_name,
                'description': action.description,
                'start_date': action.start_date.strftime('%Y-%m-%d'),
                'target_date': action.target_date.strftime('%Y-%m-%d') if action.target_date else '',
                'completion_date': action.completion_date.strftime('%Y-%m-%d') if action.completion_date else '',
                'status': action.status,
                'progress_notes': action.progress_notes,
                'teacher_notes': action.teacher_notes,
                'handled_by': action.handled_by.full_name,
                'was_successful': action.was_successful,
                'outcome_notes': action.outcome_notes,
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_POST
def delete_intervention_action(request, action_id):
    """
    Delete an intervention action.
    """
    try:
        teacher = request.user.teacher_profile
        action = get_object_or_404(InterventionAction, id=action_id)
        
        # Verify teacher has permission to delete
        if action.handled_by != teacher and action.intervention_plan.created_by != teacher:
            return JsonResponse({'success': False, 'error': 'You do not have permission to delete this action'})
        
        intervention_plan = action.intervention_plan
        action.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Intervention action deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def get_active_assessments(class_record):
    """
    Determine which WW/PT columns are actually being used based on:
    1. HPS > 0 for that column (teacher has set it)
    2. OR any student has a score in that column
    
    Returns dict with active column indices for WW and PT
    """
    # Get all student grades for this class record
    student_grades = StudentGrade.objects.filter(class_record=class_record)
    
    active_ww_indices = set()
    active_pt_indices = set()
    
    # PRIORITY 1: Check HPS values (teacher explicitly activated this column)
    for i in range(1, 11):
        ww_hps = getattr(class_record, f'ww_hps_{i}', 0)
        pt_hps = getattr(class_record, f'pt_hps_{i}', 0)
        
        # Column is active if HPS > 0 (teacher set a max score)
        if ww_hps > 0:
            active_ww_indices.add(i)
        if pt_hps > 0:
            active_pt_indices.add(i)
    
    # PRIORITY 2: Check if ANY student has scores (fallback safety check)
    # This catches cases where teacher entered scores but forgot to set HPS
    for sg in student_grades:
        for i in range(1, 11):
            ww_score = getattr(sg, f'ww_score_{i}', 0)
            pt_score = getattr(sg, f'pt_score_{i}', 0)
            
            if ww_score > 0:
                active_ww_indices.add(i)
            if pt_score > 0:
                active_pt_indices.add(i)
    
    return {
        'ww': sorted(list(active_ww_indices)),
        'pt': sorted(list(active_pt_indices)),
        'ww_count': len(active_ww_indices),
        'pt_count': len(active_pt_indices)
    }


def count_missing_works(student_grade, active_assessments):
    """
    Count missing works based on ACTIVE columns only
    Returns: (missing_ww, missing_pt, ww_detail, pt_detail)
    """
    missing_ww = 0
    missing_pt = 0
    ww_detail = []
    pt_detail = []
    
    # Check only ACTIVE WW columns
    for i in active_assessments['ww']:
        score = getattr(student_grade, f'ww_score_{i}', 0)
        if score == 0:
            missing_ww += 1
            ww_detail.append(i)
    
    # Check only ACTIVE PT columns
    for i in active_assessments['pt']:
        score = getattr(student_grade, f'pt_score_{i}', 0)
        if score == 0:
            missing_pt += 1
            pt_detail.append(i)
    
    return missing_ww, missing_pt, ww_detail, pt_detail