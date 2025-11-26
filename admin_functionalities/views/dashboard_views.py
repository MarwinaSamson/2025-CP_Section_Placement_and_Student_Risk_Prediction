# ============================================================================
# 3. admin_functionalities/views/dashboard_views.py
# ============================================================================
"""
Dashboard views for admin functionalities.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from admin_functionalities.models import Notification, Section, Teacher, Program
from enrollmentprocess.models import Student, SectionPlacement


@login_required
def admin_dashboard(request):
    """Main admin dashboard with statistics and notifications."""
    
    # Quick Statistics
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    total_sections = Section.objects.count()
    grade7_students = Student.objects.count()  # Temporary until grade levels exist

    programs = [choice[0] for choice in SectionPlacement.PROGRAM_CHOICES]
    total_programs = len(programs)

    # Program Overview Table
    program_data = []
    for prog in programs:
        placements = SectionPlacement.objects.filter(selected_program__iexact=prog)
        total_applicants = placements.count()
        approved = placements.filter(status__iexact='approved').count()
        pending = placements.filter(status__iexact='pending').count()
        rejected = placements.filter(status__iexact='rejected').count()
        num_sections = Section.objects.filter(program__name__iexact=prog).count()

        program_data.append({
            "program": prog,
            "total_applicants": total_applicants,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "num_sections": num_sections,
        })

    # Enrollment Notifications
    unread_enrollments = Notification.objects.filter(
        notification_type='student_enrollment',
        is_read=False
    ).values('program').annotate(count=Count('id')).order_by('-count')

    notifications = []
    for item in unread_enrollments:
        program_code = item['program'].lower()
        count = item['count']

        latest_notif = Notification.objects.filter(
            program__iexact=program_code, is_read=False
        ).order_by('-created_at').first()

        notification_ids = list(
            Notification.objects.filter(
                program__iexact=program_code, is_read=False
            ).values_list('id', flat=True)
        )

        notifications.append({
            'title': 'New Enrollment Requests',
            'message': f'{count} new enrollment request{"s" if count > 1 else ""} for {program_code.upper()}',
            'type': 'student_enrollment',
            'program': program_code,
            'count': count,
            'icon': 'fas fa-user-plus',
            'sample_message': latest_notif.message if latest_notif else '',
            'notification_ids': notification_ids,
            'program_slug': program_code,
        })

    total_unread = sum(item['count'] for item in unread_enrollments)

    context = {
        # Quick Stats
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_programs": total_programs,
        "total_sections": total_sections,
        "grade7_students": grade7_students,

        # Program Overview
        "program_data": program_data,

        # Notifications
        "notifications": notifications,
        "total_unread": total_unread,
    }

    return render(request, "admin_functionalities/admin-dashboard.html", context)