#  # admin_functionalities/urls.py
# from django.urls import path
# from . import views
# from .views import StudentAcademicUpdateView

# app_name = 'admin_functionalities' # Namespace for your app's URLs

# urlpatterns = [
    
#         path('', views.admin_dashboard, name='dashboard'),
       
#     ]# admin_functionalities/urls.py

# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views

# app_name = 'admin_functionalities'

# urlpatterns = [
#     #path('login/', views.admin_login, name='login'),
#     # path('logout/', views.custom_logout, name='logout'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
#     #path('sections/', views.sections_view, name='sections'),
#     # path('teachers/', views.teachers_view, name='teachers'),
#     path('enrollment/', views.enrollment_view, name='enrollment'),
#     path('mark-read/', views.mark_notification_read, name='mark_notification_read'),
#     path('enrollment/student/<int:student_id>/edit/', views.student_edit_view, name='student_edit'),
    
#     # ALL SETTINGS RELATED PATHS ARE HERE   
#     path('settings/', views.settings_view, name='settings'),   
#     path('settings/add-user/', views.AddUserView.as_view(), name='add_user'),   
#     # NEW AJAX ENDPOINTS FOR DYNAMIC TABLES
#     path('settings/get-users/', views.get_users_data, name='get_users_data'),
#     path('settings/get-logs/', views.get_logs_data, name='get_logs_data'),

   
#     # ALL SECTIONS RELATED PATHS ARE HERE
#     path('sections/', views.sections_view, name='sections'),  # Renders template
    
    
#     # ALL TEACHERS UPDATE RELATED PATHS ARE HERE
#     path('teachers/', views.teachers_view, name='teachers'),  # Renders template (you already have this)
#     # path('teachers/<int:teacher_id>/profile/', views.get_teacher_profile, name='get_teacher_profile'),
# ]

    
# # admin_functionalities/urls.py (RECOMMENDED VERSION - No Conflicts)
# from django.urls import path
# from . import views

# app_name = 'admin_functionalities'

# urlpatterns = [
#     # Dashboard
#     path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    
#     # Enrollment Management
#     path('enrollment/', views.enrollment_view, name='enrollment'),
#     path('enrollment/student/<int:student_id>/edit/', views.student_edit_view, name='student_edit'),
    
#     # Notifications
#     path('mark-read/', views.mark_notification_read, name='mark_notification_read'),
    
#     # ============ ALL SETTINGS RELATED PATHS ============
#     path('settings/', views.settings_view, name='settings'),
#     path('settings/add-user/', views.AddUserView.as_view(), name='add_user'),
#     path('settings/get-users/', views.get_users_data, name='get_users_data'),
#     path('settings/get-logs/', views.get_logs_data, name='get_logs_data'),
#     path('settings/user/<int:user_id>/profile/', views.get_user_profile, name='get_user_profile'),
    
#     # ============ ALL SECTIONS RELATED PATHS ============
#     path('sections/', views.sections_view, name='sections'),  # Main sections page
    
#     # AJAX endpoints for sections
#     path('api/get-teachers/', views.get_teachers, name='get_teachers'),  # FIXED: Moved to /api/
#     path('api/buildings-rooms/', views.get_buildings_rooms, name='get_buildings_rooms'),  # FIXED: Moved to /api/
    
#     # Section CRUD operations
#     path('sections/<str:program>/', views.get_sections_by_program, name='get_sections_by_program'),
#     path('sections/add/<str:program>/', views.add_section, name='add_section'),
#     path('sections/update/<int:section_id>/', views.update_section, name='update_section'),
#     path('sections/delete/<int:section_id>/', views.delete_section, name='delete_section'),
#     path('sections/assign-subjects/<int:section_id>/', views.assign_subject_teachers, name='assign_subject_teachers'),
#     path('sections/<int:section_id>/masterlist/', views.section_masterlist, name='section_masterlist'),
#     path('api/get-subject-teachers/', views.get_subject_teachers, name='get_subject_teachers'),
    
#     # ============ ALL TEACHERS RELATED PATHS ============
#     path('teachers/', views.teachers_view, name='teachers'),  # Teachers management page
# ]

# admin_functionalities/urls.py
"""
URL Configuration for Admin Functionalities
All imports are explicit to show which module each view comes from.
"""

from django.urls import path

# Dashboard views
from .views.dashboard_views import admin_dashboard

# Enrollment views
from .views.enrollment_views import (
    enrollment_view,
    mark_notification_read,
)

# Student views
from .views.student_views import (
    student_edit_view,
    StudentAcademicUpdateView,
)

# Settings views
from .views.settings_views import (
    AddUserView,
    settings_view,
    get_users_data,
    get_logs_data,
    get_user_profile,
)

# Section views
from .views.section_views import (
    sections_view,
    get_teachers,
    get_subject_teachers,
    get_buildings_rooms,
    get_sections_by_program,
    add_section,
    update_section,
    delete_section,
    get_section_students,
    assign_subject_teachers,
    section_masterlist,
)

# Teacher views
from .views.teacher_views import teachers_view

app_name = 'admin_functionalities'

urlpatterns = [
    # ============================================================================
    # DASHBOARD
    # ============================================================================
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    
    # ============================================================================
    # ENROLLMENT MANAGEMENT
    # ============================================================================
    path('enrollment/', enrollment_view, name='enrollment'),
    path('enrollment/student/<int:student_id>/edit/', student_edit_view, name='student_edit'),
    
    # ============================================================================
    # NOTIFICATIONS
    # ============================================================================
    path('mark-read/', mark_notification_read, name='mark_notification_read'),
    
    # ============================================================================
    # SETTINGS & USER MANAGEMENT
    # ============================================================================
    path('settings/', settings_view, name='settings'),
    path('settings/add-user/', AddUserView.as_view(), name='add_user'),
    path('settings/get-users/', get_users_data, name='get_users_data'),
    path('settings/get-logs/', get_logs_data, name='get_logs_data'),
    path('settings/user/<int:user_id>/profile/', get_user_profile, name='get_user_profile'),
    
    # ============================================================================
    # SECTIONS MANAGEMENT
    # ============================================================================
    # Main page
    path('sections/', sections_view, name='sections'),
    
    # AJAX/API endpoints
    path('api/get-teachers/', get_teachers, name='get_teachers'),
    path('api/get-subject-teachers/', get_subject_teachers, name='get_subject_teachers'),
    path('api/buildings-rooms/', get_buildings_rooms, name='get_buildings_rooms'),
    
    # Section CRUD operations
    path('sections/<str:program>/', get_sections_by_program, name='get_sections_by_program'),
    path('sections/add/<str:program>/', add_section, name='add_section'),
    path('sections/update/<int:section_id>/', update_section, name='update_section'),
    path('sections/delete/<int:section_id>/', delete_section, name='delete_section'),
    path('sections/<int:section_id>/students/', get_section_students, name='get_section_students'),
    path('sections/<int:section_id>/masterlist/', section_masterlist, name='section_masterlist'),
    path('sections/assign-subjects/<int:section_id>/', assign_subject_teachers, name='assign_subject_teachers'),
    
    # ============================================================================
    # TEACHERS MANAGEMENT
    # ============================================================================
    path('teachers/', teachers_view, name='teachers'),
    
    # ============================================================================
    # STUDENT ACADEMIC (Class-based view)
    # ============================================================================
    path('student/<int:student_id>/academic/update/', 
         StudentAcademicUpdateView.as_view(), 
         name='student_academic_update'),
]