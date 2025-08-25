from django.shortcuts import render

def homepage(request):
        return render(request, 'enrollmentprocess/index.html') # Render the index.html template

def student_data(request):
    return render(request, 'enrollmentprocess/studentData.html') # Render the studentData.html template

def family_data(request):
        return render(request, 'enrollmentprocess/familyData.html') # Render the familyData.html template

def student_non_academic(request):
        return render(request, 'enrollmentprocess/studentNonAcademic.html') # Render the studentNonAcademic.html template

def student_academic(request):
        return render(request, 'enrollmentprocess/studentAcademic.html') # Render the studentAcademic.html template

def student_academic_2(request):
        return render(request, 'enrollmentprocess/studentAcademic2.html') # Render the studentAcademic2.html template

