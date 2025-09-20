# admin_functionalities/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_functionalities:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_functionalities:dashboard')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'admin_functionalities/login.html', context)
    else:
        return render(request, 'admin_functionalities/login.html')
    
@login_required
def custom_logout(request):
    admin_name = request.user.get_full_name() or request.user.username
    last_login = request.user.last_login
    # Example session duration placeholder; replace with real calculation if needed
    session_duration = "2h 0m"
    logout(request)  # Log out the user
    context = {
        'admin_name': admin_name,
        'last_login': last_login,
        'session_duration': session_duration,
    }
    return render(request, 'admin_functionalities/logout.html', context)

@login_required
def admin_dashboard(request):
    return render(request, 'admin_functionalities/admin-dashboard.html')

@login_required
def settings_view(request):
    # Add any context data if needed
    return render(request, 'admin_functionalities/settings.html')

@login_required
def sections_view(request):
    # Add context if needed
    return render(request, 'admin_functionalities/sections.html', {'active_page': 'sections'})

@login_required
def teachers_view(request):
    # Add context if needed
    return render(request, 'admin_functionalities/teachers.html')
