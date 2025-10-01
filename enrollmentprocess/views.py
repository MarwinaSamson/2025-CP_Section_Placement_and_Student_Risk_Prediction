
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy, reverse
from .models import Student, Family, StudentNonAcademic, StudentAcademic, SectionPlacement
from .forms import StudentForm, FamilyForm, StudentNonAcademicForm, StudentAcademicForm
from django.http import HttpResponseRedirect
from django.db import transaction
from .model_utils import predict_program_eligibility
from admin_functionalities.models import Notification 


class IndexView(TemplateView):
    template_name = 'enrollmentprocess/landingpage.html'

class StudentDataView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'enrollmentprocess/studentData.html'

    def get_success_url(self):
        # Redirect to family data form, passing the newly created student's ID
        return reverse_lazy('family_data', kwargs={'student_id': self.object.pk})

    def form_valid(self, form):
        # Convert boolean fields from string 'True'/'False' to actual booleans
        # form.instance.is_sped = (form.cleaned_data['is_sped'] == 'True')
        # form.instance.is_working_student = (form.cleaned_data['is_working_student'] == 'True')
        # return super().form_valid(form)
        form.instance.is_sped = form.cleaned_data['is_sped']
        form.instance.is_working_student = form.cleaned_data['is_working_student']
        form.instance.sped_details = form.cleaned_data.get('sped_details')
        form.instance.working_details = form.cleaned_data.get('working_details')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(f"DEBUG: Before setting instance, instance is: {kwargs.get('instance')}")
        kwargs['instance'] = None
        print(f"DEBUG: After setting instance, instance is: {kwargs.get('instance')}")
        kwargs['user'] = self.request.user
        return kwargs


class FamilyDataView(CreateView):
    model = Family
    form_class = FamilyForm
    template_name = 'enrollmentprocess/familyData.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass student_id to the template for the "Back" button URL
        context['student_id'] = self.kwargs['student_id']
        return context

    def form_valid(self, form):
        with transaction.atomic():
            family_instance = form.save()
            student = get_object_or_404(Student, pk=self.kwargs['student_id'])
            student.family_data = family_instance
            student.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to non-academic data form, passing the student's ID
        return reverse_lazy('student_non_academic', kwargs={'student_id': self.kwargs['student_id']})

class StudentNonAcademicView(CreateView):
    model = StudentNonAcademic
    form_class = StudentNonAcademicForm
    template_name = 'enrollmentprocess/studentNonAcademic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_academic', kwargs={'student_id': self.kwargs['student_id']})

class StudentAcademicView(CreateView):
    model = StudentAcademic
    form_class = StudentAcademicForm
    template_name = 'enrollmentprocess/studentAcademic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form = context['form']

        # Pre-fill LRN and lock it
        form.fields['lrn'].initial = student.lrn
        form.fields['lrn'].widget.attrs['readonly'] = True

        # Pass read-only info from Student to template
        context['student_id'] = self.kwargs['student_id']
        context['is_working_student'] = "YES" if student.is_working_student else "NO"
        context['working_details'] = student.working_details or "N/A"
        context['is_pwd'] = "YES" if student.is_sped else "NO"
        context['disability_type'] = student.sped_details or "N/A"

        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student

        # Always enforce values from Student model
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped
        form.instance.disability_type = student.sped_details if student.is_sped else None

        # Ensure LRN matches
        if form.cleaned_data['lrn'] != student.lrn:
            form.add_error('lrn', "LRN does not match the student's record.")
            return self.form_invalid(form)

        # Compute overall average (if applicable)
        form.instance.overall_average = form.cleaned_data.get('overall_average', 0.0)
        return super().form_valid(form)
    
    def get_success_url(self): return reverse_lazy('section_placement', kwargs={'student_id': self.kwargs['student_id']})
 


class SectionPlacementView(TemplateView):
    template_name = 'enrollmentprocess/sectionPlacement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['student'] = student
        context['is_pwd'] = student.is_sped
        context['is_working_student'] = student.is_working_student

        try:
            academic = student.studentacademic
        except StudentAcademic.DoesNotExist:
            context['error_message'] = "Academic data not found for this student."
            return context

        input_data = {
            'dost_exam_result': academic.dost_exam_result,
            'filipino grade': academic.filipino,
            'English grade': academic.english,
            'mathematics grade': academic.mathematics,
            'science grade': academic.science,
            'araling panlipunan grade': academic.araling_panlipunan,
            'Edukasyon sa pagpapakatao grade': academic.edukasyon_pagpapakatao,
            'Edukasyong panglipunan at pangkabuhayan grade': academic.edukasyon_pangkabuhayan,
            'MAPEH grade': academic.mapeh,
            'Average grade': academic.overall_average,
        }

        recommendations = predict_program_eligibility(input_data)
        context['recommendations'] = recommendations

        # Check for success query param to show success modal
        if self.request.GET.get('success') == '1':
            context['show_success_modal'] = True

        return context

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        selected_program = request.POST.get('selected_program')

        if selected_program:
            # Update student's current section placement
            student.section_placement = selected_program
            student.save()

            # Create SectionPlacement record if not exists
            SectionPlacement.objects.get_or_create(
                student=student,
                selected_program=selected_program,
            )
            
             # NEW: Check if student is complete and trigger notification
            is_complete = (
                student.family_data is not None and  # Family form filled
                StudentAcademic.objects.filter(student=student).exists() and  # Academic exists (already checked in GET)
                StudentNonAcademic.objects.filter(student=student).exists() and  # Non-academic form filled
                SectionPlacement.objects.filter(student=student).exists()  # Placement confirmed (just saved)
            )
            
            if is_complete:
                # Create Notification for Admin (trigger on confirm/submit)
                program = selected_program
                student_name = f"{student.first_name} {student.middle_name or ''} {student.last_name}".strip()
                Notification.objects.create(
                    title="New Enrollment Submission",
                    message=f"{student_name} confirmed and submitted for {program} program.",
                    notification_type='student_enrollment',
                    program=program,
                    related_student=student,
                )

            # Redirect back with success flag to trigger modal
            url = reverse('section_placement', kwargs={'student_id': student.pk})
            return redirect(f"{url}?success=1")

        context = self.get_context_data(**kwargs)
        context['error_message'] = "Please select a program/section."
        return self.render_to_response(context)

# LoginView can be added here if needed, or use Django's built-in auth views.
def login_view(request):
    return render(request, 'enrollmentprocess/login.html')  # Adjust path if your template is in a subfolder
