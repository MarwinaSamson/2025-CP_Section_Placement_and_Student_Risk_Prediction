"""
Utility functions for attendance management.
Helper functions for calculations, validations, and data processing.
"""

from datetime import date, timedelta
from calendar import monthrange
from django.db.models import Count, Q


def get_school_days_in_month(year, month):
    """
    Get list of school days (Monday-Friday) for a given month.
    
    Args:
        year (int): Year
        month (int): Month (1-12)
    
    Returns:
        list: List of date objects for school days
    """
    days_in_month = monthrange(year, month)[1]
    school_days = []
    
    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        # 0=Monday, 6=Sunday
        if current_date.weekday() < 5:  # Monday to Friday
            school_days.append(current_date)
    
    return school_days


def get_school_days_count(year, month):
    """Get count of school days in a month"""
    return len(get_school_days_in_month(year, month))


def validate_attendance_code(code):
    """
    Validate attendance code.
    
    Args:
        code (str): Attendance code to validate
    
    Returns:
        tuple: (is_valid, normalized_code, error_message)
    """
    if not code:
        return True, '', None
    
    code_upper = code.strip().upper()
    valid_codes = ['', 'X', 'E', 'T']
    
    if code_upper in valid_codes:
        return True, code_upper, None
    else:
        return False, '', f"Invalid code '{code}'. Use: blank (present), X/E (absent), T (tardy)"


def calculate_attendance_percentage(present_days, total_days):
    """
    Calculate attendance percentage.
    
    Args:
        present_days (int): Number of days present
        total_days (int): Total school days
    
    Returns:
        float: Attendance percentage rounded to 2 decimals
    """
    if total_days == 0:
        return 0.0
    return round((present_days / total_days) * 100, 2)


def parse_daily_attendance(attendance_dict):
    """
    Parse daily attendance dictionary and calculate statistics.
    
    Args:
        attendance_dict (dict): Dictionary with day numbers as keys, codes as values
    
    Returns:
        dict: Statistics with present, absent, tardy counts
    """
    stats = {
        'present': 0,
        'absent': 0,
        'tardy': 0,
        'total_days': len(attendance_dict)
    }
    
    for day, code in attendance_dict.items():
        code_upper = code.upper().strip()
        
        if code_upper in ['X', 'E']:
            stats['absent'] += 1
        elif code_upper == 'T':
            stats['tardy'] += 1
            stats['present'] += 1  # Tardy counts as present
        else:
            stats['present'] += 1
    
    return stats


def get_quarter_for_month(school_year, month_date):
    """
    Determine which quarter a month falls in.
    
    Args:
        school_year (SchoolYear): SchoolYear object
        month_date (date): Date within the month
    
    Returns:
        str: Quarter code ('1', '2', '3', '4') or None
    """
    if not school_year:
        return None
    
    # Get first day of the month
    first_day = month_date.replace(day=1)
    
    # Check each quarter
    quarters = {
        '1': (school_year.q1_start, school_year.q1_end),
        '2': (school_year.q2_start, school_year.q2_end),
        '3': (school_year.q3_start, school_year.q3_end),
        '4': (school_year.q4_start, school_year.q4_end),
    }
    
    for quarter, (start, end) in quarters.items():
        if start <= first_day <= end:
            return quarter
    
    return None


def get_months_in_quarter(school_year, quarter):
    """
    Get list of months (year, month tuples) in a quarter.
    
    Args:
        school_year (SchoolYear): SchoolYear object
        quarter (str): Quarter code ('1', '2', '3', '4')
    
    Returns:
        list: List of (year, month) tuples
    """
    start_date, end_date = school_year.get_quarter_dates(quarter)
    if not start_date or not end_date:
        return []
    
    months = []
    current = start_date.replace(day=1)
    end = end_date.replace(day=1)
    
    while current <= end:
        months.append((current.year, current.month))
        # Move to next month
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)
    
    return months


def detect_status_from_remarks(remarks):
    """
    Detect student status changes from remarks.
    
    Args:
        remarks (str): Remarks text
    
    Returns:
        dict: Dictionary with status flags
    """
    remarks_lower = remarks.lower()
    
    status = {
        'dropped': False,
        'transferred_out': False,
        'transferred_in': False,
        'reason': ''
    }
    
    if 'drop' in remarks_lower:
        status['dropped'] = True
        status['reason'] = 'dropped'
    
    if 'transfer out' in remarks_lower or 'transferred out' in remarks_lower:
        status['transferred_out'] = True
        status['reason'] = 'transferred out'
    
    if 'transfer in' in remarks_lower or 'transferred in' in remarks_lower:
        status['transferred_in'] = True
        status['reason'] = 'transferred in'
    
    return status


def generate_attendance_summary(attendance_record):
    """
    Generate complete attendance summary for a record.
    
    Args:
        attendance_record (AttendanceRecord): Attendance record object
    
    Returns:
        dict: Complete summary with all statistics
    """
    school_days = attendance_record.get_school_days()
    num_school_days = len(school_days)
    
    # Initialize counters
    summary = {
        'school_days': num_school_days,
        'male': {
            'enrolled': 0,
            'present_total': 0,
            'absent_total': 0,
            'tardy_total': 0,
            'avg_attendance': 0,
            'attendance_percentage': 0,
            'dropped': 0,
            'transferred_out': 0,
            'transferred_in': 0,
        },
        'female': {
            'enrolled': 0,
            'present_total': 0,
            'absent_total': 0,
            'tardy_total': 0,
            'avg_attendance': 0,
            'attendance_percentage': 0,
            'dropped': 0,
            'transferred_out': 0,
            'transferred_in': 0,
        },
        'total': {
            'enrolled': 0,
            'present_total': 0,
            'absent_total': 0,
            'tardy_total': 0,
            'avg_attendance': 0,
            'attendance_percentage': 0,
            'dropped': 0,
            'transferred_out': 0,
            'transferred_in': 0,
        }
    }
    
    # Process each student
    students = attendance_record.student_attendance.all()
    
    for student_attendance in students:
        gender = student_attendance.student.gender
        gender_key = 'male' if gender in ['M', 'Male'] else 'female'
        
        # Count enrollment
        summary[gender_key]['enrolled'] += 1
        summary['total']['enrolled'] += 1
        
        # Add attendance counts
        summary[gender_key]['present_total'] += student_attendance.total_present
        summary[gender_key]['absent_total'] += student_attendance.total_absent
        summary[gender_key]['tardy_total'] += student_attendance.total_tardy
        
        summary['total']['present_total'] += student_attendance.total_present
        summary['total']['absent_total'] += student_attendance.total_absent
        summary['total']['tardy_total'] += student_attendance.total_tardy
        
        # Parse status from remarks
        status = detect_status_from_remarks(student_attendance.remarks)
        
        if status['dropped']:
            summary[gender_key]['dropped'] += 1
            summary['total']['dropped'] += 1
        
        if status['transferred_out']:
            summary[gender_key]['transferred_out'] += 1
            summary['total']['transferred_out'] += 1
        
        if status['transferred_in']:
            summary[gender_key]['transferred_in'] += 1
            summary['total']['transferred_in'] += 1
    
    # Calculate averages and percentages
    for key in ['male', 'female', 'total']:
        if num_school_days > 0:
            summary[key]['avg_attendance'] = round(
                summary[key]['present_total'] / num_school_days, 2
            )
        
        if summary[key]['enrolled'] > 0 and num_school_days > 0:
            summary[key]['attendance_percentage'] = round(
                (summary[key]['avg_attendance'] / summary[key]['enrolled']) * 100, 2
            )
    
    return summary


def validate_attendance_record_data(data):
    """
    Validate attendance record data before saving.
    
    Args:
        data (dict): Attendance record data
    
    Returns:
        tuple: (is_valid, errors_dict)
    """
    errors = {}
    
    # Required fields
    required_fields = ['section_id', 'school_year', 'quarter', 'month']
    for field in required_fields:
        if not data.get(field):
            errors[field] = f'{field} is required'
    
    # Validate quarter
    if data.get('quarter') and data['quarter'] not in ['1', '2', '3', '4']:
        errors['quarter'] = 'Invalid quarter. Must be 1, 2, 3, or 4'
    
    # Validate month format
    if data.get('month'):
        try:
            from datetime import datetime
            datetime.strptime(data['month'], '%Y-%m')
        except ValueError:
            errors['month'] = 'Invalid month format. Use YYYY-MM'
    
    # Validate late enrollees
    for field in ['late_enrollees_male', 'late_enrollees_female', 'late_enrollees_total']:
        if data.get(field):
            try:
                value = int(data[field])
                if value < 0:
                    errors[field] = f'{field} cannot be negative'
            except ValueError:
                errors[field] = f'{field} must be a number'
    
    return len(errors) == 0, errors


def get_attendance_statistics_for_section(section, school_year, quarter=None):
    """
    Get comprehensive attendance statistics for a section.
    
    Args:
        section (Section): Section object
        school_year (SchoolYear): School year object
        quarter (str, optional): Quarter filter
    
    Returns:
        dict: Statistics dictionary
    """
    from teacher.models import AttendanceRecord
    
    query = AttendanceRecord.objects.filter(
        section=section,
        school_year=school_year
    )
    
    if quarter:
        query = query.filter(quarter=quarter)
    
    records = query.all()
    
    stats = {
        'total_records': len(records),
        'months_covered': [r.get_month_display() for r in records],
        'quarters_covered': list(set(r.quarter for r in records)),
        'total_school_days': sum(len(r.get_school_days()) for r in records),
        'average_attendance_rate': 0,
    }
    
    if records:
        total_percentage = sum(
            r.calculate_statistics()['avg_attendance_total'] 
            for r in records
        )
        stats['average_attendance_rate'] = round(
            total_percentage / len(records), 2
        ) if len(records) > 0 else 0
    
    return stats