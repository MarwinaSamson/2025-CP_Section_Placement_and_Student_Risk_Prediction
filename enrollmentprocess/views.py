
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy, reverse
from .models import Student, Family, StudentNonAcademic, StudentAcademic, SectionPlacement
from .forms import StudentForm, FamilyForm, StudentNonAcademicForm, StudentAcademicForm
from django.http import HttpResponseRedirect
from django.db import transaction
from .model_utils import predict_program_eligibility
from admin_functionalities.models import Notification, CustomUser  
from .model_utils import extract_grades_from_image, SUBJECT_MAPPING  # Import from utils
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date
from django .http import JsonResponse
import json



class IndexView(TemplateView):
    template_name = 'enrollmentprocess/landingpage.html'


class StudentDataView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'enrollmentprocess/studentData.html'

    def student_data(request):
        # Render the studentData.html template
        return render(request, 'enrollmentprocess/studentData.html')


    def family_data(request):
        # Render the familyData.html template
        return render(request, 'enrollmentprocess/familyData.html')


    def student_non_academic(request):
        # Render the studentNonAcademic.html template
        return render(request, 'enrollmentprocess/studentNonAcademic.html')
    
    def student_academic(request):
        # Render the studentAcademic.html template
        return render(request, 'enrollmentprocess/studentAcademic.html')


    def student_academic_2(request):
        # Render the studentAcademic2.html template
        return render(request, 'enrollmentprocess/studentAcademic2.html')


    def qualified_program(request):
        return render(request, 'enrollmentprocess/qualified_program.html')
    
    def get_object(self):
        """Get existing student object if student_id is provided"""
        student_id = self.kwargs.get('student_id')
        if student_id:
            try:
                return Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return None
        return None

    def get_initial(self):
        """Prefill form with existing data if available"""
        initial = super().get_initial()
        student = self.get_object()

        if student:
            initial.update({
                'lrn': student.lrn,
                'enrolling_as': student.enrolling_as.split(',') if student.enrolling_as else [],
                'is_sped': '1' if student.is_sped else '0',
                'sped_details': student.sped_details,
                'is_working_student': '1' if student.is_working_student else '0',
                'working_details': student.working_details,
                'last_name': student.last_name,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'address': student.address,
                'gender': student.gender,
                'date_of_birth': student.date_of_birth,
                'place_of_birth': student.place_of_birth,
                'religion': student.religion,
                'dialect_spoken': student.dialect_spoken,
                'ethnic_tribe': student.ethnic_tribe,
                'last_school_attended': student.last_school_attended,
                'previous_grade_section': student.previous_grade_section,
                'last_school_year': student.last_school_year,
            })
        return initial
    
    def get_success_url(self):
     return reverse_lazy('enrollmentprocess:family_data', kwargs={'student_id': self.object.pk})

    def form_valid(self, form):
        # Calculate age from date_of_birth
        if form.cleaned_data.get('date_of_birth'):
            today = date.today()
            birth_date = form.cleaned_data['date_of_birth']
            age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
            form.instance.age = age

        # Handle other boolean fields
        form.instance.is_sped = form.cleaned_data['is_sped']
        form.instance.is_working_student = form.cleaned_data['is_working_student']
        form.instance.sped_details = form.cleaned_data.get('sped_details')
        form.instance.working_details = form.cleaned_data.get(
            'working_details')

        # If we're editing an existing student, update it instead of creating new
        student = self.get_object()
        if student:
            # Update existing student
            for field, value in form.cleaned_data.items():
                setattr(student, field, value)
            student.save()
            self.object = student
        else:
            # Create new student
            self.object = form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass student_id if we're editing
        student_id = self.kwargs.get('student_id')
        if student_id:
            context['student_id'] = student_id
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print(f"DEBUG: Before setting instance, instance is: {kwargs.get('instance')}")
        kwargs['instance'] = None
        print(f"DEBUG: After setting instance, instance is: {kwargs.get('instance')}")
        return kwargs


class FamilyDataView(CreateView):
    model = Family
    form_class = FamilyForm
    template_name = 'enrollmentprocess/familyData.html'

    def get_initial(self):
        """Prefill form with existing family data if available"""
        initial = super().get_initial()
        student_id = self.kwargs['student_id']

        try:
            student = Student.objects.get(pk=student_id)
            if hasattr(student, 'family_data') and student.family_data:
                family = student.family_data
                initial.update({
                    'father_family_name': family.father_family_name,
                    'father_first_name': family.father_first_name,
                    'father_middle_name': family.father_middle_name,
                    'father_occupation': family.father_occupation,
                    'father_dob': family.father_dob,
                    'father_contact_number': family.father_contact_number,
                    'father_email': family.father_email,
                    'mother_family_name': family.mother_family_name,
                    'mother_first_name': family.mother_first_name,
                    'mother_middle_name': family.mother_middle_name,
                    'mother_occupation': family.mother_occupation,
                    'mother_dob': family.mother_dob,
                    'mother_contact_number': family.mother_contact_number,
                    'mother_email': family.mother_email,
                    'guardian_family_name': family.guardian_family_name,
                    'guardian_first_name': family.guardian_first_name,
                    'guardian_middle_name': family.guardian_middle_name,
                    'guardian_occupation': family.guardian_occupation,
                    'guardian_dob': family.guardian_dob,
                    'guardian_address': family.guardian_address,
                    'guardian_relationship': family.guardian_relationship,
                    'guardian_contact_number': family.guardian_contact_number,
                    'guardian_email': family.guardian_email,
                })
        except Student.DoesNotExist:
            pass

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']

        # Get student info for display
        try:
            student = Student.objects.get(pk=self.kwargs['student_id'])
            context['student_name'] = f"{student.first_name} {student.last_name}"
            context['student_lrn'] = student.lrn
        except Student.DoesNotExist:
            pass

        return context

    def form_valid(self, form):
        # Calculate ages from date of birth before saving
        today = date.today()

        # Calculate father's age
        if form.cleaned_data.get('father_dob'):
            birth_date = form.cleaned_data['father_dob']
            father_age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
            form.instance.father_age = father_age

        # Calculate mother's age
        if form.cleaned_data.get('mother_dob'):
            birth_date = form.cleaned_data['mother_dob']
            mother_age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
            form.instance.mother_age = mother_age

        # Calculate guardian's age
        if form.cleaned_data.get('guardian_dob'):
            birth_date = form.cleaned_data['guardian_dob']
            guardian_age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
            form.instance.guardian_age = guardian_age

        with transaction.atomic():
            family_instance = form.save()
            student = get_object_or_404(Student, pk=self.kwargs['student_id'])
            student.family_data = family_instance
            student.save()
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('enrollmentprocess:student_non_academic', kwargs={'student_id': self.kwargs['student_id']})


class StudentNonAcademicView(CreateView):
    model = StudentNonAcademic
    form_class = StudentNonAcademicForm
    template_name = 'enrollmentprocess/studentNonAcademic.html'

    def get_initial(self):
        """Prefill form with existing non-academic data if available"""
        initial = super().get_initial()
        student_id = self.kwargs['student_id']

        try:
            non_academic = StudentNonAcademic.objects.get(
                student_id=student_id)

            initial.update({
                'study_hours': non_academic.study_hours,
                'study_place': non_academic.study_place.split(',') if non_academic.study_place else [],
                'study_with': non_academic.study_with,
                'live_with': non_academic.live_with.split(',') if non_academic.live_with else [],
                'parent_help': non_academic.parent_help,
                'highest_education': non_academic.highest_education,
                'marital_status': non_academic.marital_status,
                'house_type': non_academic.house_type,
                'quiet_place': non_academic.quiet_place,
                'study_area': non_academic.study_area,
                'transport_mode': non_academic.transport_mode,
                'travel_time': non_academic.travel_time,
                'access_resources': non_academic.access_resources.split(',') if non_academic.access_resources else [],
                'computer_use': non_academic.computer_use,
                'hobbies': non_academic.hobbies,
                'personality_traits': non_academic.personality_traits.split(',') if non_academic.personality_traits else [],
                'confidence_level': non_academic.confidence_level,
            })
        except StudentNonAcademic.DoesNotExist:
            pass

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])

        # Pass read-only info from Student to template
        context['student_id'] = self.kwargs['student_id']
        context['is_working_student'] = "YES" if student.is_working_student else "NO"
        context['working_details'] = student.working_details or "N/A"
        context['is_pwd'] = "YES" if student.is_sped else "NO"
        context['disability_type'] = student.sped_details or "N/A"

        return context

    def get_success_url(self):
        return reverse_lazy('enrollmentprocess:student_academic', kwargs={'student_id': self.kwargs['student_id']})

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student

        # Enforce values from Student
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped
        form.instance.disability_type = student.sped_details if student.is_sped else None

        return super().form_valid(form)

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

        # Enforce values from Student
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped
        form.instance.disability_type = student.sped_details if student.is_sped else None

        # Ensure LRN matches
        if form.cleaned_data['lrn'] != student.lrn:
            form.add_error('lrn', "LRN does not match the student's record.")
            return self.form_invalid(form)

        # Set overall_average if provided (you may compute it instead)
        form.instance.overall_average = form.cleaned_data.get('overall_average', 0.0)

        # First save the form / instance (super will call form.save())
        response = super().form_valid(form)  # This sets self.object

        # Now extract OCR grades from the saved file (self.object.report_card)
        mismatches = {}
        try:
            report_field = self.object.report_card
            if report_field:
                # Use the storage path if available, else pass the file-like object
                ocr_source = None
                try:
                    ocr_source = report_field.path  # Works with local FileSystemStorage
                except Exception:
                    # Fallback to file-like object
                    ocr_source = report_field

                ocr_grades = extract_grades_from_image(ocr_source)

                # Fields to compare - keys should match your SUBJECT_MAPPING keys
                compare_fields = [
                    'mathematics', 'araling_panlipunan', 'english',
                    'edukasyon_pagpapakatao', 'science',
                    'edukasyon_pangkabuhayan', 'filipino', 'mapeh'
                ]
                TOLERANCE = 0.5  # Tolerance for small OCR/rounding differences

                for field_name in compare_fields:
                    entered = getattr(self.object, field_name, None)
                    ocr_value = ocr_grades.get(field_name)
                    if entered is not None and ocr_value is not None:
                        try:
                            if abs(float(entered) - float(ocr_value)) > TOLERANCE:
                                mismatches[field_name] = {
                                    'entered': float(entered),
                                    'ocr': float(ocr_value)
                                }
                        except Exception:
                            # If conversion fails, mark as mismatch for manual check
                            mismatches[field_name] = {
                                'entered': entered,
                                'ocr': ocr_value
                            }

        except Exception as e:
            print("OCR/verification error:", e)
            # Do not block saving; just continue

        # Save mismatch details into the JSONField
        self.object.mismatch_fields = mismatches or {}
        self.object.save(update_fields=['mismatch_fields'])

        # Optional: Create a Notification so admin sees this in their queue
        try:
            if mismatches:
                student_name = f"{student.first_name} {student.last_name}".strip()
                fields = ", ".join(mismatches.keys())
                Notification.objects.create(
                    title="Grade mismatch detected",
                    message=f"Possible grade mismatch for {student_name}. Fields: {fields}"
                )
        except Exception as e:
            print("Notification creation failed:", e)

        return response


    def get_success_url(self):
        return reverse_lazy('enrollmentprocess:section_placement', kwargs={'student_id': self.kwargs['student_id']})




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
# def login_view(request):
#     return render(request, 'enrollmentprocess/login.html')  # Adjust path if your template is in a subfolder
def get_redirect_url_by_role(user):
    """Returns redirect URL based on CustomUser roles (admin, staff, teacher subtypes)."""
    try:
        if user.is_superuser:  # Admin (is_superuser=True)
            return reverse('admin_functionalities:admin-dashboard')  # To /admin-functionalities/admin-dashboard/ → admin_dashboard.html
        elif user.is_staff and not user.is_superuser:  # Staff (is_staff=True, fallback to admin for now)
            return reverse('admin_functionalities:admin-dashboard')  # Same as admin
        elif user.is_teacher or user.is_subject_teacher:  # Teacher umbrella
            if user.is_adviser and user.is_subject_teacher:  # Both True → Combined dashboard
                return reverse('teacher:bothaccess-dashboard')  # To /teacher/bothaccess_dashboard/ → bothaccess_dashboard.html
            elif user.is_subject_teacher and not user.is_adviser:  # Subject only → Subject dashboard
                return reverse('teacher:subjectteacher-dashboard')  # To /teacher/subjectteacher-dashboard/ → subjectteacher-dashboard.html
            else:  # Fallback for general teacher
                return reverse('teacher:subjectteacher-dashboard')
        else:
            # Unauthorized/default: Back to homepage
            return reverse('enrollmentprocess:homepage')
    except Exception as e:  # NoReverseMatch or other (e.g., URL name wrong)
        print(f"Redirect error: {e}")  # Debug in server console
        # Fallback paths (adjust to your exact URLs)
        if user.is_superuser or user.is_staff:
            return '/admin-functionalities/admin-dashboard/'
        elif user.is_adviser and user.is_subject_teacher:
            return '/teacher/bothaccess-dashboard/'
        elif user.is_subject_teacher:
            return '/teacher/subjectteacher-ashboard/'
        else:
            return '/'

def login_view(request):
    """Login view: Render form on GET; handle POST (AJAX or form) with role redirect."""
    if request.user.is_authenticated:
        # Already logged in: Redirect or JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX
            redirect_url = get_redirect_url_by_role(request.user)
            return JsonResponse({
                'success': True,
                'message': 'Already logged in.',
                'redirect': redirect_url
            })
        else:
            # Non-AJAX: Direct redirect
            return redirect(get_redirect_url_by_role(request.user))
    
    if request.method == 'POST':
        # AJAX or form POST
        username = request.POST.get('username')  # Assuming email as username
        password = request.POST.get('password')
        
        if not username or not password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Please enter username and password.'})
            else:
                # Non-AJAX: Re-render with error (use messages or form errors)
                from django.contrib import messages
                messages.error(request, 'Please enter username and password.')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_url = get_redirect_url_by_role(user)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': f'Welcome, {user.first_name or user.username}!',
                        'redirect': redirect_url
                    })
                else:
                    return redirect(redirect_url)
            else:
                error_msg = 'Account is disabled. Contact admin.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    from django.contrib import messages
                    messages.error(request, error_msg)
        else:
            error_msg = 'Invalid username or password.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
            else:
                from django.contrib import messages
                messages.error(request, error_msg)
        
        # For non-AJAX POST errors, re-render form
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'enrollmentprocess/login.html')  # Shared template
    
    # GET: Render login form
    return render(request, 'enrollmentprocess/login.html')

def logout_view(request):
    
    logout(request) 
    return redirect('enrollmentprocess:login')  # /login/ form