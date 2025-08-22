from django.shortcuts import render

def homepage(request):
        return render(request, 'enrollmentprocess/index.html')

def student_data(request):
    return render(request, 'enrollmentprocess/studentData.html')