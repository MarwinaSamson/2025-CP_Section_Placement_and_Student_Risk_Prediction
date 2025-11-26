# ============================================================================
# 7. admin_functionalities/views/settings_views.py
# ============================================================================
"""
Settings and user management views.
"""

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from django.views import View

from admin_functionalities.models import ActivityLog, AddUserLog
from admin_functionalities.forms import AddUserForm
from admin_functionalities.utils import log_activity
from .utils import _get_user_role

CustomUser = get_user_model()


@method_decorator(login_required, name='dispatch')
class AddUserView(View):
    """View for adding new users."""
    
    def get(self, request):
        return redirect(reverse('admin_functionalities:settings'))

    def post(self, request):
        print(f"=== DEBUG: POST received in AddUserView ===")
        form = AddUserForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                user = form.save(created_by_user=request.user)
                
                log_activity(request.user, "Settings", f"Added new user {user.username}")

                # JSON Response for AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'User {user.first_name} {user.last_name} added successfully!',
                        'user': {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'is_superuser': user.is_superuser,
                            'is_staff_expert': getattr(user, 'is_staff_expert', False),
                            'is_subject_teacher': getattr(user, 'is_subject_teacher', False),
                            'is_adviser': getattr(user, 'is_adviser', False),
                            'date_joined_formatted': user.date_joined.strftime("%B %d, %Y"),
                        }
                    })

                return redirect(reverse('admin_functionalities:settings'))

            except Exception as save_err:
                print(f"=== ERROR: {save_err} ===")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': str(save_err)}, status=500)
                from django.contrib import messages
                messages.error(request, f"Error saving user: {save_err}")
                return redirect(reverse('admin_functionalities:settings'))
        else:
            print("=== DEBUG: Invalid form ===", form.errors)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            from django.contrib import messages
            messages.error(request, 'Form validation failed.')
            return redirect(reverse('admin_functionalities:settings'))


@login_required
def settings_view(request):
    """Main settings page with users and activity logs."""
    users = CustomUser.objects.filter(is_active=True)
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:50]
    return render(request, 'admin_functionalities/settings.html', {
        'users': users,
        'logs': logs,
        'active_page': 'settings'
    })


@login_required
def get_user_profile(request, user_id):
    """Get detailed user profile data."""
    try:
        user = CustomUser.objects.get(id=user_id, is_active=True)
        teacher = getattr(user, 'teacher_profile', None)

        profile_data = {
            'full_name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'employee_id': user.employee_id or 'Not provided',
            'position': user.position or 'Not specified',
            'department': user.department or 'Not provided',
            'profile_photo': (teacher.profile_photo.url if teacher and teacher.profile_photo else None),
            'date_of_birth': (teacher.date_of_birth.strftime('%B %d, %Y') if teacher and teacher.date_of_birth else 'Not provided – Update your profile'),
            'gender': (teacher.gender if teacher else 'Not provided – Update your profile'),
            'phone_number': (teacher.phone if teacher and teacher.phone else user.phone_number or 'Not provided – Update your profile'),
            'address': (teacher.address if teacher and teacher.address else user.address or 'Not provided – Update your profile'),
            'age': (teacher.age if teacher and teacher.age else 'Not provided – Update your profile'),
            'is_subject_teacher': user.is_subject_teacher,
            'is_adviser': user.is_adviser,
            'roles_summary': f"Subject Teacher: {'Yes' if user.is_subject_teacher else 'No'} | Adviser: {'Yes' if user.is_adviser else 'No'}" if user.is_teacher else 'N/A (Non-Teacher Role)',
            'subjects_taught': (teacher.subjects_taught if teacher else 'To be assigned – Update your profile'),
            'classes_handled': (teacher.classes_handled if teacher else 'To be assigned – Update your profile'),
            'change_history': list(AddUserLog.objects.filter(user=user).values('action', 'date', 'time')[:3]) or [
                {'action': 'Account Created', 'date': user.date_joined.strftime('%m/%d/%Y'), 'time': user.date_joined.strftime('%I:%M %p')}
            ],
        }
        return JsonResponse({'success': True, 'data': profile_data})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)


@login_required
def get_users_data(request):
    """Get all users data for display."""
    users = CustomUser.objects.filter(is_active=True).order_by('-id')

    user_data = []
    for user in users:
        user_data.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff_expert': getattr(user, 'is_staff_expert', False),
            'is_subject_teacher': getattr(user, 'is_subject_teacher', False),
            'is_adviser': getattr(user, 'is_adviser', False),
            'date_joined_formatted': user.date_joined.strftime("%B %d, %Y"),
            'last_login_formatted': user.last_login.strftime("%B %d, %Y") if user.last_login else None,
        })

    return JsonResponse({'users': user_data})


@login_required
def get_logs_data(request):
    """Fetch recent activity logs for the History tab."""
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:50]

    data = []
    for log in logs:
        local_time = localtime(log.timestamp)
        data.append({
            'user_full_name': f"{log.user.first_name} {log.user.last_name}".strip() or log.user.username,
            'user_role': _get_user_role(log.user),
            'action': log.action,
            'date_formatted': local_time.strftime("%B %d, %Y"),
            'time_formatted': local_time.strftime("%I:%M %p"),
        })

    return JsonResponse({'logs': data})
