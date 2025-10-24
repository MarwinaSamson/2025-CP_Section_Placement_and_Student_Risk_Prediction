"""
Section Auto-Assignment Service
Handles fair distribution of students across sections within their chosen program.
Location: admin_functionalities/services.py
"""

from django.db import transaction, models
from enrollmentprocess.models import Student, SectionPlacement, StudentAcademic
from admin_functionalities.models import Section
from django.utils import timezone
from django.db.models import Count, Q
import logging

logger = logging.getLogger(__name__)


class SectionAssignmentService:
    """
    Handles automatic, fair distribution of students to sections.
    Uses a load-balancing algorithm with academic merit consideration.
    """

    @staticmethod
    def get_available_sections(program):
        """
        Fetch all sections for a program that aren't at max capacity.
        Sorted by current student count (ascending) for fair distribution.
        """
        sections = Section.objects.filter(
            program=program.upper()
        ).annotate(
            student_count=Count('sectionplacement', filter=Q(sectionplacement__status='approved'))
        ).filter(
            student_count__lt=models.F('max_students')  # Not at capacity
        ).order_by('student_count')  # Sections with fewer students first

        return sections

    @staticmethod
    def get_student_academic_ranking(student):
        """
        Get student's overall average from StudentAcademic model.
        Returns 0.0 if no academic data (fallback for incomplete records).
        """
        try:
            academic = StudentAcademic.objects.get(student=student)
            return academic.overall_average or 0.0
        except StudentAcademic.DoesNotExist:
            logger.warning(f"No academic data for student {student.id}. Using default 0.0")
            return 0.0

    @staticmethod
    def assign_student_to_section(student, program):
        """
        Main assignment logic with capacity enforcement:
        1. Find an available section (not full)
        2. Use transaction & row locking to prevent race conditions
        3. Create/update SectionPlacement with proper FK to Section
        4. Update counters safely and log results
        """
        try:
            academic_data = StudentAcademic.objects.filter(student=student).first()
            if not academic_data:
                return False, None, f"Student {student.id} has no academic data"

            # Fetch candidate sections for this program
            sections = (
                Section.objects.filter(program=program.upper())
                .annotate(
                    student_count=Count(
                        'sectionplacement',
                        filter=Q(sectionplacement__status='approved')
                    )
                )
                .order_by('student_count', 'name')
            )

            if not sections.exists():
                return False, None, f"No sections available for program {program}"

            # Choose first section under capacity
            assigned_section = None
            for sec in sections:
                if sec.student_count < sec.max_students:
                    assigned_section = sec
                    break

            if not assigned_section:
                return False, None, f"All sections for {program} are already full"

            # Atomic block ensures no two assignments overfill
            with transaction.atomic():
                # Lock the chosen section row for update
                sec = Section.objects.select_for_update().get(pk=assigned_section.pk)

                # Double-check capacity after locking
                if sec.current_students >= sec.max_students:
                    return False, None, f"Section '{sec.name}' is already at capacity"

                # Create or update SectionPlacement
                placement, created = SectionPlacement.objects.update_or_create(
                    student=student,
                    selected_program=program.upper(),
                    defaults={
                        'status': 'approved',
                        'section': sec,             # ✅ set actual section FK
                        'placement_date': timezone.now(),
                    },
                )

                # Increment student counter safely
                sec.current_students = models.F('current_students') + 1
                sec.save(update_fields=['current_students'])
                sec.refresh_from_db(fields=['current_students'])

                # Update student reference field for quick lookup
                student.section_placement = sec.name
                student.save(update_fields=['section_placement'])

            logger.info(
                f"✅ Student {student.id} assigned to {sec.name} ({program}) "
                f"Load: {sec.current_students}/{sec.max_students}"
            )

            return True, sec, f"Assigned to section: {sec.name}"

        except Exception as e:
            logger.error(f"❌ Error assigning student {student.id} to section: {str(e)}")
            return False, None, f"Assignment error: {str(e)}"


    @staticmethod
    def bulk_assign_students_by_ranking(program):
        """
        Advanced: Assign multiple pending students to a program in ranked order.
        
        Algorithm:
        1. Get all students with pending placement for this program
        2. Sort by overall_average (descending - highest first)
        3. Distribute using round-robin with load balancing
        
        Use case: Admin runs bulk assignment after multiple enrollments.
        """
        try:
            # Get pending placements for this program, sorted by academic ranking
            pending = SectionPlacement.objects.filter(
                selected_program=program.upper(),
                status='pending'
            ).select_related('student', 'student__studentacademic').order_by(
                '-student__studentacademic__overall_average'  # Highest average first
            )

            if not pending.exists():
                return {
                    'success': True,
                    'assigned': 0,
                    'failed': 0,
                    'message': f'No pending placements for {program}'
                }

            assigned = 0
            failed = 0
            failed_students = []

            for placement in pending:
                success, section, msg = SectionAssignmentService.assign_student_to_section(
                    placement.student,
                    program
                )
                if success:
                    assigned += 1
                else:
                    failed += 1
                    failed_students.append({
                        'student_id': placement.student.id,
                        'name': f"{placement.student.first_name} {placement.student.last_name}",
                        'reason': msg
                    })

            return {
                'success': True,
                'assigned': assigned,
                'failed': failed,
                'failed_students': failed_students,
                'message': f'Assigned {assigned} students to {program} sections'
            }

        except Exception as e:
            logger.error(f"Bulk assignment error for {program}: {str(e)}")
            return {
                'success': False,
                'assigned': 0,
                'failed': 0,
                'message': f'Bulk assignment error: {str(e)}'
            }

    @staticmethod
    def get_section_status(program):
        """
        Get current status of all sections in a program.
        Useful for dashboard/monitoring.
        """
        try:
            sections = Section.objects.filter(
                program=program.upper()
            ).annotate(
                current_load=Count(
                    'sectionplacement',
                    filter=Q(sectionplacement__status='approved')
                )
            ).values(
                'id', 'name', 'adviser__full_name', 'max_students', 'current_load'
            ).order_by('name')

            return {
                'success': True,
                'program': program.upper(),
                'sections': list(sections)
            }

        except Exception as e:
            logger.error(f"Error fetching section status: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }