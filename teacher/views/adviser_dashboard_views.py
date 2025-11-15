from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from admin_functionalities.models import Teacher, Section, SectionSubjectAssignment
from enrollmentprocess.models import Student

@login_required
def bothaccess_dashboard(request):
    """
    Adviser Dashboard - Shows overview for teachers with adviser + subject teacher access
    """
    user = request.user
    
    # Get teacher profile
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        # Redirect to error page or login if teacher profile doesn't exist
        return redirect('login')  # Adjust to your login URL name

    # Get advisory class (section where this teacher is the adviser)
    advisory_section = Section.objects.filter(adviser=teacher).first()

    # Count students in advisory class
    advisory_students_count = 0
    advisory_section_name = "Not Assigned"
    if advisory_section:
        # Count students assigned to this section using the section_placement field
        advisory_students_count = Student.objects.filter(
            section_placement=f"{advisory_section.program}-{advisory_section.name}"
        ).count()
        advisory_section_name = f"{advisory_section.program}-{advisory_section.name}"
        advisory_students_count = advisory_section.current_students

    # Get sections handled as subject teacher
    subject_assignments = SectionSubjectAssignment.objects.filter(
    teacher=teacher
    ).select_related('section')

    # Count unique sections (a teacher might teach multiple subjects in same section)
    sections_handled = subject_assignments.values('section_id').distinct().count()

    # Count unique subjects taught
    subjects_handled = subject_assignments.values('subject').distinct().count()
    # Count total students across all sections
    section_ids = subject_assignments.values_list('section_id', flat=True).distinct()
    total_students = sum(
        Section.objects.filter(id__in=section_ids).values_list('current_students', flat=True)
    )

    # At-risk students - STATIC for now (ML model not ready yet)
    # TODO: Replace with ML model prediction when ready
    at_risk_students = 11  # Static placeholder value

    # Generate teacher initials for profile photo fallback
    teacher_initials = ""
    if teacher.first_name and teacher.last_name:
        teacher_initials = f"{teacher.first_name[0]}{teacher.last_name[0]}".upper()
    elif teacher.first_name:
        teacher_initials = teacher.first_name[0].upper()
    elif teacher.last_name:
        teacher_initials = teacher.last_name[0].upper()
    else:
        teacher_initials = "T"

    # Prepare context data
    context = {
        'teacher': teacher,
        'teacher_full_name': f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name}".strip(),
        'teacher_position': teacher.position if teacher.position else 'Teacher',
        'teacher_photo': teacher.profile_photo.url if teacher.profile_photo else None,
        'teacher_initials': teacher_initials,
        
        # Advisory class info
        'advisory_section_name': advisory_section_name,
        'advisory_students_count': advisory_students_count,
        'has_advisory_class': advisory_section is not None,
        
        # Stats cards
        'sections_handled': sections_handled,
        'subjects_handled': subjects_handled,
        'total_students': total_students,
        'at_risk_students': at_risk_students,  # Static for now
        
        # For school year dropdown (display only for now)
        'current_school_year': '2025-2026',
    }

    return render(request, 'teacher/adviser/Teacher_Landingpage.html', context)