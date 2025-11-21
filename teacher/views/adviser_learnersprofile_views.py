from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from admin_functionalities.models import Teacher
from enrollmentprocess.models import Student, Family, StudentAcademic, StudentNonAcademic, SectionPlacement
from datetime import datetime


@login_required
def adviser_learnerprofile(request):
    """
    Display detailed learner profile for a specific student
    Accessed when teacher clicks "View" in masterlist
    """
    # Get student_id from query params
    student_id = request.GET.get('student_id')
    
    if not student_id:
        # Redirect back to masterlist if no student_id provided
        return redirect('teacher:adviser-masterlist')
    
    try:
        # Get the teacher profile
        teacher = Teacher.objects.select_related('user').get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('teacher:bothaccess-dashboard')
    
    # Get the student with related data
    student = get_object_or_404(
        Student.objects.select_related('family_data'),
        id=student_id
    )
    
    # Get family data
    family = student.family_data
    
    # Get academic data if exists
    try:
        academic = StudentAcademic.objects.get(student=student)
    except StudentAcademic.DoesNotExist:
        academic = None
    
    # Get non-academic data if exists
    try:
        non_academic = StudentNonAcademic.objects.get(student=student)
    except StudentNonAcademic.DoesNotExist:
        non_academic = None
    
    # Get section placement
    try:
        placement = SectionPlacement.objects.filter(
            student=student,
            status='approved'
        ).select_related('section').first()
        current_section = placement.section if placement else None
        current_program = placement.get_selected_program_display() if placement else 'Not Assigned'
    except:
        current_section = None
        current_program = 'Not Assigned'
    
    # Calculate age if date_of_birth exists
    age = student.age
    if not age and student.date_of_birth:
        today = datetime.today().date()
        age = today.year - student.date_of_birth.year - (
            (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day)
        )
    
    # Prepare student data
    student_data = {
        'id': student.id,
        'lrn': student.lrn,
        'last_name': student.last_name,
        'first_name': student.first_name,
        'middle_name': student.middle_name or 'N/A',
        'full_name': f"{student.last_name}, {student.first_name} {student.middle_name or ''}".strip(),
        'gender': student.gender,
        'age': age or 'N/A',
        'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else 'N/A',
        'place_of_birth': student.place_of_birth or 'N/A',
        'address': student.address or 'N/A',
        'religion': student.religion or 'N/A',
        'dialect': student.dialect_spoken or 'N/A',
        'ethnicity': student.ethnic_tribe or 'N/A',
        'photo_url': student.photo.url if student.photo else None,
        
        # School background
        'last_school': student.last_school_attended or 'N/A',
        'prev_grade_section': student.previous_grade_section or 'N/A',
        'last_school_year': student.last_school_year or 'N/A',
        
        # Enrollment details
        'current_program': current_program,
        'current_section': current_section.name if current_section else 'Not Assigned',
        'current_grade': 'Grade 7',  # Assuming Grade 7 for new enrollees
        'date_enrolled': placement.placement_date.strftime('%Y-%m-%d') if placement else 'N/A',
        'enrollment_status': student.section_placement or 'Pending',
        
        # Special needs
        'is_sped': student.is_sped,
        'sped_details': student.sped_details or 'N/A',
        'is_working_student': student.is_working_student,
        'working_details': student.working_details or 'N/A',
    }
    
    # Prepare family data
    family_data = None
    if family:
        # Calculate parent ages if DOB exists
        father_age = family.father_age
        if not father_age and family.father_dob:
            today = datetime.today().date()
            father_age = today.year - family.father_dob.year - (
                (today.month, today.day) < (family.father_dob.month, family.father_dob.day)
            )
        
        mother_age = family.mother_age
        if not mother_age and family.mother_dob:
            today = datetime.today().date()
            mother_age = today.year - family.mother_dob.year - (
                (today.month, today.day) < (family.mother_dob.month, family.mother_dob.day)
            )
        
        guardian_age = family.guardian_age if hasattr(family, 'guardian_age') else 'N/A'
        
        family_data = {
            # Father
            'father_last_name': family.father_family_name or 'N/A',
            'father_first_name': family.father_first_name or 'N/A',
            'father_middle_name': family.father_middle_name or 'N/A',
            'father_full_name': f"{family.father_family_name}, {family.father_first_name} {family.father_middle_name or ''}".strip(),
            'father_dob': family.father_dob.strftime('%Y-%m-%d') if family.father_dob else 'N/A',
            'father_age': father_age or 'N/A',
            'father_occupation': family.father_occupation or 'N/A',
            'father_contact': family.father_contact_number or 'N/A',
            'father_email': family.father_email or 'N/A',
            
            # Mother
            'mother_last_name': family.mother_family_name or 'N/A',
            'mother_first_name': family.mother_first_name or 'N/A',
            'mother_middle_name': family.mother_middle_name or 'N/A',
            'mother_full_name': f"{family.mother_family_name}, {family.mother_first_name} {family.mother_middle_name or ''}".strip(),
            'mother_dob': family.mother_dob.strftime('%Y-%m-%d') if family.mother_dob else 'N/A',
            'mother_age': mother_age or 'N/A',
            'mother_occupation': family.mother_occupation or 'N/A',
            'mother_contact': family.mother_contact_number or 'N/A',
            'mother_email': family.mother_email or 'N/A',
            
            # Guardian
            'guardian_last_name': family.guardian_family_name or 'N/A',
            'guardian_first_name': family.guardian_first_name or 'N/A',
            'guardian_middle_name': family.guardian_middle_name or 'N/A',
            'guardian_full_name': f"{family.guardian_family_name}, {family.guardian_first_name} {family.guardian_middle_name or ''}".strip() if family.guardian_family_name else 'N/A',
            'guardian_relationship': family.guardian_relationship or 'N/A',
            'guardian_contact': family.guardian_contact_number or 'N/A',
            'guardian_address': family.guardian_address or student.address or 'N/A',
            'guardian_dob': family.guardian_dob.strftime('%Y-%m-%d') if hasattr(family, 'guardian_dob') and family.guardian_dob else 'N/A',
            'guardian_age': guardian_age,
            'guardian_email': family.guardian_email if hasattr(family, 'guardian_email') else 'N/A',
            'guardian_occupation': family.guardian_occupation if hasattr(family, 'guardian_occupation') else 'N/A',
            
            # Parent photo
            'parent_photo_url': family.parent_photo.url if family.parent_photo else None,
        }
    else:
        # No family data available
        family_data = {
            'father_last_name': 'N/A',
            'father_first_name': 'N/A',
            'father_middle_name': 'N/A',
            'father_full_name': 'N/A',
            'father_dob': 'N/A',
            'father_age': 'N/A',
            'father_occupation': 'N/A',
            'father_contact': 'N/A',
            'father_email': 'N/A',
            
            'mother_last_name': 'N/A',
            'mother_first_name': 'N/A',
            'mother_middle_name': 'N/A',
            'mother_full_name': 'N/A',
            'mother_dob': 'N/A',
            'mother_age': 'N/A',
            'mother_occupation': 'N/A',
            'mother_contact': 'N/A',
            'mother_email': 'N/A',
            
            'guardian_last_name': 'N/A',
            'guardian_first_name': 'N/A',
            'guardian_middle_name': 'N/A',
            'guardian_full_name': 'N/A',
            'guardian_relationship': 'N/A',
            'guardian_contact': 'N/A',
            'guardian_address': 'N/A',
            'guardian_dob': 'N/A',
            'guardian_age': 'N/A',
            'guardian_email': 'N/A',
            'guardian_occupation': 'N/A',
            
            'parent_photo_url': None,
        }
    
    # Prepare academic data (if exists)
    academic_data = None
    if academic:
        academic_data = {
            'mathematics': academic.mathematics,
            'araling_panlipunan': academic.araling_panlipunan,
            'english': academic.english,
            'edukasyon_pagpapakatao': academic.edukasyon_pagpapakatao,
            'science': academic.science,
            'edukasyon_pangkabuhayan': academic.edukasyon_pangkabuhayan,
            'filipino': academic.filipino,
            'mapeh': academic.mapeh,
            'overall_average': academic.overall_average,
            'dost_exam_result': academic.dost_exam_result or 'N/A',
            'report_card_url': academic.report_card.url if academic.report_card else None,
        }
    
    # Prepare non-academic data (if exists)
    non_academic_data = None
    if non_academic:
        non_academic_data = {
            'study_hours': non_academic.study_hours or 'N/A',
            'study_place': non_academic.study_place or 'N/A',
            'study_with': non_academic.study_with or 'N/A',
            'live_with': non_academic.live_with or 'N/A',
            'parent_help': non_academic.parent_help or 'N/A',
            'highest_education': non_academic.highest_education or 'N/A',
            'marital_status': non_academic.marital_status or 'N/A',
            'house_type': non_academic.house_type or 'N/A',
            'quiet_place': non_academic.quiet_place or 'N/A',
            'study_area': non_academic.study_area or 'N/A',
            'transport_mode': non_academic.transport_mode or 'N/A',
            'travel_time': non_academic.travel_time or 'N/A',
            'access_resources': non_academic.access_resources or 'N/A',
            'computer_use': non_academic.computer_use or 'N/A',
            'hobbies': non_academic.hobbies or 'N/A',
            'personality_traits': non_academic.personality_traits or 'N/A',
            'confidence_level': non_academic.confidence_level or 'N/A',
        }
    
    context = {
        'teacher': teacher,
        'student': student_data,
        'family': family_data,
        'academic': academic_data,
        'non_academic': non_academic_data,
    }
    
    return render(request, 'teacher/adviser/Learner_Profile.html', context)