# teacher/management/commands/update_interventions.py
# Management command to bulk update all intervention plans

from django.core.management.base import BaseCommand
from django.utils import timezone
from teacher.models import InterventionPlan, StudentGrade, StudentAttendance
from admin_functionalities.models import Section, SchoolYear


class Command(BaseCommand):
    help = 'Update all active intervention plans with latest data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quarter',
            type=str,
            help='Quarter to update (Q1, Q2, Q3, Q4)',
        )
        parser.add_argument(
            '--section',
            type=int,
            help='Section ID to update',
        )

    def handle(self, *args, **options):
        quarter = options.get('quarter')
        section_id = options.get('section')
        
        queryset = InterventionPlan.objects.filter(is_active=True)
        
        if quarter:
            queryset = queryset.filter(quarter=quarter)
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        
        updated_count = 0
        for intervention in queryset:
            # Update attendance data
            attendance_records = StudentAttendance.objects.filter(
                student=intervention.student,
                attendance_record__section=intervention.section,
                attendance_record__quarter=intervention.quarter
            )
            intervention.total_absences = sum(rec.total_absences for rec in attendance_records)
            
            # Update grade data
            student_grades = StudentGrade.objects.filter(
                student=intervention.student,
                class_record__section=intervention.section,
                class_record__subject=intervention.subject,
                class_record__quarter=intervention.quarter
            ).first()
            
            if student_grades:
                intervention.current_grade = student_grades.quarterly_grade
                
                ww_scores = student_grades.get_ww_scores_list()
                pt_scores = student_grades.get_pt_scores_list()
                
                intervention.missing_written_works = sum(1 for score in ww_scores if score == 0)
                intervention.missing_performance_tasks = sum(1 for score in pt_scores if score == 0)
                
                if student_grades.class_record.qa_hps_1 > 0 and student_grades.qa_score_1 == 0:
                    intervention.missed_quarterly_assessment = True
            
            # Recalculate risk level and tier
            intervention.update_risk_assessment()
            intervention.save()
            
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Updated intervention for {intervention.student.last_name}, {intervention.student.first_name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} intervention plans')
        )


# teacher/management/commands/generate_intervention_report.py
# Generate intervention reports for advisers

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Q
from teacher.models import InterventionPlan, InterventionAction
from admin_functionalities.models import Section, Teacher
import csv
import os


class Command(BaseCommand):
    help = 'Generate intervention report for sections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quarter',
            type=str,
            default='Q1',
            help='Quarter to report on',
        )
        parser.add_argument(
            '--output',
            type=str,
            default='intervention_report.csv',
            help='Output CSV file path',
        )

    def handle(self, *args, **options):
        quarter = options['quarter']
        output_file = options['output']
        
        # Get all sections with interventions
        sections = Section.objects.filter(
            intervention_plans__quarter=quarter,
            intervention_plans__is_active=True
        ).distinct()
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Section', 'Adviser', 'Total Students', 
                'Critical Risk', 'At Risk', 'Tier 1', 'Tier 2', 'Tier 3',
                'Total Interventions', 'Resolved'
            ])
            
            for section in sections:
                interventions = InterventionPlan.objects.filter(
                    section=section,
                    quarter=quarter,
                    is_active=True
                )
                
                total = interventions.count()
                critical = interventions.filter(risk_level='Critical').count()
                at_risk = interventions.filter(risk_level='At Risk').count()
                tier1 = interventions.filter(current_tier='Tier 1').count()
                tier2 = interventions.filter(current_tier='Tier 2').count()
                tier3 = interventions.filter(current_tier='Tier 3').count()
                resolved = interventions.filter(is_resolved=True).count()
                
                writer.writerow([
                    section.name,
                    section.adviser.full_name if section.adviser else 'N/A',
                    section.current_students,
                    critical,
                    at_risk,
                    tier1,
                    tier2,
                    tier3,
                    total,
                    resolved
                ])
        
        self.stdout.write(
            self.style.SUCCESS(f'Report generated: {output_file}')
        )


# teacher/utils/intervention_utils.py
# Utility functions for intervention system

from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta


def get_section_intervention_summary(section, quarter, school_year):
    """
    Get comprehensive intervention summary for a section.
    Returns dict with statistics and student lists.
    """
    from teacher.models import InterventionPlan
    
    interventions = InterventionPlan.objects.filter(
        section=section,
        quarter=quarter,
        school_year=school_year,
        is_active=True
    ).select_related('student', 'subject', 'created_by')
    
    summary = {
        'total_interventions': interventions.count(),
        'critical_count': interventions.filter(risk_level='Critical').count(),
        'at_risk_count': interventions.filter(risk_level='At Risk').count(),
        'tier_1_count': interventions.filter(current_tier='Tier 1').count(),
        'tier_2_count': interventions.filter(current_tier='Tier 2').count(),
        'tier_3_count': interventions.filter(current_tier='Tier 3').count(),
        'resolved_count': interventions.filter(is_resolved=True).count(),
        'avg_absences': interventions.aggregate(Avg('total_absences'))['total_absences__avg'] or 0,
        'avg_grade': interventions.aggregate(Avg('current_grade'))['current_grade__avg'] or 0,
        'students_by_risk': {
            'Critical': list(interventions.filter(risk_level='Critical').values_list('student__id', flat=True)),
            'At Risk': list(interventions.filter(risk_level='At Risk').values_list('student__id', flat=True)),
        }
    }
    
    return summary


def check_student_needs_intervention(student, section, subject, quarter, school_year):
    """
    Check if a student needs an intervention plan.
    Returns (needs_intervention: bool, risk_level: str, reasons: list)
    """
    from teacher.models import StudentGrade, StudentAttendance
    
    reasons = []
    
    # Check attendance
    attendance_records = StudentAttendance.objects.filter(
        student=student,
        attendance_record__section=section,
        attendance_record__quarter=quarter
    )
    total_absences = sum(rec.total_absences for rec in attendance_records)
    
    # Check grades
    student_grades = StudentGrade.objects.filter(
        student=student,
        class_record__section=section,
        class_record__subject=subject,
        class_record__quarter=quarter
    ).first()
    
    missing_ww = 0
    missing_pt = 0
    current_grade = 0
    missed_qa = False
    
    if student_grades:
        current_grade = student_grades.quarterly_grade
        ww_scores = student_grades.get_ww_scores_list()
        pt_scores = student_grades.get_pt_scores_list()
        missing_ww = sum(1 for score in ww_scores if score == 0)
        missing_pt = sum(1 for score in pt_scores if score == 0)
        
        if student_grades.class_record.qa_hps_1 > 0 and student_grades.qa_score_1 == 0:
            missed_qa = True
    
    # Determine risk level
    risk_level = 'On Track'
    needs_intervention = False
    
    # Critical conditions
    if total_absences >= 7:
        risk_level = 'Critical'
        needs_intervention = True
        reasons.append(f'Excessive absences: {total_absences}')
    
    if missed_qa:
        risk_level = 'Critical'
        needs_intervention = True
        reasons.append('Missed quarterly assessment')
    
    if missing_ww >= 4:
        risk_level = 'Critical'
        needs_intervention = True
        reasons.append(f'Too many missing written works: {missing_ww}')
    
    if missing_pt >= 3:
        risk_level = 'Critical'
        needs_intervention = True
        reasons.append(f'Too many missing performance tasks: {missing_pt}')
    
    # At Risk conditions (if not already critical)
    if risk_level != 'Critical':
        if total_absences >= 5:
            risk_level = 'At Risk'
            needs_intervention = True
            reasons.append(f'High absences: {total_absences}')
        
        if missing_ww >= 2:
            risk_level = 'At Risk'
            needs_intervention = True
            reasons.append(f'Missing written works: {missing_ww}')
        
        if missing_pt >= 2:
            risk_level = 'At Risk'
            needs_intervention = True
            reasons.append(f'Missing performance tasks: {missing_pt}')
        
        if missing_ww >= 1 and missing_pt >= 1:
            risk_level = 'At Risk'
            needs_intervention = True
            reasons.append('Missing both written works and performance tasks')
    
    if current_grade < 75 and current_grade > 0:
        if risk_level == 'On Track':
            risk_level = 'At Risk'
        needs_intervention = True
        reasons.append(f'Failing grade: {current_grade}')
    
    return needs_intervention, risk_level, reasons


def auto_create_intervention_if_needed(student, section, subject, quarter, school_year, teacher):
    """
    Automatically create an intervention plan if student meets criteria.
    Returns (created: bool, intervention: InterventionPlan or None)
    """
    from teacher.models import InterventionPlan
    
    # Check if intervention already exists
    existing = InterventionPlan.objects.filter(
        student=student,
        section=section,
        subject=subject,
        quarter=quarter,
        school_year=school_year,
        is_active=True
    ).first()
    
    if existing:
        # Update existing intervention
        existing.update_risk_assessment()
        return False, existing
    
    # Check if intervention is needed
    needs_intervention, risk_level, reasons = check_student_needs_intervention(
        student, section, subject, quarter, school_year
    )
    
    if not needs_intervention:
        return False, None
    
    # Get current data
    from teacher.models import StudentGrade, StudentAttendance
    
    attendance_records = StudentAttendance.objects.filter(
        student=student,
        attendance_record__section=section,
        attendance_record__quarter=quarter
    )
    total_absences = sum(rec.total_absences for rec in attendance_records)
    
    student_grades = StudentGrade.objects.filter(
        student=student,
        class_record__section=section,
        class_record__subject=subject,
        class_record__quarter=quarter
    ).first()
    
    missing_ww = 0
    missing_pt = 0
    current_grade = 0
    missed_qa = False
    
    if student_grades:
        current_grade = student_grades.quarterly_grade
        ww_scores = student_grades.get_ww_scores_list()
        pt_scores = student_grades.get_pt_scores_list()
        missing_ww = sum(1 for score in ww_scores if score == 0)
        missing_pt = sum(1 for score in pt_scores if score == 0)
        
        if student_grades.class_record.qa_hps_1 > 0 and student_grades.qa_score_1 == 0:
            missed_qa = True
    
    # Create intervention
    intervention = InterventionPlan.objects.create(
        student=student,
        section=section,
        subject=subject,
        created_by=teacher,
        quarter=quarter,
        school_year=school_year,
        risk_level=risk_level,
        current_grade=current_grade,
        total_absences=total_absences,
        missing_written_works=missing_ww,
        missing_performance_tasks=missing_pt,
        missed_quarterly_assessment=missed_qa
    )
    
    intervention.update_risk_assessment()
    
    return True, intervention


def bulk_update_section_interventions(section, quarter, school_year, teacher):
    """
    Update or create interventions for all students in a section.
    Returns dict with counts of created/updated interventions.
    """
    from enrollmentprocess.models import Student
    from admin_functionalities.models import Subject, SectionSubjectAssignment
    from django.db.models import Q
    
    students = Student.objects.filter(
        masterlist_entries__masterlist__section=section,
        masterlist_entries__is_active=True
    ).distinct()
    
    # Get subjects for this section through SectionSubjectAssignment
    # Note: SectionSubjectAssignment.subject is a CharField, not FK
    taught_subject_codes = SectionSubjectAssignment.objects.filter(
        section=section
    ).values_list('subject', flat=True).distinct()
    
    subjects = Subject.objects.filter(
        Q(subject_code__in=taught_subject_codes) | 
        Q(subject_name__in=taught_subject_codes),
        is_active=True
    ).distinct()
    
    created_count = 0
    updated_count = 0
    
    for student in students:
        for subject in subjects:
            created, intervention = auto_create_intervention_if_needed(
                student, section, subject, quarter, school_year, teacher
            )
            
            if created:
                created_count += 1
            elif intervention:
                updated_count += 1
    
    return {
        'created': created_count,
        'updated': updated_count,
        'total_students': students.count(),
        'subjects_checked': subjects.count()
    }