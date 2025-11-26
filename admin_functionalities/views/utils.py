# ============================================================================
# 2. admin_functionalities/views/utils.py
# ============================================================================
"""
Shared helper functions for views.
"""

from enrollmentprocess.models import (
    Family,
    StudentNonAcademic,
    StudentAcademic,
    SectionPlacement,
)


def get_or_create_related(model, student, defaults=None):
    """Generic helper: Get or create related instance."""
    if defaults is None:
        defaults = {}
    try:
        instance, created = model.objects.get_or_create(student=student, defaults=defaults)
        return instance
    except Exception as e:
        print(f"Error in get_or_create for {model.__name__}: {e}")
        return model(student=student)


def _get_user_role(user):
    """Return a readable role name for a CustomUser."""
    if user.is_superuser:
        return "Administrator"
    elif getattr(user, 'is_staff_expert', False):
        return "Staff Expert"
    elif getattr(user, 'is_subject_teacher', False):
        return "Subject Teacher"
    elif getattr(user, 'is_adviser', False):
        return "Adviser"
    return "User"


def get_family_or_create(student):
    """Get or create Family instance for student."""
    return get_or_create_related(Family, student, defaults={
        'father_family_name': '',
        'father_first_name': '',
        'father_middle_name': '',
        'father_age': 0,
        'father_occupation': '',
        'father_dob': None,
        'father_contact_number': '',
        'father_email': '',
        'mother_family_name': '',
        'mother_first_name': '',
        'mother_middle_name': '',
        'mother_age': 0,
        'mother_occupation': '',
        'mother_dob': None,
        'mother_contact_number': '',
        'mother_email': '',
        'guardian_family_name': '',
        'guardian_first_name': '',
        'guardian_middle_name': '',
        'guardian_age': 0,
        'guardian_occupation': '',
        'guardian_dob': None,
        'guardian_address': '',
        'guardian_relationship': '',
        'guardian_contact_number': '',
        'guardian_email': '',
        'parent_photo': None,
    })


def get_non_academic_or_create(student):
    """Get or create StudentNonAcademic instance for student."""
    return get_or_create_related(StudentNonAcademic, student, defaults={
        'study_hours': '',
        'study_place': '',
        'study_with': '',
        'live_with': '',
        'parent_help': '',
        'highest_education': '',
        'marital_status': '',
        'house_type': '',
        'quiet_place': '',
        'study_area': '',
        'transport_mode': '',
        'travel_time': '',
        'access_resources': '',
        'computer_use': '',
        'confidence_level': '',
        'hobbies': '',
        'personality_traits': '',
    })


def get_academic_or_create(student):
    """Get or create StudentAcademic instance for student."""
    return get_or_create_related(StudentAcademic, student, defaults={
        'lrn': student.lrn if hasattr(student, 'lrn') else '',
        'dost_exam_result': '',
        'report_card': None,
        'mathematics': 0.0,
        'araling_panlipunan': 0.0,
        'english': 0.0,
        'edukasyon_pagpapakatao': 0.0,
        'science': 0.0,
        'edukasyon_pangkabuhayan': 0.0,
        'filipino': 0.0,
        'mapeh': 0.0,
        'agreed_to_terms': False,
    })


def get_placement_or_create(student):
    """Get or create SectionPlacement instance for student."""
    try:
        placement = SectionPlacement.objects.filter(student=student).latest('id')
        return placement
    except SectionPlacement.DoesNotExist:
        pass
    
    placement = SectionPlacement.objects.create(
        student=student,
        status='pending',
        selected_program='regular'
    )
    print(f"DEBUG: Created new placement {placement.id} for student {student.id}")
    return placement