# from django.shortcuts import render, redirect, get_object_or_404

# def homepage(request):
#         return render(request, 'enrollmentprocess/index.html') 
    
# def student_data(request):
#         return render(request, 'enrollmentprocess/studentData.html') 
    
# def family_data(request):
#         return render(request, 'enrollmentprocess/familyData.html') 
    
# def student_non_academic(request):
#         return render(request, 'enrollmentprocess/studentNonAcademic.html')

# def student_academic(request):
#         return render(request, 'enrollmentprocess/studentAcademic.html')
    
# def section_placement(request):
#     return render(request, 'enrollmentprocess/sectionPlacement.html')
    
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy, reverse
from .models import Student, Family, StudentNonAcademic, StudentAcademic
from .forms import StudentForm, FamilyForm, StudentNonAcademicForm, StudentAcademicForm
from django.http import HttpResponseRedirect
from django.db import transaction

class IndexView(TemplateView):
    template_name = 'enrollmentprocess/index.html'

class StudentDataView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'enrollmentprocess/studentData.html'

    def get_success_url(self):
        # Redirect to family data form, passing the newly created student's ID
        return reverse_lazy('family_data', kwargs={'student_id': self.object.pk})

    def form_valid(self, form):
        # Convert boolean fields from string 'True'/'False' to actual booleans
        form.instance.is_sped = (form.cleaned_data['is_sped'] == 'True')
        form.instance.is_working_student = (form.cleaned_data['is_working_student'] == 'True')
        return super().form_valid(form)

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
        context['student_id'] = self.kwargs['student_id']
        # Pass student's LRN to pre-fill the form if needed
        context['form'].fields['lrn'].initial = student.lrn
        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student
        # Populate is_working_student and is_pwd from the Student model
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped # Assuming is_sped in Student model maps to is_pwd here
        form.instance.disability_type = student.sped_details if student.is_sped else None
        
        # Ensure LRN matches the student's LRN
        if form.cleaned_data['lrn'] != student.lrn:
            form.add_error('lrn', "LRN does not match the student's record.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('section_placement', kwargs={'student_id': self.kwargs['student_id']})

class SectionPlacementView(TemplateView):
    template_name = 'enrollmentprocess/sectionPlacement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['student'] = student
        context['is_pwd'] = student.is_sped # Use is_sped from Student model for PWD status
        context['is_working_student'] = student.is_working_student
        return context

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        selected_program = request.POST.get('selected_program')

        if selected_program:
            student.section_placement = selected_program
            student.save()
            # You might want to add a success message here
            return redirect(reverse('section_placement', kwargs={'student_id': student.pk})) # Redirect back to the same page to show success or to a confirmation page
        
        # If no program was selected, re-render the page with an error or message
        context = self.get_context_data(**kwargs)
        context['error_message'] = "Please select a program/section."
        return self.render_to_response(context)

