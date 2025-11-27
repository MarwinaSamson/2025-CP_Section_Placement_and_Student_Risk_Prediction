# teacher/views/adviser_masterlist_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from admin_functionalities.models import Teacher, Section
from enrollmentprocess.models import Student, StudentAcademic
from teacher.models import (
    AdviserMasterlist, 
    MasterlistStudent, 
    QuarterEnrollment,
    StudentGrade,
    ClassRecord
)
import json


@login_required
def adviser_masterlist(request):
    """
    Main masterlist view - shows all students in adviser's section
    """
    user = request.user
    
    # Get teacher profile
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return redirect('login')
    
    # Get advisory section
    advisory_section = Section.objects.filter(adviser=teacher).first()
    
    if not advisory_section:
        context = {
            'teacher': teacher,
            'has_advisory_class': False,
            'error_message': 'You do not have an assigned advisory class.',
        }
        return render(request, 'teacher/adviser/Masterlist.html', context)
    
    # Get or create masterlist for current school year
    school_year = '2025-2026'  # Can be dynamic later
    masterlist, created = AdviserMasterlist.objects.get_or_create(
        adviser=teacher,
        section=advisory_section,
        school_year=school_year,
        defaults={'is_active': True}
    )
    
    # FIXED: Get students assigned to this section through SectionPlacement
    # Import SectionPlacement model
    from enrollmentprocess.models import SectionPlacement
    
    # Get students who have approved placements in this section
    students = Student.objects.filter(
        section_placements__section=advisory_section,
        section_placements__status='approved'  # Only approved placements
    ).select_related('studentacademic').distinct().order_by(
        'last_name', 'first_name'
    )
    
    # If no approved students, try getting all students with any placement status
    if not students.exists():
        students = Student.objects.filter(
            section_placements__section=advisory_section
        ).select_related('studentacademic').distinct().order_by(
            'last_name', 'first_name'
        )
    
    # Ensure all students are in masterlist
    for student in students:
        MasterlistStudent.objects.get_or_create(
            masterlist=masterlist,
            student=student,
            defaults={
                'status': 'Active',
                'is_active': True
            }
        )
    
    # Get masterlist students with additional data
    masterlist_students = MasterlistStudent.objects.filter(
        masterlist=masterlist,
        is_active=True
    ).select_related('student', 'student__studentacademic').order_by(
        'student__last_name', 
        'student__first_name'
    )
    
    # Build student data list
    students_data = []
    for ms in masterlist_students:
        student = ms.student
        
        # Get academic data if available
        try:
            academic = student.studentacademic
            overall_avg = academic.overall_average
            is_probation = overall_avg < 70 if overall_avg else False
        except (StudentAcademic.DoesNotExist, AttributeError):
            overall_avg = None
            is_probation = False
        
        # Check quarter enrollment (Q1 for now)
        quarter_enrolled = QuarterEnrollment.objects.filter(
            masterlist_student=ms,
            quarter='Q1',
            is_enrolled=True
        ).exists()
        
        students_data.append({
            'id': student.id,
            'lrn': student.lrn,
            'full_name': f"{student.last_name}, {student.first_name} {student.middle_name or ''}".strip(),
            'last_name': student.last_name,
            'first_name': student.first_name,
            'middle_name': student.middle_name or '',
            'gender': student.gender,
            'age': student.age,
            'photo': student.photo.url if student.photo else None,
            'overall_average': overall_avg,
            'is_probation': is_probation,
            'status': ms.status,
            'is_honor': ms.is_honor_student,
            'is_at_risk': ms.is_at_risk,
            'has_intervention': ms.has_intervention,
            'quarter_enrolled': quarter_enrolled,
        })
    
    # Calculate statistics
    total_students = len(students_data)
    male_count = len([s for s in students_data if s['gender'] == 'Male'])
    female_count = len([s for s in students_data if s['gender'] == 'Female'])
    
    # Generate teacher initials
    teacher_initials = _get_initials(teacher)
    
    context = {
        'teacher': teacher,
        'teacher_full_name': f"{teacher.last_name}, {teacher.first_name} {teacher.middle_name or ''}".strip(),
        'teacher_position': teacher.position if teacher.position else 'Adviser',
        'teacher_photo': teacher.profile_photo.url if teacher.profile_photo else None,
        'teacher_initials': teacher_initials,
        
        'has_advisory_class': True,
        'advisory_section': advisory_section,
        'program': advisory_section.program.name,
        'program_code': advisory_section.program,
        'section_name': advisory_section.name,
        'full_section_name': f"{advisory_section.program}-{advisory_section.name}",
        
        'masterlist': masterlist,
        'students': students_data,
        'total_students': total_students,
        'male_count': male_count,
        'female_count': female_count,
        
        'school_year': school_year,
        'quarters': ['Q1', 'Q2', 'Q3', 'Q4'],
        'current_quarter': 'Q1',
    }
    
    return render(request, 'teacher/adviser/Masterlist.html', context)


@login_required
def get_student_grades(request, student_id):
    """
    API endpoint to get student's grades for a specific quarter
    Returns JSON with all subject grades
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    quarter = request.GET.get('quarter', 'Q1')
    school_year = request.GET.get('school_year', '2025-2026')
    
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    
    # Get all grades for this student in this quarter
    grades = StudentGrade.objects.filter(
        student=student,
        class_record__quarter=quarter,
        class_record__school_year=school_year
    ).select_related('class_record__subject')
    
    # Build grades list
    grades_data = []
    total_grade = 0
    count = 0
    
    for grade in grades:
        subject_name = grade.class_record.subject.subject_name
        quarterly_grade = grade.quarterly_grade
        
        grades_data.append({
            'subject': subject_name,
            'grade': quarterly_grade,
            'ww_percentage': round(grade.ww_percentage, 2),
            'pt_percentage': round(grade.pt_percentage, 2),
            'qa_percentage': round(grade.qa_percentage, 2),
            'initial_grade': round(grade.initial_grade, 2),
        })
        
        if quarterly_grade > 0:
            total_grade += quarterly_grade
            count += 1
    
    # Calculate average
    average = round(total_grade / count) if count > 0 else 0
    
    # Get student info
    student_info = {
        'id': student.id,
        'lrn': student.lrn,
        'full_name': f"{student.last_name}, {student.first_name} {student.middle_name or ''}".strip(),
        'gender': student.gender,
        'age': student.age,
        'photo': student.photo.url if student.photo else None,
    }
    
    return JsonResponse({
        'student': student_info,
        'grades': grades_data,
        'average': average,
        'quarter': quarter,
        'school_year': school_year,
    })


@login_required
def update_student_status(request, student_id):
    """
    Update student's masterlist status (Active, Probation, Dropped, etc.)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        status = data.get('status')
        
        if status not in dict(MasterlistStudent.STATUS_CHOICES):
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        # Get masterlist student
        student = Student.objects.get(id=student_id)
        advisory_section = Section.objects.filter(adviser=teacher).first()
        
        if not advisory_section:
            return JsonResponse({'error': 'No advisory section'}, status=403)
        
        masterlist = AdviserMasterlist.objects.get(
            adviser=teacher,
            section=advisory_section,
            school_year='2025-2026'
        )
        
        masterlist_student = MasterlistStudent.objects.get(
            masterlist=masterlist,
            student=student
        )
        
        masterlist_student.status = status
        masterlist_student.save()
        
        return JsonResponse({
            'success': True,
            'student_id': student_id,
            'status': status
        })
        
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except AdviserMasterlist.DoesNotExist:
        return JsonResponse({'error': 'Masterlist not found'}, status=404)
    except MasterlistStudent.DoesNotExist:
        return JsonResponse({'error': 'Student not in masterlist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def toggle_quarter_enrollment(request, student_id):
    """
    Toggle student's enrollment status for a specific quarter
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    
    try:
        data = json.loads(request.body)
        quarter = data.get('quarter', 'Q1')
        is_enrolled = data.get('is_enrolled', True)
        
        # Get masterlist student
        student = Student.objects.get(id=student_id)
        advisory_section = Section.objects.filter(adviser=teacher).first()
        
        if not advisory_section:
            return JsonResponse({'error': 'No advisory section'}, status=403)
        
        masterlist = AdviserMasterlist.objects.get(
            adviser=teacher,
            section=advisory_section,
            school_year='2025-2026'
        )
        
        masterlist_student = MasterlistStudent.objects.get(
            masterlist=masterlist,
            student=student
        )
        
        # Get or create quarter enrollment
        quarter_enrollment, created = QuarterEnrollment.objects.get_or_create(
            masterlist_student=masterlist_student,
            quarter=quarter,
            defaults={'is_enrolled': is_enrolled}
        )
        
        if not created:
            quarter_enrollment.is_enrolled = is_enrolled
            quarter_enrollment.save()
        
        return JsonResponse({
            'success': True,
            'student_id': student_id,
            'quarter': quarter,
            'is_enrolled': is_enrolled
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def _get_initials(teacher):
    """Helper function to generate teacher initials"""
    if teacher.first_name and teacher.last_name:
        return f"{teacher.first_name[0]}{teacher.last_name[0]}".upper()
    elif teacher.first_name:
        return teacher.first_name[0].upper()
    elif teacher.last_name:
        return teacher.last_name[0].upper()
    return "T"