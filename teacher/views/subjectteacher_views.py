from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from enrollmentprocess.models import Student

# Create your views here for TEACHER WHO HAS BOTH ACCESS



# Create your views here for TEACHER WHO HAS subject teacher  ACCESS only
@login_required
def subjectteacher_dashboard(request):
      # Subject only (e.g., grades, subjects)
      return render(request, 'teacher/subjectteacher/Subject_Teacher_View.html', {})

@login_required
def teacher_settings(request):
    return render(request, 'teacher/subjectteacher/Setting.html', {})

@login_required
def sub_teacher_view(request):
    return render(request, 'teacher/subjectteacher/Subject_Teacher_View.html')

@login_required
def sub_class_record(request):
    return render(request, 'teacher/subjectteacher/Class_Record.html')

@login_required
def subject_teacher_attendance(request):
    return render(request, 'teacher/subjectteacher/Subject_Teacher_Attendance.html')

@login_required
def sub_intervention(request):
    return render(request, 'teacher/subjectteacher/Intervention.html')

@login_required
def sub_viewclass(request):
    return render(request, 'teacher/subjectteacher/View_Class.html')

# def view_class(request, class_id):
#     # Fetch the class info (replace "Class" with your actual model)
#     class_obj = get_object_or_404(Student, id=class_id)
    
#     context = {
#         'class_obj': class_obj,
#     }
#     return render(request, 'teacher/subjectteacher/View_Class.html', context)