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
        Main assignment logic:
        1. Get all available sections for the program
        2. Sort sections by current load (ascending)
        3. Assign student to the section with lowest load
        4. Update Section.current_students counter
        5. Create/update SectionPlacement record with 'approved' status

        Returns: (success: bool, section: Section or None, message: str)
        """
        try:
            # Validate student has academic data
            academic_data = StudentAcademic.objects.filter(student=student).first()
            if not academic_data:
                return False, None, f"Student {student.id} has no academic data"

            # Get available sections, sorted by current load
            sections = Section.objects.filter(
                program=program.upper()
            ).annotate(
                student_count=Count(
                    'sectionplacement',
                    filter=Q(sectionplacement__status='approved')
                )
            ).order_by('student_count')  # Lowest load first

            # Check if any sections exist
            if not sections.exists():
                return False, None, f"No sections available for program {program}"

            # Find section with lowest load that isn't at max capacity
            assigned_section = None
            for section in sections:
                if section.student_count < section.max_students:
                    assigned_section = section
                    break

            if not assigned_section:
                return False, None, f"All sections for {program} are at max capacity"

            # Use transaction to ensure atomicity
            with transaction.atomic():
                # Update or create SectionPlacement with 'approved' status
                placement, created = SectionPlacement.objects.update_or_create(
                    student=student,
                    selected_program=program.upper(),
                    defaults={
                        'status': 'approved',
                        'placement_date': timezone.now()
                    }
                )

                # Update Section.current_students counter
                assigned_section.current_students += 1
                assigned_section.save(update_fields=['current_students'])

                # Update Student model's section_placement field (CharField) for quick reference
                student.section_placement = assigned_section.name
                student.save(update_fields=['section_placement'])

            logger.info(
                f"Student {student.id} assigned to {assigned_section.name} "
                f"({program}) - Current load: {assigned_section.current_students}/{assigned_section.max_students}"
            )

            return True, assigned_section, f"Assigned to section: {assigned_section.name}"

        except Exception as e:
            logger.error(f"Error assigning student {student.id} to section: {str(e)}")
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