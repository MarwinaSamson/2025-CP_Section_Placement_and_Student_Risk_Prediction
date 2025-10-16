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

    
# admin_functionalities/urls.py (RECOMMENDED VERSION - No Conflicts)
from django.urls import path
from . import views

app_name = 'admin_functionalities'

urlpatterns = [
    # Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    
    # Enrollment Management
    path('enrollment/', views.enrollment_view, name='enrollment'),
    path('enrollment/student/<int:student_id>/edit/', views.student_edit_view, name='student_edit'),
    
    # Notifications
    path('mark-read/', views.mark_notification_read, name='mark_notification_read'),
    
    # ============ ALL SETTINGS RELATED PATHS ============
    path('settings/', views.settings_view, name='settings'),
    path('settings/add-user/', views.AddUserView.as_view(), name='add_user'),
    path('settings/get-users/', views.get_users_data, name='get_users_data'),
    path('settings/get-logs/', views.get_logs_data, name='get_logs_data'),
    path('settings/user/<int:user_id>/profile/', views.get_user_profile, name='get_user_profile'),
    
    # ============ ALL SECTIONS RELATED PATHS ============
    path('sections/', views.sections_view, name='sections'),  # Main sections page
    
    # AJAX endpoints for sections
    path('api/get-teachers/', views.get_teachers, name='get_teachers'),  # FIXED: Moved to /api/
    path('api/buildings-rooms/', views.get_buildings_rooms, name='get_buildings_rooms'),  # FIXED: Moved to /api/
    
    # Section CRUD operations
    path('sections/<str:program>/', views.get_sections_by_program, name='get_sections_by_program'),
    path('sections/add/<str:program>/', views.add_section, name='add_section'),
    path('sections/update/<int:section_id>/', views.update_section, name='update_section'),
    path('sections/delete/<int:section_id>/', views.delete_section, name='delete_section'),
    path('sections/assign-subjects/<int:section_id>/', views.assign_subject_teachers, name='assign_subject_teachers'),
    
    # ============ ALL TEACHERS RELATED PATHS ============
    path('teachers/', views.teachers_view, name='teachers'),  # Teachers management page
]