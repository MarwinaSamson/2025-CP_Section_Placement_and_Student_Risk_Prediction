# teacher/views/adviser_view_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from admin_functionalities.models import Teacher, Section, SectionSubjectAssignment, SchoolYear
from enrollmentprocess.models import Student
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from teacher.models import (
    Intervention, InterventionUpdate, 
    InterventionPlan, InterventionAction,
    MasterlistStudent, AdviserMasterlist
)


@login_required
def adviser_view(request):
    """
    Adviser Dashboard Detail View - Shows subject teacher interventions (read-only)
    and allows creating adviser interventions for Tier 3 cases
    """
    user = request.user
    
    # Get teacher profile
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return redirect('login')
    
    # Get advisory section
    advisory_section = Section.objects.filter(adviser=teacher, is_active=True).first()
    
    if not advisory_section:
        context = {
            'teacher': teacher,
            'has_advisory_class': False,
            'error_message': 'You do not have an assigned advisory class.',
        }
        return render(request, 'teacher/adviser/adviser_view.html', context)
    
    # Get current school year
    current_sy = SchoolYear.get_current()
    
    # Get students in advisory section
    masterlist = AdviserMasterlist.objects.filter(
        adviser=teacher,
        section=advisory_section,
        school_year=current_sy.name if current_sy else '2025-2026',
        is_active=True
    ).first()
    
    if masterlist:
        students = Student.objects.filter(
            masterlist_entries__masterlist=masterlist,
            masterlist_entries__is_active=True
        ).distinct()
    else:
        students = Student.objects.filter(
            section_placement=advisory_section.name
        )
    
    total_students = students.count()
    male_count = students.filter(gender='Male').count()
    female_count = students.filter(gender='Female').count()
    
    # Calculate students with interventions
    students_with_interventions = InterventionPlan.objects.filter(
        student__in=students,
        school_year=current_sy,
        is_active=True
    ).values('student').distinct().count()
    
    # Calculate Tier 3 escalations (students needing adviser intervention)
    tier3_count = InterventionPlan.objects.filter(
        student__in=students,
        school_year=current_sy,
        current_tier='Tier 3',
        is_active=True
    ).values('student').distinct().count()
    
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
        'section_id': advisory_section.id,
        
        # Stats
        'total_students': total_students,
        'male_count': male_count,
        'female_count': female_count,
        'students_with_interventions': students_with_interventions,
        'tier3_count': tier3_count,
        
        # Current quarter
        'current_quarter': 'Q1',
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
        'current_sy': current_sy,
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
def get_subject_interventions(request):
    """
    Get all subject teacher interventions for adviser's advisory class
    Returns one row per subject intervention (not combined)
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    section_id = request.GET.get('section_id')
    quarter = request.GET.get('quarter', 'Q1')
    
    if not section_id:
        return JsonResponse({'success': False, 'error': 'Section ID required'})
    
    section = get_object_or_404(Section, id=section_id)
    current_sy = SchoolYear.get_current()
    
    # Get all students in this section
    students = Student.objects.filter(
        masterlist_entries__masterlist__section=section,
        masterlist_entries__is_active=True
    ).distinct()
    
    # Get all InterventionPlan records (subject teacher interventions)
    interventions = InterventionPlan.objects.filter(
        student__in=students,
        quarter=quarter,
        school_year=current_sy,
        is_active=True
    ).select_related('student', 'subject', 'created_by', 'section')
    
    # Build response data (one row per subject)
    data = []
    for intervention in interventions:
        # Fetch the latest action to determine the tier
        latest_action = InterventionAction.objects.filter(
            intervention_plan=intervention
        ).order_by('-id').first()
        
        intervention_tier = latest_action.tier if latest_action else intervention.current_tier
        
        # Check if adviser has already created intervention for this student
        adviser_intervention = Intervention.objects.filter(
            student=intervention.student,
            quarter=quarter,
            related_subject_intervention=intervention,
            is_active=True
        ).first()
        
        data.append({
            'id': intervention.id,
            'student_id': intervention.student.id,
            'student_name': f"{intervention.student.last_name}, {intervention.student.first_name} {intervention.student.middle_name}".strip(),
            'lrn': intervention.student.lrn,
            'sex': intervention.student.gender,
            'age': intervention.student.age,
            'subject': intervention.subject.subject_name,
            'subject_id': intervention.subject.id,
            'current_grade': intervention.current_grade,
            'absences': intervention.total_absences,
            'missing_ww': intervention.missing_written_works,
            'missing_pt': intervention.missing_performance_tasks,
            'missing_work': intervention.missing_written_works + intervention.missing_performance_tasks,
            'missed_qa': intervention.missed_quarterly_assessment,
            'risk_level': intervention.risk_level,
            'tier': intervention_tier,
            'created_by': intervention.created_by.full_name,
            'created_at': intervention.created_at.isoformat(),
            'is_tier_3': intervention_tier == 'Tier 3',
            'has_adviser_intervention': adviser_intervention is not None,
            'adviser_intervention_id': adviser_intervention.id if adviser_intervention else None,
        })
    
    return JsonResponse({
        'success': True,
        'interventions': data
    })


@login_required
@require_http_methods(["GET"])
def get_intervention_details(request, intervention_id):
    """
    Get detailed information about a subject teacher intervention (read-only)
    """
    try:
        intervention = get_object_or_404(InterventionPlan, id=intervention_id)
        
        # Get all actions for this intervention
        actions = InterventionAction.objects.filter(
            intervention_plan=intervention
        ).select_related('handled_by').order_by('-start_date')
        
        actions_data = [{
            'id': action.id,
            'tier': action.tier,
            'action_type': action.action_type,
            'action_name': action.action_name,
            'description': action.description,
            'start_date': action.start_date.strftime('%Y-%m-%d'),
            'target_date': action.target_date.strftime('%Y-%m-%d') if action.target_date else '',
            'status': action.status,
            'progress_notes': action.progress_notes,
            'teacher_notes': action.teacher_notes,
            'handled_by': action.handled_by.full_name,
        } for action in actions]
        
        # Check the latest action to determine the correct tier
        latest_action = actions.first()
        intervention_tier = latest_action.tier if latest_action else intervention.current_tier
        
        # Check if adviser intervention exists
        adviser_intervention = Intervention.objects.filter(
            related_subject_intervention=intervention,
            is_active=True
        ).first()
        
        return JsonResponse({
            'success': True,
            'intervention': {
                'id': intervention.id,
                'student_name': f"{intervention.student.last_name}, {intervention.student.first_name}",
                'subject': intervention.subject.subject_name,
                'risk_level': intervention.risk_level,
                'tier': intervention_tier,
                'current_grade': intervention.current_grade,
                'total_absences': intervention.total_absences,
                'missing_ww': intervention.missing_written_works,
                'missing_pt': intervention.missing_performance_tasks,
                'missed_qa': intervention.missed_quarterly_assessment,
                'risk_factors': intervention.get_risk_factors(),
                'created_by': intervention.created_by.full_name,
                'created_at': intervention.created_at.isoformat(),
            },
            'actions': actions_data,
            'has_adviser_intervention': adviser_intervention is not None,
            'adviser_intervention_id': adviser_intervention.id if adviser_intervention else None,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_http_methods(["POST"])
def create_adviser_intervention(request):
    """
    Create adviser intervention from Tier 3 escalation
    Fixed version with proper data handling
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Teacher profile not found'})
    
    try:
        data = json.loads(request.body)
        
        student_id = data.get('student_id')
        quarter = data.get('quarter', 'Q1')
        intervention_plan_id = data.get('intervention_plan_id')  # Single intervention ID
        
        if not student_id:
            return JsonResponse({'success': False, 'error': 'Student ID required'})
        
        student = get_object_or_404(Student, id=student_id)
        
        # Get the specific InterventionPlan
        intervention_plan = None
        if intervention_plan_id:
            intervention_plan = InterventionPlan.objects.filter(
                id=intervention_plan_id,
                student=student,
                is_active=True
            ).first()
        
        # Check if adviser intervention already exists
        existing = Intervention.objects.filter(
            student=student,
            quarter=quarter,
            created_by=teacher,
            is_active=True
        ).first()
        
        if existing:
            return JsonResponse({
                'success': False, 
                'error': 'Adviser intervention already exists for this student in this quarter',
                'intervention_id': existing.id
            })
        
        # Parse dates
        start_date = None
        if data.get('date_contacted'):
            try:
                start_date = datetime.strptime(data['date_contacted'], '%Y-%m-%d').date()
            except:
                start_date = datetime.now().date()
        else:
            start_date = datetime.now().date()
        
        review_date = None
        if data.get('meeting_date'):
            try:
                review_date = datetime.strptime(data['meeting_date'], '%Y-%m-%d').date()
            except:
                pass
        
        # Get reason and action_plan from the request
        reason = data.get('reason', 'Tier 3 Escalation - Requires parent involvement')
        action_plan = data.get('action_plan', '')
        
        # Create adviser intervention
        intervention = Intervention.objects.create(
            student=student,
            created_by=teacher,
            intervention_type='Tier 3 Escalation',
            quarter=quarter,
            start_date=start_date,
            review_date=review_date,
            reason=reason,
            smart_goal=action_plan,
            is_active=True,
            related_subject_intervention=intervention_plan
        )
        
        # Create initial update with meeting details
        parent_name = data.get('parent_name', 'N/A')
        parent_contact = data.get('parent_contact', 'N/A')
        contact_method = data.get('contact_method', 'N/A')
        additional_notes = data.get('notes', '')  # Get from Additional Notes field
        
        initial_note = f"""TIER 3 ESCALATION - ADVISER INTERVENTION

Parent/Guardian Information:
- Name: {parent_name}
- Contact Number: {parent_contact}
- Contact Method: {contact_method}

Meeting Details:
- Date Contacted: {start_date.strftime('%B %d, %Y')}
- Meeting Date: {review_date.strftime('%B %d, %Y') if review_date else 'To be scheduled'}

Action Plan:
{action_plan}

Additional Notes:
{additional_notes if additional_notes else 'None'}
        """.strip()
        
        # Create the update record
        InterventionUpdate.objects.create(
            intervention=intervention,
            date=start_date,
            status='No change',
            note=initial_note,
            created_by=teacher
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Adviser intervention created successfully',
            'intervention_id': intervention.id,
            'redirect_url': '/teacher/adviser-adviser-intervention/'  # Redirect to adviser intervention page
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("ERROR CREATING INTERVENTION:")
        print(error_details)
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


@login_required
@require_http_methods(["GET"])
def get_tier3_interventions_for_student(request, student_id):
    """
    Get all Tier 3 interventions for a student (for combining into one adviser intervention)
    """
    try:
        quarter = request.GET.get('quarter', 'Q1')
        current_sy = SchoolYear.get_current()
        
        student = get_object_or_404(Student, id=student_id)
        
        # Get all Tier 3 interventions for this student
        interventions = InterventionPlan.objects.filter(
            student=student,
            quarter=quarter,
            school_year=current_sy,
            current_tier='Tier 3',
            is_active=True
        ).select_related('subject', 'created_by')
        
        data = [{
            'id': interv.id,
            'subject': interv.subject.subject_name,
            'risk_level': interv.risk_level,
            'current_grade': interv.current_grade,
            'absences': interv.total_absences,
            'missing_work': interv.missing_written_works + interv.missing_performance_tasks,
            'risk_factors': interv.get_risk_factors(),
            'created_by': interv.created_by.full_name,
        } for interv in interventions]
        
        return JsonResponse({
            'success': True,
            'interventions': data,
            'student_name': f"{student.last_name}, {student.first_name}",
            'lrn': student.lrn,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Additional views for adviser_intervention.html page (if needed)
@login_required
@require_http_methods(["GET"])
def get_interventions(request):
    """
    Get all interventions created by adviser (for adviser_intervention.html page)
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    # Get advisory section
    advisory_section = Section.objects.filter(adviser=teacher, is_active=True).first()
    if not advisory_section:
        return JsonResponse({'interventions': []})
    
    # Get quarter filter
    quarter = request.GET.get('quarter', 'Q1')
    
    # Get students in this section
    students = Student.objects.filter(
        masterlist_entries__masterlist__section=advisory_section,
        masterlist_entries__is_active=True
    ).distinct()
    student_ids = students.values_list('id', flat=True)
    
    # Get adviser interventions (Intervention model, not InterventionPlan)
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
        
        # Get linked subject intervention if exists
        linked_subject = None
        if intervention.related_subject_intervention:
            linked_subject = {
                'subject': intervention.related_subject_intervention.subject.subject_name,
                'tier': intervention.related_subject_intervention.current_tier,
            }
        
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
            'updates': updates,
            'linked_subject_intervention': linked_subject,
        })
    
    return JsonResponse({'interventions': data})


@login_required
@require_http_methods(["POST"])
def create_intervention(request):
    """
    Create a new adviser intervention (from adviser_intervention.html page)
    Legacy endpoint - kept for compatibility
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        
        # Parse student name
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
            intervention_type='General',
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
    Add update to adviser intervention
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
        
        update_date = datetime.now().date()
        if data.get('date'):
            try:
                update_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        update = InterventionUpdate.objects.create(
            intervention=intervention,
            date=update_date,
            status=data.get('status', 'No change'),
            note=data.get('note', ''),
            created_by=teacher
        )
        
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
    Delete (soft delete) adviser intervention
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        intervention = Intervention.objects.get(id=intervention_id, created_by=teacher)
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
    Delete intervention update
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        update = InterventionUpdate.objects.get(id=update_id)
        intervention = update.intervention
        
        if intervention.created_by != teacher:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        update.delete()
        
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