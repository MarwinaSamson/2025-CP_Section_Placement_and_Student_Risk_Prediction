# from django.urls import path
# from .views import subjectteacher_views, adviser_views, adviser_dashboard_views, adviser_view_views, adviser_masterlist_views, adviser_attendance_views, adviser_settings_views, adviser_learnersprofile_views

# app_name = 'teacher'

# urlpatterns = [ 
    
#     # ADVISER + SUBJECT TEACHER
#       path('bothaccess-dashboard/', adviser_dashboard_views.bothaccess_dashboard, name='bothaccess-dashboard'),  # Combined
#       path('adviserview/', adviser_view_views.adviser_view, name='adviser-view'),
#       path('adviserclass-record/', adviser_views.adviser_classrecord, name='adviser-classrecord'),
#       path('adviserintervention/', adviser_views.adviser_intervention, name='adviser-intervention'),
#       path('advisermasterlist/', adviser_masterlist_views.adviser_masterlist, name='adviser-masterlist'),
#       path('adviserattendance/', adviser_views.adviser_attendance, name='adviser-attendance'),
#       path('adviserreports/', adviser_views.adviser_reports, name='adviser-reports'),
#       path('advisersettings/', adviser_settings_views.adviser_settings, name='adviser-settings'),
#       path('advisersubview/', adviser_views.adviser_subview, name='adviser-subview'),
#       path('adviserlearnersprofile/', adviser_learnersprofile_views.adviser_learnerprofile, name='adviser-studentprofile'),
    
#     # INTERVENTION API ENDPOINTS (NEW)
#     path('api/interventions/', adviser_view_views.get_interventions, name='api-get-interventions'),
#     path('api/interventions/create/', adviser_view_views.create_intervention, name='api-create-intervention'),
#     path('api/interventions/<int:intervention_id>/update/', adviser_view_views.add_intervention_update, name='api-add-update'),
#     path('api/interventions/<int:intervention_id>/delete/', adviser_view_views.delete_intervention, name='api-delete-intervention'),
#     path('api/interventions/updates/<int:update_id>/delete/', adviser_view_views.delete_intervention_update, name='api-delete-update'),
    
    
#     # MASTERLIST API ENDPOINTS (NEW)
#     path('api/masterlist/student/<int:student_id>/grades/', adviser_masterlist_views.get_student_grades, name='api-student-grades'),
#     path('api/masterlist/student/<int:student_id>/status/', adviser_masterlist_views.update_student_status, name='api-update-status'),
#     path('api/masterlist/student/<int:student_id>/quarter/', adviser_masterlist_views.toggle_quarter_enrollment, name='api-toggle-quarter'),
     
   
#     # SETTINGS API ENDPOINTS (NEW)
#     path('api/settings/update-teacher/', adviser_settings_views.update_teacher_data, name='api-update-teacher-data'),
#     path('api/settings/update-contact/', adviser_settings_views.update_contact_data, name='api-update-contact-data'),
#     path('api/settings/change-history/', adviser_settings_views.get_change_history, name='api-change-history'),
    
#     # ATTENDANCE API ENDPOINTS (NEW)
    
    
    
#     #   SUBJECT TEACHER
#       path('subjectteacher-dashboard/', subjectteacher_views.subjectteacher_dashboard, name='subjectteacher-dashboard'),  # Subject only
#       path('settings/', subjectteacher_views.teacher_settings, name='teacher-settings'),
#       path('sub-teacher-view/', subjectteacher_views.sub_teacher_view, name='sub-teacher-view'),
#       path('class-record/', subjectteacher_views.sub_class_record, name='class-record'),
#       path('attendance/', subjectteacher_views.subject_teacher_attendance, name='subject-teacher-attendance'),
#       path('intervention/', subjectteacher_views.sub_intervention, name='intervention'),
#       path('viewclass/', subjectteacher_views.sub_viewclass, name='view-class'),
#   ]

# teacher/urls.py
from django.urls import path
from .views import subjectteacher_views, adviser_views, adviser_dashboard_views, adviser_view_views, adviser_masterlist_views, adviser_attendance_views, adviser_settings_views, adviser_learnersprofile_views, adviser_classrecord_views, adviser_subintervention_views, adviser_subview_views

app_name = 'teacher'

urlpatterns = [ 
    
    # ADVISER + SUBJECT TEACHER
    path('bothaccess-dashboard/', adviser_dashboard_views.bothaccess_dashboard, name='bothaccess-dashboard'),
    path('adviserview/', adviser_view_views.adviser_view, name='adviser-view'),
    path('adviserclass-record/', adviser_classrecord_views.adviser_classrecord, name='adviser-classrecord'),
    path('adviserintervention/', adviser_subintervention_views. adviser_sub_intervention, name='adviser-intervention'),
    path('advisermasterlist/', adviser_masterlist_views.adviser_masterlist, name='adviser-masterlist'),
    path('adviserattendance/', adviser_attendance_views.adviser_attendance, name='adviser-attendance'),  # Main page
    path('adviserreports/', adviser_views.adviser_reports, name='adviser-reports'),
    path('advisersettings/', adviser_settings_views.adviser_settings, name='adviser-settings'),
    path('advisersubview/', adviser_subview_views.adviser_subview, name='adviser-subview'),
    path('adviserlearnersprofile/', adviser_learnersprofile_views.adviser_learnerprofile, name='adviser-studentprofile'),
    path('adviser-adviser-intervention/', adviser_views.adviser_adviser_intervention, name='adviser-adviser-intervention'),
    path('adviser-viewclass/', adviser_views.adviser_viewclass, name='adviser-viewclass'),
    
     # Adviser View (Read-only subject interventions)
    path('adviser/view/', adviser_view_views.adviser_view, name='adviser_view'),
    path('adviser/view/interventions/', adviser_view_views.get_subject_interventions, name='get_subject_interventions'),
    path('adviser/view/intervention/<int:intervention_id>/', adviser_view_views.get_intervention_details, name='get_intervention_details'),
    path('adviser/view/tier3/<int:student_id>/', adviser_view_views.get_tier3_interventions_for_student, name='get_tier3_interventions'),
    path('adviser/view/create-intervention/', adviser_view_views.create_adviser_intervention, name='create_adviser_intervention'),
    
    # ===== ADVISER VIEW ENDPOINTS (Read-only subject interventions) =====
    # Get all subject teacher interventions for section
    path('adviser/view/interventions/', adviser_view_views.get_subject_interventions, name='get_subject_interventions'),
    # Get details of specific subject intervention
    path('adviser/view/intervention/<int:intervention_id>/', adviser_view_views.get_intervention_details, name='get_intervention_details'),
    # Get all Tier 3 interventions for a student
    path('adviser/view/tier3/<int:student_id>/', adviser_view_views.get_tier3_interventions_for_student, name='get_tier3_interventions'),
    # Create adviser intervention from Tier 3 escalation
    path('adviser/view/create-intervention/', adviser_view_views.create_adviser_intervention, name='create_adviser_intervention'),
    # ===== ADVISER INTERVENTION ENDPOINTS (Adviser-created interventions) =====
    path('adviser-sub-intervention/', adviser_subintervention_views.adviser_sub_intervention, name='adviser-sub-intervention'),
    # ===== SUBJECT TEACHER INTERVENTION SYSTEM ENDPOINTS =====
    path('api/intervention/students/', adviser_subintervention_views.get_intervention_students, name='api-intervention-students'),
    path('api/intervention/student/<int:student_id>/details/', adviser_subintervention_views.get_student_intervention_details, name='api-student-intervention-details'),
    path('api/intervention/action/create/', adviser_subintervention_views.create_intervention_action, name='api-create-intervention-action'),
    path('api/intervention/action/<int:action_id>/', adviser_subintervention_views.get_intervention_action, name='api-get-intervention-action'),
    path('api/intervention/action/<int:action_id>/update/', adviser_subintervention_views.update_intervention_action, name='api-update-intervention-action'),
    path('api/intervention/action/<int:action_id>/delete/', adviser_subintervention_views.delete_intervention_action, name='api-delete-intervention-action'),
    path('api/intervention/note/add/', adviser_subintervention_views.add_intervention_note, name='api-add-intervention-note'),
    path('api/intervention/<int:intervention_id>/resolve/', adviser_subintervention_views.resolve_intervention, name='api-resolve-intervention'),
    path('api/intervention/<int:intervention_id>/reactivate/', adviser_subintervention_views.reactivate_intervention, name='api-reactivate-intervention'),
    path('api/intervention/<int:intervention_id>/escalate/', adviser_subintervention_views.escalate_to_tier_3, name='api-escalate-intervention'),

    # ===== CLASSRECORD ENDPOINTS =====

    # INTERVENTION API ENDPOINTS
    path('api/interventions/', adviser_view_views.get_interventions, name='api-get-interventions'),
    path('api/interventions/create/', adviser_view_views.create_intervention, name='api-create-intervention'),
    path('api/interventions/<int:intervention_id>/update/', adviser_view_views.add_intervention_update, name='api-add-update'),
    path('api/interventions/<int:intervention_id>/delete/', adviser_view_views.delete_intervention, name='api-delete-intervention'),
    path('api/interventions/updates/<int:update_id>/delete/', adviser_view_views.delete_intervention_update, name='api-delete-update'),
    
    # INTERVENTION SYSTEM ENDPOINTS (NEW)
    path('adviser-sub-intervention/', adviser_subintervention_views.adviser_sub_intervention, name='adviser-sub-intervention'),
    path('api/intervention/students/', adviser_subintervention_views.get_intervention_students, name='api-intervention-students'),
    path('api/intervention/student/<int:student_id>/details/', adviser_subintervention_views.get_student_intervention_details, name='api-student-intervention-details'),
    path('api/intervention/action/create/', adviser_subintervention_views.create_intervention_action, name='api-create-intervention-action'),
    path('api/intervention/action/<int:action_id>/', adviser_subintervention_views.get_intervention_action, name='api-get-intervention-action'),
    path('api/intervention/action/<int:action_id>/update/', adviser_subintervention_views.update_intervention_action, name='api-update-intervention-action'),
    path('api/intervention/action/<int:action_id>/delete/', adviser_subintervention_views.delete_intervention_action, name='api-delete-intervention-action'),
    path('api/intervention/note/add/', adviser_subintervention_views.add_intervention_note, name='api-add-intervention-note'),
    path('api/intervention/<int:intervention_id>/resolve/', adviser_subintervention_views.resolve_intervention, name='api-resolve-intervention'),
    path('api/intervention/<int:intervention_id>/reactivate/', adviser_subintervention_views.reactivate_intervention, name='api-reactivate-intervention'),
    path('api/intervention/<int:intervention_id>/escalate/', adviser_subintervention_views.escalate_to_tier_3, name='api-escalate-intervention'),
    
   
    
    # MASTERLIST API ENDPOINTS
    path('api/masterlist/student/<int:student_id>/grades/', adviser_masterlist_views.get_student_grades, name='api-student-grades'),
    path('api/masterlist/student/<int:student_id>/status/', adviser_masterlist_views.update_student_status, name='api-update-status'),
    path('api/masterlist/student/<int:student_id>/quarter/', adviser_masterlist_views.toggle_quarter_enrollment, name='api-toggle-quarter'),
     
    # SETTINGS API ENDPOINTS
    path('api/settings/update-teacher/', adviser_settings_views.update_teacher_data, name='api-update-teacher-data'),
    path('api/settings/update-contact/', adviser_settings_views.update_contact_data, name='api-update-contact-data'),
    path('api/settings/change-history/', adviser_settings_views.get_change_history, name='api-change-history'),
    
    # ATTENDANCE API ENDPOINTS (NEW)
    path('api/attendance/section/<int:section_id>/', adviser_attendance_views.get_section_info, name='api-section-info'),
    path('api/attendance/quarter-months/', adviser_attendance_views.get_quarter_months, name='api-quarter-months'),
    path('api/attendance/load/', adviser_attendance_views.load_attendance_record, name='api-load-attendance'),
    path('api/attendance/save/', adviser_attendance_views.save_attendance, name='api-save-attendance'),
    path('api/attendance/student/<int:student_att_id>/excuse/', adviser_attendance_views.update_student_excuse, name='api-update-excuse'),
    path('api/attendance/history/', adviser_attendance_views.get_attendance_history, name='api-attendance-history'),
    path('api/attendance/record/<int:record_id>/logs/', adviser_attendance_views.get_change_logs, name='api-attendance-logs'),
    path('api/attendance/record/<int:record_id>/finalize/', adviser_attendance_views.finalize_attendance, name='api-finalize-attendance'),
    path('api/attendance/record/<int:record_id>/delete/', adviser_attendance_views.delete_attendance_record, name='api-delete-attendance'),
    path('api/attendance/record/<int:record_id>/export/', adviser_attendance_views.export_attendance_data, name='api-export-attendance'),
    
    # Classrecord
    path('api/classrecord/get/', adviser_classrecord_views.get_class_record, name='api-get-classrecord'),
    path('api/classrecord/save/', adviser_classrecord_views.save_class_record, name='api-save-classrecord'),
    path('api/classrecord/<int:record_id>/export/pdf/', adviser_classrecord_views.export_class_record_pdf, name='api-export-pdf'),
    path('api/classrecord/<int:record_id>/export/excel/', adviser_classrecord_views.export_class_record_excel, name='api-export-excel'),
    path('api/classrecord/history/', adviser_classrecord_views.get_class_record_history, name='api-classrecord-history'),
    # Early Warning System Endpoints
    path('api/classrecord/warnings/check/', adviser_classrecord_views.check_early_warnings, name='api-check-warnings'),
    path('api/classrecord/warnings/get/', adviser_classrecord_views.get_early_warnings, name='api-get-warnings'),
    path('api/classrecord/warnings/dismiss/', adviser_classrecord_views.dismiss_warning, name='api-dismiss-warning'),

    # Subject Teacher View
    # path('subject-teacher-view/', adviser_subview_views.subject_teacher_view, name='subject-teacher-view'),
    path('api/set-active-section/', adviser_subview_views.set_active_section, name='set-active-section'),
    path('api/get-active-section/', adviser_subview_views.get_active_section, name='get-active-section'),
    path('api/clear-active-section/', adviser_subview_views.clear_active_section, name='clear-active-section'),


    # SUBJECT TEACHER(LATER NA TO BASTA ANOTHER FOLDER TO)
    path('subjectteacher-dashboard/', subjectteacher_views.subjectteacher_dashboard, name='subjectteacher-dashboard'),
    path('settings/', subjectteacher_views.teacher_settings, name='teacher-settings'),
    path('sub-teacher-view/', subjectteacher_views.sub_teacher_view, name='sub-teacher-view'),
    path('class-record/', subjectteacher_views.sub_class_record, name='class-record'),
    path('attendance/', subjectteacher_views.subject_teacher_attendance, name='subject-teacher-attendance'),
    path('intervention/', subjectteacher_views.sub_intervention, name='intervention'),
    path('viewclass/', subjectteacher_views.sub_viewclass, name='view-class'),
]