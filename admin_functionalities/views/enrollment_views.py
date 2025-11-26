# ============================================================================
# 6. admin_functionalities/views/enrollment_views.py
# ============================================================================
"""
Enrollment management views.
"""

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from admin_functionalities.models import Notification
from admin_functionalities.utils import log_activity
from enrollmentprocess.models import SectionPlacement


@login_required
def enrollment_view(request):
    """
    Enrollment management view with proper filtering for both program and status.
    """
    # Get filters from URL params
    program_filter = request.GET.get('program', 'all')
    status_filter = request.GET.get('status', 'pending')
    
    # Base query
    queryset = SectionPlacement.objects.select_related('student').order_by('-placement_date', '-id')
    
    # Apply program filter
    if program_filter and program_filter != 'all':
        queryset = queryset.filter(selected_program__iexact=program_filter)
    
    # Apply status filter
    if status_filter and status_filter != 'all':
        queryset = queryset.filter(status=status_filter)
    
    # Fetch enrollments
    enrollments = list(queryset.values(
        'id',
        'student__id',
        'student__lrn',
        'student__first_name',
        'student__middle_name',
        'student__last_name',
        'selected_program',
        'status',
        'placement_date'
    ))
    
    # Calculate stats based on current filters
    if program_filter and program_filter != 'all':
        stats_queryset = SectionPlacement.objects.filter(selected_program__iexact=program_filter)
        total_requests = stats_queryset.count()
        approved = stats_queryset.filter(status='approved').count()
        pending = stats_queryset.filter(status='pending').count()
        rejected = stats_queryset.filter(status='rejected').count()
    else:
        total_requests = SectionPlacement.objects.count()
        approved = SectionPlacement.objects.filter(status='approved').count()
        pending = SectionPlacement.objects.filter(status='pending').count()
        rejected = SectionPlacement.objects.filter(status='rejected').count()
    
    # Program display mapping
    PROGRAM_DISPLAY_NAMES = {
        'ste': 'STE',
        'spfl': 'SPFL',
        'sptve': 'SPTVE',
        'sned': 'SNED',
        'top5': 'TOP 5',
        'hetero': 'HETERO',
        'ohsp': 'OHSP',
        'regular': 'Regular',
    }
    
    # Determine display name
    if program_filter == 'all':
        display_name = 'All Programs'
    else:
        display_name = PROGRAM_DISPLAY_NAMES.get(program_filter.lower(), program_filter.upper())
    
    is_filtered = (program_filter != 'all' or status_filter != 'pending')
    
    context = {
        'enrollments': enrollments,
        'total_requests': total_requests,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'program_filter': program_filter,
        'status_filter': status_filter,
        'display_name': display_name,
        'is_filtered': is_filtered,
    }
    
    return render(request, 'admin_functionalities/enrollment-management.html', context)


@csrf_exempt
def mark_notification_read(request):
    """Mark notifications as read."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            if ids:
                Notification.objects.filter(id__in=ids).update(is_read=True)
                log_activity(request.user, "Notifications", f"Marked {len(ids)} notification(s) as read")
                return JsonResponse({'success': True, 'marked': len(ids)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False}, status=400)