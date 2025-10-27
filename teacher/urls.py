from django.urls import path
from . import views, adviser_views

app_name = 'teacher'

urlpatterns = [
    
    # ADVISER + SUBJECT TEACHER
      path('bothaccess-dashboard/', adviser_views.bothaccess_dashboard, name='bothaccess-dashboard'),  # Combined
      path('adviserview/', adviser_views.adviser_view, name='adviser-view'),
      path('adviserclass-record/', adviser_views.adviser_classrecord, name='adviser-classrecord'),
      path('adviserintervention/', adviser_views.adviser_intervention, name='adviser-intervention'),
      path('advisermasterlist/', adviser_views.adviser_masterlist, name='adviser-masterlist'),
      path('adviserattendance/', adviser_views.adviser_attendance, name='adviser-attendance'),
      path('adviserreports/', adviser_views.adviser_reports, name='adviser-reports'),
      path('advisersettings/', adviser_views.adviser_settings, name='adviser-settings'),
      
    #   SUBJECT TEACHER
      path('subjectteacher-dashboard/', views.subjectteacher_dashboard, name='subjectteacher-dashboard'),  # Subject only
      path('settings/', views.teacher_settings, name='teacher-settings'),
      path('sub-teacher-view/', views.sub_teacher_view, name='sub-teacher-view'),
      path('class-record/', views.sub_class_record, name='class-record'),
      path('attendance/', views.subject_teacher_attendance, name='subject-teacher-attendance'),
      path('intervention/', views.sub_intervention, name='intervention'),
      path('viewclass/', views.sub_viewclass, name='view-class'),
  ]
