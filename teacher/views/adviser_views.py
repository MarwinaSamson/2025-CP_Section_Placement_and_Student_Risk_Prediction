from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# @login_required
# def bothaccess_dashboard(request):
#       # Adviser + Subject logic (e.g., sections, advisees)
#       return render(request, 'teacher/adviser/Teacher_Landingpage.html', {})
  
# @login_required
# def adviser_view(request):
#     return render(request, 'teacher/adviser/Adviser_View.html')

@login_required
def adviser_classrecord(request):
    return render(request, 'teacher/adviser/Class_Record.html')

@login_required
def adviser_intervention(request):
    return render(request, 'teacher/adviser/subject_Intervention.html')

# @login_required
# def adviser_masterlist(request):
#     return render(request, 'teacher/adviser/Masterlist.html')

@login_required
def adviser_attendance(request):
    return render(request, 'teacher/adviser/Attendance.html')

@login_required
def adviser_reports(request):
    return render(request, 'teacher/adviser/Reports.html')

# @login_required
# def adviser_settings(request):
#     return render(request, 'teacher/adviser/Setting.html')

@login_required
def adviser_subview(request):
    return render(request, 'teacher/adviser/Subject_Teacher_View.html')

@login_required
def adviser_adviser_intervention(request):
    return render(request, 'teacher/adviser/adviser_intervention.html')


@login_required
def adviser_viewclass(request):
    return render(request, 'teacher/adviser/View_Class.html')


# @login_required
# def adviser_learnerprofile(request):
#     return render(request, 'teacher/adviser/Learner_Profile.html')