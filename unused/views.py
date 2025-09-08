# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import StudentDataForm, FamilyDataForm, StudentNonAcademicDataForm, StudentAcademicDataForm
# from .models import StudentData, FamilyData, StudentNonAcademicData, StudentAcademicData
# from django.urls import reverse




# def homepage(request):
#         return render(request, 'enrollmentprocess/index.html') # Render the index.html template

# # def student_data(request):
# #     return render(request, 'enrollmentprocess/studentData.html') # Render the studentData.html template
# def student_data_view(request):
#     if request.method == 'POST':
#         form = StudentDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             lrn = form.cleaned_data['lrn']
#             if StudentData.objects.filter(lrn=lrn).exists():
#                 form.add_error('lrn', 'A student with this LRN already exists in the system.')
#             else:
#                 student = form.save()
#                 return redirect('family_data', student_id=student.id)
#     else:
#         form = StudentDataForm()
#     return render(request, 'enrollmentprocess/studentData.html', {'form': form})


# # def family_data(request):
# #         return render(request, 'enrollmentprocess/familyData.html') # Render the familyData.html template
# def family_data_view(request, student_id):
#     student = get_object_or_404(StudentData, id=student_id)
#     if request.method == 'POST':
#         form = FamilyDataForm(request.POST, request.FILES)
#         if form.is_valid():
#             family = form.save()
#             # Link family to student
#             student.family = family
#             student.save()
#             # Redirect to non-academic form
#             return redirect('student_non_academic', student_id=student.id)
#     else:
#         form = FamilyDataForm()
#     return render(request, 'enrollmentprocess/familyData.html', {'form': form, 'student': student})



# # def student_non_academic(request):
# #         return render(request, 'enrollmentprocess/studentNonAcademic.html') # Render the studentNonAcademic.html template
# # def student_non_academic_view(request, student_id):
# #     student = get_object_or_404(StudentData, id=student_id)
# #     try:
# #         instance = student.non_academic_data
# #     except StudentNonAcademicData.DoesNotExist:
# #         instance = None

# #     if request.method == 'POST':
# #         form = StudentNonAcademicDataForm(request.POST, instance=instance)
# #         if form.is_valid():
# #             non_academic_data = form.save(commit=False)
# #             non_academic_data.student = student
# #             non_academic_data.save()
# #             return redirect('student_academic', student_id=student.id)
# #     else:
# #         form = StudentNonAcademicDataForm(instance=instance)

# #     return render(request, 'enrollmentprocess/studentNonAcademic.html', {'form': form, 'student': student})

# def student_non_academic_view(request, student_id):
#     student = get_object_or_404(StudentData, id=student_id)
#     try:
#         instance = student.non_academic_data
#     except StudentNonAcademicData.DoesNotExist:
#         instance = None

#     if request.method == 'POST':
#         form = StudentNonAcademicDataForm(request.POST, instance=instance)
#         if form.is_valid():
#             non_academic_data = form.save(commit=False)
#             non_academic_data.student = student
#             non_academic_data.save()
#             return redirect('student_academic', student_id=student.id)
#     else:
#         form = StudentNonAcademicDataForm(instance=instance)

#     return render(request, 'enrollmentprocess/studentNonAcademic.html', {'form': form, 'student': student})


# # def student_academic(request):
# #         return render(request, 'enrollmentprocess/studentAcademic.html') # Render the studentAcademic.html template
# # def student_academic_view(request, student_id):
# #     student = get_object_or_404(StudentData, id=student_id)
# #     try:
# #         instance = student.academic_data
# #     except StudentAcademicData.DoesNotExist:
# #         instance = None

# #     if request.method == 'POST':
# #         form = StudentAcademicDataForm(request.POST, request.FILES, instance=instance)
# #         if form.is_valid():
# #             academic_data = form.save(commit=False)
# #             academic_data.student = student
# #             academic_data.save()
# #             # Redirect to next step or success page
# #             return redirect('enrollment_complete')  # or your desired url
# #     else:
# #         form = StudentAcademicDataForm(instance=instance)

# #     return render(request, 'enrollmentprocess/studentAcademic.html', {'form': form, 'student': student})


# def student_academic_view(request, student_id):
#     student = get_object_or_404(StudentData, id=student_id)
#     try:
#         instance = student.academic_data
#     except StudentAcademicData.DoesNotExist:
#         instance = None

#     # Prepare initial data from StudentData
#     initial_data = {
#         'lrn': student.lrn,
#         'is_working_student': 'yes' if student.is_working_student else 'no',
#         'work_type': student.working_details or '',
#         'is_sped': 'yes' if student.is_sped else 'no',
#         'sped_details': student.sped_details or '',
#     }

#     if request.method == 'POST':
#         form = StudentAcademicDataForm(request.POST, request.FILES, instance=instance, initial=initial_data)
#         if form.is_valid():
#             academic_data = form.save(commit=False)
#             academic_data.student = student
#             academic_data.save()
#             return redirect('section_placement')  # Adjust to your next step URL name
#     else:
#         form = StudentAcademicDataForm(instance=instance, initial=initial_data)

#     return render(request, 'enrollmentprocess/studentAcademic.html', {'form': form, 'student': student})


# # def student_academic_2(request):
# #         return render(request, 'enrollmentprocess/studentAcademic2.html') # Render the studentAcademic2.html template

# def section_placement(request):
#         return render(request, 'enrollmentprocess/sectionPlacement.html')

