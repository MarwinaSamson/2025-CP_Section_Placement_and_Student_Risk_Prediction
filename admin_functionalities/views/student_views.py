# ============================================================================
# 8. admin_functionalities/views/student_views.py
# ============================================================================
"""
Student management views.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView

from enrollmentprocess.models import Student, StudentAcademic
from enrollmentprocess.forms import (
    StudentForm,
    FamilyForm,
    StudentNonAcademicForm,
    StudentAcademicForm,
    SectionPlacementForm,
)
from admin_functionalities.models import StudentRequirements
from admin_functionalities.forms import StudentRequirementsForm
from admin_functionalities.services import SectionAssignmentService
from admin_functionalities.utils import log_activity
from .utils import (
    get_family_or_create,
    get_non_academic_or_create,
    get_academic_or_create,
    get_placement_or_create,
)

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def student_edit_view(request, student_id):
    """
    Edit student details and auto-assign to section upon save.
    
    Flow:
    1. Admin reviews/edits all student details
    2. Admin clicks "Save All Changes"
    3. All forms validated and saved
    4. System automatically assigns student to a section based on:
       - Selected program (from SectionPlacementForm)
       - Academic merit (overall average)
       - Section availability and current load
    5. Success message shows assigned section
    """
    student = get_object_or_404(Student, id=student_id)

    if not request.user.is_staff:
        messages.error(request, 'Access denied: Admin only.')
        return render(request, 'admin_functionalities/error.html', {'error': 'Permission denied.'})

    # Get or create requirements record
    requirements, _ = StudentRequirements.objects.get_or_create(student=student)

    if request.method == "POST":
        logger.info(f"\n{'='*80}")
        logger.info(f"📝 Processing POST request for student {student_id}: {student.first_name} {student.last_name}")
        logger.info(f"{'='*80}")
        
        student_form = StudentForm(request.POST, request.FILES, instance=student, user=request.user)
        family_form = FamilyForm(request.POST, request.FILES, instance=get_family_or_create(student), user=request.user)
        non_academic_form = StudentNonAcademicForm(request.POST, instance=get_non_academic_or_create(student), user=request.user)
        academic_form = StudentAcademicForm(request.POST, request.FILES, instance=get_academic_or_create(student), user=request.user)
        placement_form = SectionPlacementForm(request.POST, instance=get_placement_or_create(student), user=request.user)
        requirements_form = StudentRequirementsForm(request.POST, instance=requirements)

        # Helper to collect missing requirements
        def get_missing_requirements(req_cleaned):
            missing = []
            for fname, friendly in [
                ('birth_certificate', 'Birth Certificate'),
                ('good_moral', 'Good Moral Certificate'),
                ('interview_done', 'Interview'),
                ('reading_assessment_done', 'Reading Assessment'),
            ]:
                if not req_cleaned.get(fname):
                    missing.append(friendly)
            return missing

        # Validate all forms
        forms_valid = all([
            student_form.is_valid(),
            family_form.is_valid(),
            non_academic_form.is_valid(),
            academic_form.is_valid(),
            placement_form.is_valid(),
            requirements_form.is_valid()
        ])
        
        if not forms_valid:
            messages.error(request, "Please correct the errors below.")
            logger.warning(f"⚠️ Form validation failed for student {student.id}")
            
            # Log which forms have errors
            for form_name, form in [
                ('Student', student_form),
                ('Family', family_form),
                ('Non-Academic', non_academic_form),
                ('Academic', academic_form),
                ('Placement', placement_form),
                ('Requirements', requirements_form)
            ]:
                if not form.is_valid():
                    logger.error(f"❌ {form_name} form errors: {form.errors}")
        else:
            try:
                with transaction.atomic():
                    logger.info("💾 Saving all forms...")
                    
                    # Save forms first
                    student_form.save()
                    family_form.save()
                    non_academic_form.save()
                    academic_form.save()
                    placement_form.save()
                    requirements_form.save()
                    
                    logger.info("✅ All forms saved successfully")

                    # Get placement details
                    placement_status = placement_form.cleaned_data.get('status', '').lower()
                    selected_program = placement_form.cleaned_data.get('selected_program', '') or ''
                    selected_program = str(selected_program).strip().upper()
                    
                    logger.info(f"📋 Placement Status: {placement_status}")
                    logger.info(f"📋 Selected Program: {selected_program}")

                    # Check requirements
                    requirement_confirmed = request.POST.get('confirm_approve_incomplete') == '1'
                    missing_requirements = get_missing_requirements(requirements_form.cleaned_data)
                    
                    if missing_requirements:
                        logger.warning(f"⚠️ Missing requirements: {', '.join(missing_requirements)}")

                    # Only auto-assign when status == 'approved'
                    if placement_status == 'approved':
                        logger.info("🎯 Status is 'approved' - proceeding with section assignment")
                        
                        # Check requirements before assignment
                        if missing_requirements and not requirement_confirmed:
                            logger.warning("⚠️ Requirements incomplete and not confirmed")
                            messages.warning(
                                request, 
                                f"Student marked as Approved but requirements incomplete: "
                                f"{', '.join(missing_requirements)}"
                            )
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                "requirement_missing_list": missing_requirements,
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)

                        # Validate program is selected
                        if not selected_program:
                            logger.error("❌ No program selected for approved student")
                            messages.error(
                                request,
                                "Cannot approve student without selecting a program. "
                                "Please select a program and try again."
                            )
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)

                        # Attempt section assignment
                        logger.info(f"🚀 Calling assign_student_to_section...")
                        
                        result = SectionAssignmentService.assign_student_to_section(
                            student, 
                            selected_program
                        )
                        
                        # Validate result
                        if result is None:
                            logger.error("❌ assign_student_to_section returned None!")
                            messages.error(
                                request,
                                "Section assignment failed: Service returned no result. "
                                "Please contact system administrator."
                            )
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                "section_assignment_error": "Service returned None",
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)
                        
                        # Unpack result
                        if not isinstance(result, tuple) or len(result) != 3:
                            logger.error(f"❌ Unexpected result format: {result}")
                            messages.error(
                                request,
                                f"Section assignment failed: Invalid result format. "
                                f"Please contact system administrator."
                            )
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                "section_assignment_error": f"Invalid result: {result}",
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)
                        
                        success, assigned_section, msg = result
                        
                        logger.info(f"📊 Assignment Result:")
                        logger.info(f"  Success: {success}")
                        logger.info(f"  Section: {assigned_section}")
                        logger.info(f"  Message: {msg}")

                        if success and assigned_section:
                            success_msg = (
                                f"✓ Student {student.first_name} {student.last_name} "
                                f"updated and assigned to {assigned_section.name} ({selected_program})"
                            )
                            messages.success(request, success_msg)
                            log_activity(
                                request.user, 
                                "Enrollment", 
                                f"Approved and assigned {student.first_name} {student.last_name} "
                                f"to {assigned_section.name} ({selected_program})"
                            )
                            logger.info(f"✅ {success_msg}")
                        else:
                            warning_msg = f"Student updated but section assignment failed: {msg}"
                            messages.warning(request, warning_msg)
                            log_activity(
                                request.user, 
                                "Enrollment", 
                                f"Updated {student.first_name} {student.last_name}, "
                                f"but section assignment failed: {msg}"
                            )
                            logger.warning(f"⚠️ {warning_msg}")
                            
                            context = {
                                "student": student,
                                "student_form": student_form,
                                "family_form": family_form,
                                "non_academic_form": non_academic_form,
                                "academic_form": academic_form,
                                "placement_form": placement_form,
                                "requirements_form": requirements_form,
                                "is_admin": request.user.is_staff,
                                "section_assignment_error": msg,
                                "section_program": selected_program.lower(),
                            }
                            return render(request, "admin_functionalities/student_edit.html", context)
                    else:
                        # Not approved: skip assignment
                        info_msg = (
                            f"Student {student.first_name} {student.last_name} updated. "
                            f"Section placement skipped (status: {placement_status})."
                        )
                        messages.success(request, info_msg)
                        log_activity(
                            request.user, 
                            "Enrollment", 
                            f"Updated student {student.first_name} {student.last_name} "
                            f"(status: {placement_status})"
                        )
                        logger.info(f"ℹ️ {info_msg}")

                logger.info(f"{'='*80}\n")
                return redirect("admin_functionalities:student_edit", student_id=student.id)

            except Exception as e:
                logger.error(f"❌ Error in student_edit_view for student {student.id}: {str(e)}")
                logger.exception("Full traceback:")
                messages.error(request, f"Error saving data: {e}")
                logger.info(f"{'='*80}\n")
    else:
        # GET request - initialize forms
        student_form = StudentForm(instance=student, user=request.user)
        family_form = FamilyForm(instance=get_family_or_create(student), user=request.user)
        non_academic_form = StudentNonAcademicForm(instance=get_non_academic_or_create(student), user=request.user)
        academic_form = StudentAcademicForm(instance=get_academic_or_create(student), user=request.user)
        placement_form = SectionPlacementForm(instance=get_placement_or_create(student), user=request.user)
        requirements_form = StudentRequirementsForm(instance=requirements)

    context = {
        "student": student,
        "student_form": student_form,
        "family_form": family_form,
        "non_academic_form": non_academic_form,
        "academic_form": academic_form,
        "placement_form": placement_form,
        "requirements_form": requirements_form,
        "is_admin": request.user.is_staff,
    }
    return render(request, "admin_functionalities/student_edit.html", context)


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only admin users can access views."""
    def test_func(self):
        return self.request.user.is_staff


class StudentAcademicUpdateView(AdminRequiredMixin, UpdateView):
    """View for updating student academic information."""
    model = StudentAcademic
    form_class = StudentAcademicForm
    template_name = 'enrollmentprocess/studentAcademic.html'

    def get_object(self, queryset=None):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        return get_object_or_404(StudentAcademic, student=student)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form = context['form']

        # Pre-fill LRN and lock it
        form.fields['lrn'].initial = student.lrn
        form.fields['lrn'].widget.attrs['readonly'] = True

        context['student_id'] = self.kwargs['student_id']
        context['is_working_student'] = "YES" if student.is_working_student else "NO"
        context['working_details'] = student.working_details or "N/A"
        context['is_pwd'] = "YES" if student.is_sped else "NO"
        context['disability_type'] = student.sped_details or "N/A"
        return context

    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        form.instance.student = student

        # Enforce values from Student model
        form.instance.is_working_student = student.is_working_student
        form.instance.work_type = student.working_details if student.is_working_student else None
        form.instance.is_pwd = student.is_sped
        form.instance.disability_type = student.sped_details if student.is_sped else None

        # Ensure LRN matches
        if form.cleaned_data['lrn'] != student.lrn:
            form.add_error('lrn', "LRN does not match the student's record.")
            return self.form_invalid(form)

        form.instance.overall_average = form.cleaned_data.get('overall_average', 0.0)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('admin_dashboard')