from django.urls import path
from . import views
urlpatterns = [
        path("", views.homepage, name="homepage"), # Route the root URL to the homepage view
        path("student-data/", views.student_data, name='student_data'), # Route to the student_data view
        path("family-data/", views.family_data, name='family_data'), # Route to the family_data view
        path("student-academic/", views.student_academic, name='student_academic'), # Route to the student_academic view
        path("student-academic-2/", views.student_academic_2, name='student_academic_2'), # Route to the student_academic_2 view
    ]
    