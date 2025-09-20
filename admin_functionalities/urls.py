 # admin_functionalities/urls.py
from django.urls import path
from . import views

app_name = 'admin_functionalities' # Namespace for your app's URLs

urlpatterns = [
    
        path('', views.admin_dashboard, name='dashboard'),
       
    ]# admin_functionalities/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'admin_functionalities'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('sections/', views.sections_view, name='sections'),
    path('teachers/', views.teachers_view, name='teachers'),
]

    
