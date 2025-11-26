# ============================================================================
# 1. admin_functionalities/views/__init__.py
# ============================================================================
"""
Views package for admin functionalities.
Imports all views to maintain backward compatibility with existing urls.py
"""

from .dashboard_views import admin_dashboard
from .section_views import (
    sections_view,
    get_teachers,
    get_subject_teachers,
    get_buildings_rooms,
    get_sections_by_program,
    add_section,
    update_section,
    delete_section,
    get_section_students,
    section_masterlist,
    assign_subject_teachers,
)
from .teacher_views import teachers_view
from .enrollment_views import enrollment_view, mark_notification_read
from .settings_views import (
    AddUserView,
    settings_view,
    get_user_profile,
    get_users_data,
    get_logs_data,
)
from .student_views import (
    student_edit_view,
    StudentAcademicUpdateView,
)

__all__ = [
    # Dashboard
    'admin_dashboard',
    
    # Sections
    'sections_view',
    'get_teachers',
    'get_subject_teachers',
    'get_buildings_rooms',
    'get_sections_by_program',
    'add_section',
    'update_section',
    'delete_section',
    'get_section_students',
    'section_masterlist',
    'assign_subject_teachers',
    
    # Teachers
    'teachers_view',
    
    # Enrollment
    'enrollment_view',
    'mark_notification_read',
    
    # Settings
    'AddUserView',
    'settings_view',
    'get_user_profile',
    'get_users_data',
    'get_logs_data',
    
    # Students
    'student_edit_view',
    'StudentAcademicUpdateView',
]