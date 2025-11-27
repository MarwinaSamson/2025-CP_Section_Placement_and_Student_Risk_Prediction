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
from .models import Program
import logging

logger = logging.getLogger(__name__)


class SectionAssignmentService:
    """
    Handles automatic student-to-section assignment based on:
    - Selected program
    - Academic merit (overall average)
    - Section availability (STRICT capacity enforcement)
    """
    
    @classmethod
    def assign_student_to_section(cls, student, program_name):
        """
        Automatically assign a student to the best available section.
        ENFORCES STRICT CAPACITY: current_students must be < max_students
        
        Args:
            student: Student instance
            program_name: Program name (e.g., 'STE', 'SPFL', 'HETERO')
        
        Returns:
            tuple: (success: bool, section: Section|None, message: str)
        """
        try:
            # Input validation
            if not student:
                error_msg = "Invalid student instance provided"
                logger.error(error_msg)
                return False, None, error_msg
            
            if not program_name:
                error_msg = "No program specified"
                logger.error(error_msg)
                return False, None, error_msg
            
            program_name = str(program_name).strip().upper()
            
            logger.info(
                f"🎯 Attempting to assign student {student.id} "
                f"({student.first_name} {student.last_name}) to program: {program_name}"
            )
            
            with transaction.atomic():
                # Get student's academic record for merit ranking
                try:
                    academic_record = StudentAcademic.objects.get(student=student)
                    overall_average = academic_record.overall_average or 0.0
                    logger.info(f"📊 Student average: {overall_average}")
                except StudentAcademic.DoesNotExist:
                    overall_average = 0.0
                    logger.warning(
                        f"⚠️ No academic record found for student {student.id}, "
                        f"using 0.0 as average"
                    )
                
                # Find the Program instance
                try:
                    program = Program.objects.get(name__iexact=program_name, is_active=True)
                    logger.info(f"✅ Found program: {program.name} (ID: {program.id})")
                except Program.DoesNotExist:
                    msg = f"Program '{program_name}' not found or is inactive"
                    logger.error(f"❌ {msg}")
                    return False, None, msg
                
                # Find available sections for this program
                available_sections = cls._get_available_sections(program)
                
                if not available_sections.exists():
                    msg = (
                        f"❌ NO AVAILABLE SECTIONS for program '{program_name}'.\n\n"
                        f"All sections are at full capacity. Please:\n"
                        f"1. Create a new section for {program_name}, OR\n"
                        f"2. Increase the max_students capacity of existing sections\n\n"
                        f"Current section status:\n"
                    )
                    
                    # Show current section capacities
                    all_sections = Section.objects.filter(
                        program=program,
                        is_active=True
                    ).annotate(
                        enrolled_count=Count(
                            'sectionplacement',
                            filter=Q(sectionplacement__status='approved')
                        )
                    )
                    
                    for section in all_sections:
                        msg += f"  • {section.name}: {section.enrolled_count}/{section.max_students} students"
                        if section.enrolled_count >= section.max_students:
                            msg += " (FULL)"
                        msg += "\n"
                    
                    logger.error(f"❌ {msg}")
                    return False, None, msg
                
                # Select best section based on merit and capacity
                best_section = cls._select_best_section(
                    sections=available_sections,
                    student_average=overall_average
                )
                
                if not best_section:
                    msg = (
                        f"All sections for program '{program_name}' are at capacity. "
                        f"Please create a new section or increase capacity."
                    )
                    logger.error(f"❌ {msg}")
                    return False, None, msg
                
                # CRITICAL: Double-check capacity before assignment
                current_count = SectionPlacement.objects.filter(
                    section=best_section,
                    status='approved'
                ).count()
                
                if current_count >= best_section.max_students:
                    msg = (
                        f"Selected section '{best_section.name}' is now full "
                        f"({current_count}/{best_section.max_students}). "
                        f"Please create a new section."
                    )
                    logger.error(f"❌ {msg}")
                    return False, None, msg
                
                # Update or create SectionPlacement record
                placement, created = SectionPlacement.objects.get_or_create(
                    student=student,
                    defaults={
                        'selected_program': program_name,
                        'section': best_section,
                        'status': 'approved'
                    }
                )
                
                if not created:
                    # Student already has a placement - check if we're moving them
                    old_section = placement.section
                    
                    if old_section and old_section != best_section:
                        # Student is moving sections - update old section count
                        old_section.current_students = SectionPlacement.objects.filter(
                            section=old_section,
                            status='approved'
                        ).count()
                        old_section.save()
                        logger.info(
                            f"🔄 Updated old section {old_section.name} count: "
                            f"{old_section.current_students}/{old_section.max_students}"
                        )
                    
                    # Update placement
                    placement.selected_program = program_name
                    placement.section = best_section
                    placement.status = 'approved'
                    placement.save()
                    
                    logger.info(
                        f"🔄 Updated placement from section {old_section} to {best_section.name}"
                    )
                else:
                    logger.info(f"✨ Created new placement for student")
                
                # Update current_students count in the assigned section
                best_section.current_students = SectionPlacement.objects.filter(
                    section=best_section,
                    status='approved'
                ).count()
                best_section.save()
                
                # Verify capacity wasn't exceeded
                if best_section.current_students > best_section.max_students:
                    logger.error(
                        f"🚨 CAPACITY EXCEEDED! Section {best_section.name} now has "
                        f"{best_section.current_students}/{best_section.max_students} students!"
                    )
                    # This shouldn't happen with proper locking, but log it if it does
                
                logger.info(
                    f"✅ Successfully assigned student {student.id} to section "
                    f"{best_section.id} ({best_section.name}). "
                    f"Section now has {best_section.current_students}/{best_section.max_students} students."
                )
                
                return True, best_section, f"Successfully assigned to {best_section.name}"
                
        except Exception as e:
            error_msg = f"Error assigning student {student.id} to section: {str(e)}"
            logger.error(f"❌ {error_msg}", exc_info=True)
            return False, None, error_msg
    
    @classmethod
    def _get_available_sections(cls, program):
        """
        Get sections for the specified program that have available space.
        STRICT ENFORCEMENT: Only returns sections where current_students < max_students
        
        Args:
            program: Program instance (NOT string)
        
        Returns:
            QuerySet of available Section objects
        """
        try:
            # Get sections with enrollment count
            sections = Section.objects.filter(
                program=program,
                is_active=True
            ).annotate(
                enrolled_count=Count(
                    'sectionplacement',
                    filter=Q(sectionplacement__status='approved')
                )
            )
            
            # CRITICAL: Filter to only sections with available space
            # Use F() expression to compare enrolled_count with max_students
            from django.db.models import F
            available_sections = sections.filter(
                enrolled_count__lt=F('max_students')  # STRICT: enrolled < max
            ).order_by('enrolled_count', 'name')  # Prefer less full sections
            
            count = available_sections.count()
            logger.info(f"📋 Found {count} available sections for program '{program.name}'")
            
            if count > 0:
                logger.info("Available sections:")
                for section in available_sections[:5]:  # Log first 5
                    logger.info(
                        f"  ✅ {section.name}: {section.enrolled_count}/{section.max_students} students "
                        f"({section.max_students - section.enrolled_count} slots available)"
                    )
            else:
                logger.warning(f"⚠️ NO available sections found!")
                # Show all sections and their status
                all_sections = sections
                if all_sections.exists():
                    logger.warning(f"All sections are FULL:")
                    for section in all_sections:
                        status = "FULL" if section.enrolled_count >= section.max_students else "Available"
                        logger.warning(
                            f"  🚫 {section.name}: {section.enrolled_count}/{section.max_students} ({status})"
                        )
            
            return available_sections
            
        except Exception as e:
            logger.error(f"❌ Error getting available sections: {e}", exc_info=True)
            return Section.objects.none()
    
    @classmethod
    def _select_best_section(cls, sections, student_average):
        """
        Select the most appropriate section based on merit and balance.
        
        Strategy:
        1. ONLY considers sections with available space
        2. Prioritizes sections with lower enrollment (balance load)
        3. Returns the section with the most available space
        
        Args:
            sections: QuerySet of available sections (pre-filtered for capacity)
            student_average: Student's overall academic average
        
        Returns:
            Section instance or None
        """
        if not sections.exists():
            logger.warning("⚠️ No sections available for selection")
            return None
        
        # Select the section with the most available space
        # (sections are already ordered by enrolled_count ascending)
        best_section = sections.first()
        
        if best_section:
            logger.info(
                f"🎯 Selected section {best_section.id} ({best_section.name}) "
                f"with {best_section.enrolled_count}/{best_section.max_students} students "
                f"({best_section.max_students - best_section.enrolled_count} slots available)"
            )
        
        return best_section
    
    @classmethod
    def unassign_student_from_section(cls, student):
        """
        Remove a student from their current section.
        Updates section count accordingly.
        
        Args:
            student: Student instance
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            placement = SectionPlacement.objects.filter(student=student).first()
            
            if not placement:
                return True, "Student has no section assignment"
            
            section = placement.section
            section_name = section.name if section else "Unknown"
            
            # Delete the placement
            placement.delete()
            
            # Update section count
            if section:
                section.current_students = SectionPlacement.objects.filter(
                    section=section,
                    status='approved'
                ).count()
                section.save()
                logger.info(
                    f"✅ Removed student {student.id} from {section_name}. "
                    f"Section now has {section.current_students}/{section.max_students} students."
                )
            
            return True, f"Successfully removed from {section_name}"
            
        except Exception as e:
            error_msg = f"Error removing student from section: {str(e)}"
            logger.error(f"❌ {error_msg}", exc_info=True)
            return False, error_msg
    
    @classmethod
    def get_section_statistics(cls, program_name=None):
        """
        Get statistics about section enrollments.
        Shows capacity status for all sections.
        
        Args:
            program_name: Optional program name filter
        
        Returns:
            dict: Statistics about section capacity and enrollment
        """
        try:
            query = Section.objects.filter(is_active=True)
            
            if program_name:
                try:
                    program = Program.objects.get(name__iexact=program_name, is_active=True)
                    query = query.filter(program=program)
                except Program.DoesNotExist:
                    logger.warning(f"Program '{program_name}' not found for statistics")
                    return {
                        'total_sections': 0,
                        'total_capacity': 0,
                        'total_enrolled': 0,
                        'total_available': 0,
                        'sections': []
                    }
            
            sections = query.annotate(
                enrolled_count=Count(
                    'sectionplacement',
                    filter=Q(sectionplacement__status='approved')
                )
            )
            
            total_capacity = sum(s.max_students for s in sections)
            total_enrolled = sum(s.enrolled_count for s in sections)
            
            stats = {
                'total_sections': sections.count(),
                'total_capacity': total_capacity,
                'total_enrolled': total_enrolled,
                'total_available': total_capacity - total_enrolled,
                'sections': []
            }
            
            for section in sections:
                available_slots = section.max_students - section.enrolled_count
                is_full = section.enrolled_count >= section.max_students
                
                stats['sections'].append({
                    'id': section.id,
                    'name': section.name,
                    'program': section.program.name,
                    'enrolled': section.enrolled_count,
                    'max_students': section.max_students,
                    'available_slots': available_slots,
                    'is_full': is_full,
                    'capacity_percentage': round((section.enrolled_count / section.max_students * 100), 1) if section.max_students > 0 else 0
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting section statistics: {e}", exc_info=True)
            return {
                'total_sections': 0,
                'total_capacity': 0,
                'total_enrolled': 0,
                'total_available': 0,
                'sections': [],
                'error': str(e)
            }