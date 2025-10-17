# from django.urls import path
# 
# urlpatterns = [
#         path("", views.homepage, name="homepage"), # Route the root URL to the homepage view
#         path("student-data/", views.student_data, name='student_data'), # Route to the student_data view
#         path("family-data/", views.family_data, name='family_data'), # Route to the family_data view
#         path("student-non-academic/", views.student_non_academic, name='student_non_academic'), # Route to the student_non_academic view
#         path("student-academic/", views.student_academic, name='student_academic'), # Route to the student_academic view
#         path("section-placement/",views.section_placement, name='section_placement'),
        
#     ]
    
    
from django.urls import path
from . import views
from .views import (
    IndexView,
    StudentDataView,
    FamilyDataView,
    StudentNonAcademicView,
    StudentAcademicView,
    SectionPlacementView,
    login_view,
    logout_view  
)
from django.views.generic import TemplateView # For static login.html

app_name = 'enrollmentprocess'

urlpatterns = [
    path('', IndexView.as_view(), name='homepage'),
    path('student-data/', views.StudentDataView.as_view(), name='student_data'),
    path('student-data/<int:student_id>/', views.StudentDataView.as_view(), name='student_data'),
    path('family-data/<int:student_id>/', views.FamilyDataView.as_view(), name='family_data'),
    path('non-academic-data/<int:student_id>/', views.StudentNonAcademicView.as_view(), name='student_non_academic'),
    path('academic-data/<int:student_id>/', views.StudentAcademicView.as_view(), name='student_academic'),
    path('section-placement/<int:student_id>/', views.SectionPlacementView.as_view(), name='section_placement'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login'),  # Static login page
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]

 