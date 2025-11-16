# teacher/views/adviser_attendance_views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.utils import timezone
from datetime import date, timedelta
import json

from teacher.models import AttendanceRecord, StudentAttendance, AttendanceHistory
from enrollmentprocess.models import Student
from admin_functionalities.models import Teacher, Section, SchoolYear
from enrollmentprocess.models import SectionPlacement


@login_required
def adviser_attendance(request):
    """
    Main attendance page view.
    Renders the attendance template with necessary context.
    """
    try:
        # Get logged-in teacher
        teacher = Teacher.objects.get(user=request.user)
        
        # Get sections where this teacher is adviser
        sections = Section.objects.filter(
            adviser=teacher,
            is_active=True
        ).order_by('name')
        
        # Get current school year
        current_school_year = SchoolYear.get_current()
        
        context = {
            'teacher': teacher,
            'sections': sections,
            'current_school_year': current_school_year,
            'page_title': 'SF2 - Daily Attendance',
        }
        
        return render(request, 'teacher/adviser/attendance.html', context)
        
    except Teacher.DoesNotExist:
        return render(request, 'teacher/error.html', {
            'error_message': 'Teacher profile not found. Please contact administrator.'
        })
    except Exception as e:
        return render(request, 'teacher/error.html', {
            'error_message': f'An error occurred: {str(e)}'
        })


@login_required
@require_http_methods(["GET"])
def get_section_info(request, section_id):
    """
    API endpoint to get section information when selected.
    Returns: section details, grade level, students list.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        section = get_object_or_404(Section, id=section_id, adviser=teacher)
        
        # Get grade level from section
        # Assuming section has grade level info or we derive from program
        grade_level = "Grade 7"  # Default, adjust based on your section model
        
        # Get students in this section
        # Using SectionPlacement to get students assigned to this section
        placements = SectionPlacement.objects.filter(
            section=section,
            status='approved'
        ).select_related('student').order_by('student__gender', 'student__last_name')
        
        students_data = []
        for placement in placements:
            student = placement.student
            students_data.append({
                'id': student.id,
                'lrn': student.lrn,
                'name': f"{student.last_name}, {student.first_name} {student.middle_name}".strip(),
                'last_name': student.last_name,
                'first_name': student.first_name,
                'middle_name': student.middle_name or '',
                'gender': student.gender,  # 'Male' or 'Female'
            })
        
        return JsonResponse({
            'success': True,
            'section': {
                'id': section.id,
                'name': section.name,
                'program': section.program,
                'grade_level': grade_level,
                'building': section.building,
                'room': section.room,
            },
            'students': students_data,
        })
        
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Teacher not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def get_quarter_months(request):
    """
    API endpoint to get available months for a selected quarter.
    Returns months that fall within the quarter's date range.
    """
    try:
        quarter = request.GET.get('quarter')  # 'Q1', 'Q2', etc.
        school_year_id = request.GET.get('school_year_id')
        
        if not quarter or not school_year_id:
            return JsonResponse({
                'success': False,
                'error': 'Quarter and school_year_id required'
            }, status=400)
        
        school_year = get_object_or_404(SchoolYear, id=school_year_id)
        
        # Get start and end dates for the quarter
        start_date, end_date = school_year.get_quarter_dates(quarter)
        
        if not start_date or not end_date:
            return JsonResponse({
                'success': False,
                'error': 'Invalid quarter dates'
            }, status=400)
        
        # Get all unique months in the quarter
        months = []
        current_date = start_date.replace(day=1)
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            months.append({
                'value': f"{current_date.year}-{current_date.month:02d}",
                'label': current_date.strftime('%B %Y'),
                'year': current_date.year,
                'month': current_date.month,
            })
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return JsonResponse({
            'success': True,
            'months': months,
            'quarter_start': start_date.isoformat(),
            'quarter_end': end_date.isoformat(),
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def load_attendance_record(request):
    """
    Load existing attendance record or create new one.
    Returns attendance data for the specified section/month.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        # Get parameters
        section_id = request.GET.get('section_id')
        school_year_id = request.GET.get('school_year_id')
        quarter = request.GET.get('quarter')
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        if not all([section_id, school_year_id, quarter, month, year]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required parameters'
            }, status=400)
        
        section = get_object_or_404(Section, id=section_id, adviser=teacher)
        school_year = get_object_or_404(SchoolYear, id=school_year_id)
        
        # Try to get existing record
        attendance_record, created = AttendanceRecord.objects.get_or_create(
            section=section,
            teacher=teacher,
            school_year=school_year,
            quarter=quarter,
            month=int(month),
            year=int(year),
            defaults={
                'school_name': 'Cagayan de Oro National High School',
                'school_id': '304144',
                'grade_level': 'Grade 7',  # Adjust as needed
                'adviser_name': teacher.full_name,
                'principal_name': 'Name of Principal',
            }
        )
        
        # Calculate school days if new record
        if created:
            attendance_record.calculate_school_days()
            attendance_record.save()
        
        # Get or create student attendance entries
        students = Student.objects.filter(
            section_placements__section=section,
            section_placements__status='approved'
        ).distinct().order_by('gender', 'last_name')
        
        student_attendance_data = []
        
        for student in students:
            student_att, created = StudentAttendance.objects.get_or_create(
                attendance_record=attendance_record,
                student=student,
                defaults={
                    'daily_attendance': [''] * attendance_record.total_days
                }
            )
            
            student_attendance_data.append({
                'id': student_att.id,
                'student_id': student.id,
                'student_name': f"{student.last_name}, {student.first_name} {student.middle_name}".strip(),
                'gender': student.gender,
                'daily_attendance': student_att.daily_attendance,
                'total_absences': student_att.total_absences,
                'total_tardies': student_att.total_tardies,
                'total_present': student_att.total_present,
                'remarks': student_att.remarks,
                'is_at_risk': student_att.is_at_risk,
                'is_dropout': student_att.is_dropout,
                'warning_message': student_att.get_warning_message(),
                'has_valid_excuse': student_att.has_valid_excuse,
            })
        
        return JsonResponse({
            'success': True,
            'record': {
                'id': attendance_record.id,
                'total_days': attendance_record.total_days,
                'school_name': attendance_record.school_name,
                'school_id': attendance_record.school_id,
                'grade_level': attendance_record.grade_level,
                'adviser_name': attendance_record.adviser_name,
                'principal_name': attendance_record.principal_name,
                'is_finalized': attendance_record.is_finalized,
                
                # Summary data
                'enrollment_male': attendance_record.enrollment_male,
                'enrollment_female': attendance_record.enrollment_female,
                'late_enrollees_male': attendance_record.late_enrollees_male,
                'late_enrollees_female': attendance_record.late_enrollees_female,
                'registered_male': attendance_record.registered_male,
                'registered_female': attendance_record.registered_female,
                'avg_attendance_male': float(attendance_record.avg_attendance_male),
                'avg_attendance_female': float(attendance_record.avg_attendance_female),
                'attendance_percentage_male': float(attendance_record.attendance_percentage_male),
                'attendance_percentage_female': float(attendance_record.attendance_percentage_female),
                'dropped_male': attendance_record.dropped_male,
                'dropped_female': attendance_record.dropped_female,
                'transferred_out_male': attendance_record.transferred_out_male,
                'transferred_out_female': attendance_record.transferred_out_female,
                'transferred_in_male': attendance_record.transferred_in_male,
                'transferred_in_female': attendance_record.transferred_in_female,
            },
            'students': student_attendance_data,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def save_attendance(request):
    """
    Save attendance data for the current record.
    Updates student attendance and summary statistics.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        data = json.loads(request.body)
        
        record_id = data.get('record_id')
        students_data = data.get('students', [])
        summary_data = data.get('summary', {})
        header_data = data.get('header', {})
        
        # Get attendance record
        attendance_record = get_object_or_404(
            AttendanceRecord,
            id=record_id,
            teacher=teacher
        )
        
        # Check if finalized
        if attendance_record.is_finalized:
            return JsonResponse({
                'success': False,
                'error': 'Cannot edit finalized attendance record'
            }, status=400)
        
        # Update header data
        if header_data:
            attendance_record.school_name = header_data.get('school_name', attendance_record.school_name)
            attendance_record.school_id = header_data.get('school_id', attendance_record.school_id)
            attendance_record.grade_level = header_data.get('grade_level', attendance_record.grade_level)
            attendance_record.adviser_name = header_data.get('adviser_name', attendance_record.adviser_name)
            attendance_record.principal_name = header_data.get('principal_name', attendance_record.principal_name)
        
        # Update late enrollees (user input fields)
        if summary_data:
            attendance_record.late_enrollees_male = summary_data.get('late_enrollees_male', 0)
            attendance_record.late_enrollees_female = summary_data.get('late_enrollees_female', 0)
        
        # Update student attendance entries
        for student_data in students_data:
            student_att_id = student_data.get('id')
            if not student_att_id:
                continue
            
            try:
                student_att = StudentAttendance.objects.get(
                    id=student_att_id,
                    attendance_record=attendance_record
                )
                
                # Update daily attendance
                student_att.daily_attendance = student_data.get('daily_attendance', [])
                student_att.remarks = student_data.get('remarks', '')
                student_att.has_valid_excuse = student_data.get('has_valid_excuse', False)
                
                # Save will auto-calculate totals and update flags
                student_att.save()
                
            except StudentAttendance.DoesNotExist:
                continue
        
        # Recalculate summary statistics
        attendance_record.update_summary_statistics()
        attendance_record.save()
        
        # Create history log
        AttendanceHistory.objects.create(
            attendance_record=attendance_record,
            action='updated',
            modified_by=teacher,
            snapshot_data={
                'total_students': attendance_record.enrollment_male + attendance_record.enrollment_female,
                'total_absences': sum(s.total_absences for s in attendance_record.student_attendance.all()),
                'at_risk_count': attendance_record.get_at_risk_students().count(),
                'dropout_count': attendance_record.get_dropout_students().count(),
            },
            notes=f"Attendance updated for {attendance_record.get_month_name()} {attendance_record.year}"
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Attendance saved successfully',
            'record_id': attendance_record.id,
            'updated_at': attendance_record.updated_at.isoformat(),
        })
        
    except Teacher.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Teacher not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def update_student_excuse(request, student_att_id):
    """
    Toggle valid excuse flag for a student.
    Used when teacher wants to excuse absences (prevent dropout warning).
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        data = json.loads(request.body)
        
        has_valid_excuse = data.get('has_valid_excuse', False)
        
        # Get student attendance
        student_att = get_object_or_404(
            StudentAttendance,
            id=student_att_id,
            attendance_record__teacher=teacher
        )
        
        # Update excuse flag
        student_att.has_valid_excuse = has_valid_excuse
        student_att.save()  # Will recalculate flags
        
        return JsonResponse({
            'success': True,
            'message': 'Valid excuse updated',
            'is_at_risk': student_att.is_at_risk,
            'is_dropout': student_att.is_dropout,
            'warning_message': student_att.get_warning_message(),
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def get_attendance_history(request):
    """
    Get history of saved attendance records for the sidebar.
    Returns list of all attendance records by this teacher.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        # Get all attendance records for this teacher
        records = AttendanceRecord.objects.filter(
            teacher=teacher
        ).select_related('section', 'school_year').order_by('-year', '-month')
        
        history_data = []
        for record in records:
            history_data.append({
                'id': record.id,
                'section_name': record.section.name,
                'month_name': record.get_month_name(),
                'year': record.year,
                'quarter': record.quarter,
                'school_year': record.school_year.name,
                'total_students': record.enrollment_male + record.enrollment_female,
                'is_finalized': record.is_finalized,
                'updated_at': record.updated_at.strftime('%B %d, %Y %I:%M %p'),
                'at_risk_count': record.get_at_risk_students().count(),
                'dropout_count': record.get_dropout_students().count(),
            })
        
        return JsonResponse({
            'success': True,
            'history': history_data,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def get_change_logs(request, record_id):
    """
    Get detailed change history logs for a specific attendance record.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        attendance_record = get_object_or_404(
            AttendanceRecord,
            id=record_id,
            teacher=teacher
        )
        
        # Get history logs
        logs = AttendanceHistory.objects.filter(
            attendance_record=attendance_record
        ).select_related('modified_by').order_by('-timestamp')
        
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'action': log.action,
                'action_display': log.get_action_display(),
                'modified_by': log.modified_by.full_name if log.modified_by else 'System',
                'date': log.get_formatted_date(),
                'time': log.get_formatted_time(),
                'timestamp': log.timestamp.isoformat(),
                'notes': log.notes,
                'snapshot': log.snapshot_data,
            })
        
        return JsonResponse({
            'success': True,
            'logs': logs_data,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def finalize_attendance(request, record_id):
    """
    Mark attendance record as finalized (prevent further edits).
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        attendance_record = get_object_or_404(
            AttendanceRecord,
            id=record_id,
            teacher=teacher
        )
        
        if attendance_record.is_finalized:
            return JsonResponse({
                'success': False,
                'error': 'Record is already finalized'
            }, status=400)
        
        # Mark as finalized
        attendance_record.is_finalized = True
        attendance_record.save()
        
        # Create history log
        AttendanceHistory.objects.create(
            attendance_record=attendance_record,
            action='finalized',
            modified_by=teacher,
            snapshot_data={
                'total_students': attendance_record.enrollment_male + attendance_record.enrollment_female,
                'avg_attendance': float(attendance_record.avg_attendance_male + attendance_record.avg_attendance_female) / 2,
            },
            notes='Attendance record finalized - no further edits allowed'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Attendance record finalized successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE"])
def delete_attendance_record(request, record_id):
    """
    Delete an attendance record (only if not finalized).
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        attendance_record = get_object_or_404(
            AttendanceRecord,
            id=record_id,
            teacher=teacher
        )
        
        if attendance_record.is_finalized:
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete finalized record'
            }, status=400)
        
        # Store info before deletion
        record_info = f"{attendance_record.section.name} - {attendance_record.get_month_name()} {attendance_record.year}"
        
        # Delete will cascade to StudentAttendance and AttendanceHistory
        attendance_record.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Attendance record for {record_info} deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def export_attendance_data(request, record_id):
    """
    Export attendance data in JSON format for Excel generation on frontend.
    Returns all data needed to generate SF2 Excel file.
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        attendance_record = get_object_or_404(
            AttendanceRecord,
            id=record_id,
            teacher=teacher
        )
        
        # Get all student attendance
        students = attendance_record.student_attendance.select_related('student').order_by('student__gender', 'student__last_name')
        
        students_data = []
        for idx, student_att in enumerate(students, 1):
            students_data.append({
                'number': idx,
                'name': f"{student_att.student.last_name}, {student_att.student.first_name} {student_att.student.middle_name}".strip(),
                'gender': student_att.student.gender,
                'daily_attendance': student_att.daily_attendance,
                'total_absences': student_att.total_absences,
                'total_tardies': student_att.total_tardies,
                'remarks': student_att.remarks,
            })
        
        # Create history log for export
        AttendanceHistory.objects.create(
            attendance_record=attendance_record,
            action='exported',
            modified_by=teacher,
            notes=f'Exported SF2 for {attendance_record.get_month_name()} {attendance_record.year}'
        )
        
        export_data = {
            'record_info': {
                'school_name': attendance_record.school_name,
                'school_id': attendance_record.school_id,
                'section': attendance_record.section.name,
                'grade_level': attendance_record.grade_level,
                'school_year': attendance_record.school_year.name,
                'quarter': attendance_record.get_quarter_display(),
                'month': attendance_record.get_month_name(),
                'year': attendance_record.year,
                'total_days': attendance_record.total_days,
            },
            'summary': {
                'enrollment_male': attendance_record.enrollment_male,
                'enrollment_female': attendance_record.enrollment_female,
                'enrollment_total': attendance_record.enrollment_male + attendance_record.enrollment_female,
                
                'late_enrollees_male': attendance_record.late_enrollees_male,
                'late_enrollees_female': attendance_record.late_enrollees_female,
                'late_enrollees_total': attendance_record.late_enrollees_male + attendance_record.late_enrollees_female,
                
                'registered_male': attendance_record.registered_male,
                'registered_female': attendance_record.registered_female,
                'registered_total': attendance_record.registered_male + attendance_record.registered_female,
                
                'avg_attendance_male': float(attendance_record.avg_attendance_male),
                'avg_attendance_female': float(attendance_record.avg_attendance_female),
                'avg_attendance_total': float(attendance_record.avg_attendance_male + attendance_record.avg_attendance_female),
                
                'attendance_percentage_male': float(attendance_record.attendance_percentage_male),
                'attendance_percentage_female': float(attendance_record.attendance_percentage_female),
                'attendance_percentage_total': (float(attendance_record.attendance_percentage_male) + float(attendance_record.attendance_percentage_female)) / 2,
                
                'dropped_male': attendance_record.dropped_male,
                'dropped_female': attendance_record.dropped_female,
                'dropped_total': attendance_record.dropped_male + attendance_record.dropped_female,
                
                'transferred_out_male': attendance_record.transferred_out_male,
                'transferred_out_female': attendance_record.transferred_out_female,
                'transferred_out_total': attendance_record.transferred_out_male + attendance_record.transferred_out_female,
                
                'transferred_in_male': attendance_record.transferred_in_male,
                'transferred_in_female': attendance_record.transferred_in_female,
                'transferred_in_total': attendance_record.transferred_in_male + attendance_record.transferred_in_female,
            },
            'signatures': {
                'adviser_name': attendance_record.adviser_name,
                'principal_name': attendance_record.principal_name,
            },
            'students': students_data,
        }
        
        return JsonResponse({
            'success': True,
            'data': export_data,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)