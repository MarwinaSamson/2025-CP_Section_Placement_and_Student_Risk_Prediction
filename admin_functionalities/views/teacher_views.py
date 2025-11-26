# ============================================================================
# 5. admin_functionalities/views/teacher_views.py
# ============================================================================
"""
Teacher management views.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from admin_functionalities.models import Teacher


@login_required
def teachers_view(request):
    """Main teachers management page."""
    teachers = Teacher.objects.order_by('last_name', 'first_name')
    teachers_data = []
    
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
        })
    
    context = {
        'teachers': teachers_data,
    }
    
    return render(request, 'admin_functionalities/teachers.html', context)

