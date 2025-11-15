from django.urls import path
from .views import subjectteacher_views, adviser_views, adviser_dashboard_views, adviser_view_views, adviser_masterlist_views, adviser_attendance_views, adviser_settings_views, adviser_learnersprofile_views

app_name = 'teacher'

urlpatterns = [ 
    
    # ADVISER + SUBJECT TEACHER
      path('bothaccess-dashboard/', adviser_dashboard_views.bothaccess_dashboard, name='bothaccess-dashboard'),  # Combined
      path('adviserview/', adviser_view_views.adviser_view, name='adviser-view'),
      path('adviserclass-record/', adviser_views.adviser_classrecord, name='adviser-classrecord'),
      path('adviserintervention/', adviser_views.adviser_intervention, name='adviser-intervention'),
      path('advisermasterlist/', adviser_masterlist_views.adviser_masterlist, name='adviser-masterlist'),
      path('adviserattendance/', adviser_views.adviser_attendance, name='adviser-attendance'),
      path('adviserreports/', adviser_views.adviser_reports, name='adviser-reports'),
      path('advisersettings/', adviser_settings_views.adviser_settings, name='adviser-settings'),
      path('advisersubview/', adviser_views.adviser_subview, name='adviser-subview'),
      path('adviserlearnersprofile/', adviser_learnersprofile_views.adviser_learnerprofile, name='adviser-studentprofile'),
    
    # INTERVENTION API ENDPOINTS (NEW)
    path('api/interventions/', adviser_view_views.get_interventions, name='api-get-interventions'),
    path('api/interventions/create/', adviser_view_views.create_intervention, name='api-create-intervention'),
    path('api/interventions/<int:intervention_id>/update/', adviser_view_views.add_intervention_update, name='api-add-update'),
    path('api/interventions/<int:intervention_id>/delete/', adviser_view_views.delete_intervention, name='api-delete-intervention'),
    path('api/interventions/updates/<int:update_id>/delete/', adviser_view_views.delete_intervention_update, name='api-delete-update'),
    
    
    # MASTERLIST API ENDPOINTS (NEW)
    path('api/masterlist/student/<int:student_id>/grades/', adviser_masterlist_views.get_student_grades, name='api-student-grades'),
    path('api/masterlist/student/<int:student_id>/status/', adviser_masterlist_views.update_student_status, name='api-update-status'),
    path('api/masterlist/student/<int:student_id>/quarter/', adviser_masterlist_views.toggle_quarter_enrollment, name='api-toggle-quarter'),
     
   
    # SETTINGS API ENDPOINTS (NEW)
    path('api/settings/update-teacher/', adviser_settings_views.update_teacher_data, name='api-update-teacher-data'),
    path('api/settings/update-contact/', adviser_settings_views.update_contact_data, name='api-update-contact-data'),
    path('api/settings/change-history/', adviser_settings_views.get_change_history, name='api-change-history'),
    
    # ATTENDANCE API ENDPOINTS (NEW)
    
    
    
    #   SUBJECT TEACHER
      path('subjectteacher-dashboard/', subjectteacher_views.subjectteacher_dashboard, name='subjectteacher-dashboard'),  # Subject only
      path('settings/', subjectteacher_views.teacher_settings, name='teacher-settings'),
      path('sub-teacher-view/', subjectteacher_views.sub_teacher_view, name='sub-teacher-view'),
      path('class-record/', subjectteacher_views.sub_class_record, name='class-record'),
      path('attendance/', subjectteacher_views.subject_teacher_attendance, name='subject-teacher-attendance'),
      path('intervention/', subjectteacher_views.sub_intervention, name='intervention'),
      path('viewclass/', subjectteacher_views.sub_viewclass, name='view-class'),
  ]
