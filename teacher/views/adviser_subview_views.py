# teacher/views/adviser_subview_views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json

from admin_functionalities.models import Teacher, Section, SectionSubjectAssignment, SchoolYear


@login_required
def adviser_subview(request):
    """
    Subject Teacher Dashboard with section selection modal.
    Once a section is selected, it persists across all modules.
    """
    try:
        teacher = request.user.teacher_profile
    except:
        return render(request, 'teacher/error.html', {
            'message': 'Teacher profile not found'
        })
    
    # Get current school year
    current_sy = SchoolYear.get_current()
    
    # Get all sections where teacher has assignments
    taught_section_ids = SectionSubjectAssignment.objects.filter(
        teacher=teacher
    ).values_list('section_id', flat=True).distinct()
    
    sections = Section.objects.filter(
        id__in=taught_section_ids,
        is_active=True
    ).order_by('name')
    
    # Get currently selected section from session (if exists)
    selected_section_id = request.session.get('selected_section_id')
    selected_section = None
    
    if selected_section_id:
        try:
            selected_section = Section.objects.get(id=selected_section_id)
        except Section.DoesNotExist:
            # Clear invalid session data
            request.session.pop('selected_section_id', None)
            request.session.pop('selected_section_name', None)
    
    # Get subjects taught by this teacher per section
    sections_with_subjects = {}
    for section in sections:
        assignments = SectionSubjectAssignment.objects.filter(
            teacher=teacher,
            section=section
        ).select_related('subject')  # Optimize query
        
        subjects = []
        for assignment in assignments:
            # Since subject is a ForeignKey, access it directly
            subjects.append({
                'code': assignment.subject.subject_code,
                'name': assignment.subject.subject_name
            })
        
        sections_with_subjects[section.id] = {
            'section': section,
            'subjects': subjects,
            'student_count': section.current_students  # Use the actual field from your model
        }
    
    context = {
        'teacher': teacher,
        'sections': sections,
        'sections_with_subjects': sections_with_subjects,
        'selected_section': selected_section,
        'current_sy': current_sy,
        'show_modal': selected_section is None,  # Show modal if no section selected
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
    }
    
    return render(request, 'teacher/adviser/Subject_Teacher_View.html', context)


@login_required
@require_POST
def set_active_section(request):
    """
    Set the active section in session.
    This section will be used across all modules.
    """
    try:
        teacher = request.user.teacher_profile
        data = json.loads(request.body)
        section_id = data.get('section_id')
        
        if not section_id:
            return JsonResponse({
                'success': False,
                'error': 'Section ID is required'
            }, status=400)
        
        # Verify teacher has access to this section
        section = get_object_or_404(Section, id=section_id, is_active=True)
        
        has_access = SectionSubjectAssignment.objects.filter(
            teacher=teacher,
            section=section
        ).exists()
        
        if not has_access:
            return JsonResponse({
                'success': False,
                'error': 'You do not have access to this section'
            }, status=403)
        
        # Set in session
        request.session['selected_section_id'] = section.id
        request.session['selected_section_name'] = section.name
        request.session['selected_section_program'] = section.program.name  # ForeignKey to Program
        
        # Get subjects for this section
        assignments = SectionSubjectAssignment.objects.filter(
            teacher=teacher,
            section=section
        ).select_related('subject')
        
        subject_codes = []
        subject_names = []
        
        for assignment in assignments:
            subject_codes.append(assignment.subject.subject_code)
            subject_names.append(assignment.subject.subject_name)
        
        return JsonResponse({
            'success': True,
            'message': f'Now working on {section.name}',
            'section': {
                'id': section.id,
                'name': section.name,
                'program': section.program.name,
                'subjects': subject_codes,
                'subject_names': subject_names
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_active_section(request):
    """
    Get the currently active section from session.
    """
    try:
        selected_section_id = request.session.get('selected_section_id')
        
        if not selected_section_id:
            return JsonResponse({
                'success': False,
                'error': 'No section selected',
                'has_section': False
            })
        
        section = get_object_or_404(Section, id=selected_section_id)
        
        # Get subjects
        teacher = request.user.teacher_profile
        assignments = SectionSubjectAssignment.objects.filter(
            teacher=teacher,
            section=section
        ).select_related('subject')
        
        subject_codes = [assignment.subject.subject_code for assignment in assignments]
        
        return JsonResponse({
            'success': True,
            'has_section': True,
            'section': {
                'id': section.id,
                'name': section.name,
                'program': section.program.name,
                'building': section.building,
                'room': section.room,
                'subjects': subject_codes
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def clear_active_section(request):
    """
    Clear the active section from session.
    """
    request.session.pop('selected_section_id', None)
    request.session.pop('selected_section_name', None)
    request.session.pop('selected_section_program', None)
    
    return JsonResponse({
        'success': True,
        'message': 'Section selection cleared'
    })