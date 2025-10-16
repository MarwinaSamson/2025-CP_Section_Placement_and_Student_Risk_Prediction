from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    
      path('bothaccess-dashboard/', views.bothaccess_dashboard, name='bothaccess-dashboard'),  # Combined
      path('subjectteacher-dashboard/', views.subjectteacher_dashboard, name='subjectteacher-dashboard'),  # Subject only

  ]
