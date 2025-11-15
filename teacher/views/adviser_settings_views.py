from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from datetime import datetime, date
from admin_functionalities.models import Teacher, ChangeHistory, CustomUser
import json


@login_required
def adviser_settings(request):
    """
    Display the teacher's profile settings page.
    Fetches all data dynamically from the database.
    """
    try:
        # Get the logged-in user's teacher profile
        teacher = Teacher.objects.select_related('user').get(user=request.user)
        
        # Get teaching load (sections where this teacher is adviser or subject teacher)
        teaching_load = []
        
        # Get sections where teacher is adviser
        adviser_sections = teacher.adviser_sections.all()
        for section in adviser_sections:
            teaching_load.append({
                'subject': f'Adviser - {section.program}',
                'grade_section': f'{section.program} – {section.name}',
                'num_students': section.current_students
            })
        
        # Get sections where teacher is subject teacher
        subject_assignments = teacher.assigned_subjects.select_related('section').all()
        for assignment in subject_assignments:
            teaching_load.append({
                'subject': assignment.get_subject_display(),
                'grade_section': f'{assignment.section.program} – {assignment.section.name}',
                'num_students': assignment.section.current_students
            })
        
        # Get change history
        change_history = teacher.change_history.all().order_by('-date', '-time')[:10]
        
        # Format data for template
        context = {
            'teacher': teacher,
            'teaching_load': teaching_load,
            'change_history': change_history,
            'user': request.user,
        }
        
        return render(request, 'teacher/adviser/Setting.html', context)
        
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found. Please contact administrator.")
        return redirect('teacher:bothaccess-dashboard')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('teacher:bothaccess-dashboard')


@login_required
@require_http_methods(["POST"])
def update_teacher_data(request):
    """
    Update teacher's personal data via AJAX.
    Returns JSON response.
    """
    try:
        teacher = get_object_or_404(Teacher, user=request.user)
        
        with transaction.atomic():
            # Update personal data
            teacher.employee_id = request.POST.get('employee_id', teacher.employee_id)
            teacher.last_name = request.POST.get('last_name', teacher.last_name)
            teacher.first_name = request.POST.get('first_name', teacher.first_name)
            teacher.middle_name = request.POST.get('middle_name', teacher.middle_name)
            teacher.position = request.POST.get('position', teacher.position)
            teacher.department = request.POST.get('department', teacher.department)
            teacher.gender = request.POST.get('gender', teacher.gender)
            teacher.employment_status = request.POST.get('employment_status', teacher.employment_status)
            
            # Handle date of birth
            dob_str = request.POST.get('date_of_birth')
            if dob_str:
                try:
                    teacher.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Handle profile photo upload
            if 'profile_photo' in request.FILES:
                photo = request.FILES['profile_photo']
                # Delete old photo if exists
                if teacher.profile_photo:
                    try:
                        default_storage.delete(teacher.profile_photo.path)
                    except:
                        pass
                teacher.profile_photo = photo
            
            teacher.save()
            
            # Create change history entry
            ChangeHistory.objects.create(
                teacher=teacher,
                action='updated',
                description='Profile data updated'
            )
            
            # Format response data
            response_data = {
                'success': True,
                'message': 'Teacher data updated successfully',
                'data': {
                    'employee_id': teacher.employee_id,
                    'last_name': teacher.last_name,
                    'first_name': teacher.first_name,
                    'middle_name': teacher.middle_name,
                    'full_name': teacher.full_name,
                    'position': teacher.position,
                    'department': teacher.department,
                    'gender': teacher.get_gender_display(),
                    'date_of_birth': teacher.date_of_birth.strftime('%B %d, %Y') if teacher.date_of_birth else '',
                    'age': teacher.age if teacher.age else '',
                    'employment_status': teacher.employment_status,
                    'profile_photo': teacher.profile_photo.url if teacher.profile_photo else ''
                }
            }
            
            return JsonResponse(response_data)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating teacher data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def update_contact_data(request):
    """
    Update teacher's contact information via AJAX.
    Returns JSON response.
    """
    try:
        teacher = get_object_or_404(Teacher, user=request.user)
        
        with transaction.atomic():
            # Update contact data
            teacher.email = request.POST.get('email', teacher.email)
            teacher.phone = request.POST.get('phone', teacher.phone)
            teacher.address = request.POST.get('address', teacher.address)
            
            teacher.save()
            
            # Create change history entry
            ChangeHistory.objects.create(
                teacher=teacher,
                action='updated',
                description='Contact data updated'
            )
            
            response_data = {
                'success': True,
                'message': 'Contact data updated successfully',
                'data': {
                    'email': teacher.email,
                    'phone': teacher.phone,
                    'address': teacher.address
                }
            }
            
            return JsonResponse(response_data)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating contact data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def get_change_history(request):
    """
    Get paginated change history for the teacher.
    Returns JSON response.
    """
    try:
        teacher = get_object_or_404(Teacher, user=request.user)
        
        # Get pagination parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        
        # Get change history
        history = teacher.change_history.all().order_by('-date', '-time')[offset:offset + limit]
        
        history_data = []
        for entry in history:
            history_data.append({
                'action': entry.get_action_display(),
                'description': entry.description,
                'date': entry.date.strftime('%m/%d/%Y'),
                'time': entry.time.strftime('%I:%M %p')
            })
        
        return JsonResponse({
            'success': True,
            'data': history_data,
            'has_more': teacher.change_history.count() > (offset + limit)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching history: {str(e)}'
        }, status=400)