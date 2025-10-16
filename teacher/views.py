from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here for TEACHER WHO HAS BOTH ACCESS
@login_required
def bothaccess_dashboard(request):
      # Adviser + Subject logic (e.g., sections, advisees)
      return render(request, 'teacher/bothaccess_dashboard.html', {})


# Create your views here for TEACHER WHO HAS subject teacher  ACCESS only
@login_required
def subjectteacher_dashboard(request):
      # Subject only (e.g., grades, subjects)
      return render(request, 'teacher/subjectteacher_dashboard.html', {})