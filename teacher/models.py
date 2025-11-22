# teacher/models.py
# Add these models to your existing teacher/models.py file

from django.db import models
import json
from django.utils import timezone
from enrollmentprocess.models import Student
from admin_functionalities.models import Teacher, Subject, Section, SchoolYear
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, datetime



class Intervention(models.Model):
    """
    Intervention plans created by advisers for students who need support.
    Moved to teacher app - this is where adviser functionality belongs.
    """
    QUARTER_CHOICES = [
        ('Q1', 'Quarter 1'),
        ('Q2', 'Quarter 2'),
        ('Q3', 'Quarter 3'),
        ('Q4', 'Quarter 4'),
    ]
    
    STATUS_CHOICES = [
        ('', 'Not Started'),
        ('Improved', 'Improved'),
        ('No change', 'No Change'),
        ('Worsened', 'Worsened'),
    ]
    
    INTERVENTION_TYPE_CHOICES = [
        ('Academic', 'Academic - Subject-Specific'),
        ('Behavioral', 'Behavioral - Conduct/Discipline'),
        ('Attendance', 'Attendance - Absences/Tardiness'),
        ('Social', 'Social - Peer Relationships'),
        ('Emotional', 'Emotional - Mental Health'),
        ('General', 'General - Overall Performance'),
    ]
    
    # Core Information
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='interventions',
        verbose_name="Student"
    )
    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='created_interventions',
        verbose_name="Created By (Adviser)"
    )
    
    # Intervention Type & Subject (RECOMMENDED ADDITION)
    intervention_type = models.CharField(
        max_length=20,
        choices=INTERVENTION_TYPE_CHOICES,
        default='General',
        verbose_name="Intervention Type",
        help_text="What area does this intervention address?"
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interventions',
        verbose_name="Subject",
        help_text="Leave blank for general/behavioral interventions."
    )
    
    # Plan Details
    quarter = models.CharField(
        max_length=2, 
        choices=QUARTER_CHOICES, 
        default='Q1',
        verbose_name="Quarter"
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        null=True,
        blank=True
    )
    review_date = models.DateField(
        verbose_name="Review Date",
        null=True,
        blank=True
    )
    reason = models.TextField(
        verbose_name="Reason / Concern",
        help_text="Why is this intervention needed? Be specific."
    )
    smart_goal = models.TextField(
        verbose_name="SMART Goal",
        help_text="Specific, Measurable, Achievable, Relevant, Time-bound goal"
    )
    
    # Current Status
    last_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='',
        blank=True,
        verbose_name="Latest Status"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    # Additional flags
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Uncheck to archive this intervention"
    )
    
    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'quarter']),
            models.Index(fields=['created_by', '-created_at']),
            models.Index(fields=['last_status']),
            models.Index(fields=['subject', 'intervention_type']),  # New index
        ]
    
    def __str__(self):
        subject_info = f" - {self.get_subject_display()}" if self.subject else ""
        return f"{self.student.last_name}, {self.student.first_name} - {self.quarter} ({self.intervention_type}{subject_info})"
    
    def get_latest_update(self):
        """Get the most recent update for this intervention"""
        return self.updates.order_by('-date').first()
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        if self.last_status == 'Improved':
            return 'status-badge-improved'
        elif self.last_status == 'No change':
            return 'status-badge-nochange'
        elif self.last_status == 'Worsened':
            return 'status-badge-worsened'
        return 'status-badge-notstarted'
    
    def is_academic(self):
        """Check if this is an academic intervention"""
        return self.intervention_type == 'Academic' and self.subject is not None


class InterventionUpdate(models.Model):
    """
    Progress updates for interventions.
    Tracks changes in student status over time.
    """
    STATUS_CHOICES = [
        ('Improved', 'Improved'),
        ('No change', 'No Change'),
        ('Worsened', 'Worsened'),
    ]
    
    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name="Intervention"
    )
    
    # Update Details
    date = models.DateField(
        default=timezone.now,
        verbose_name="Update Date"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='No change',
        verbose_name="Status"
    )
    note = models.TextField(
        verbose_name="Notes",
        help_text="Progress notes, actions taken, observations",
        blank=True
    )
    
    # Metadata
    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='intervention_updates',
        verbose_name="Updated By",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    
    class Meta:
        verbose_name = "Intervention Update"
        verbose_name_plural = "Intervention Updates"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['intervention', '-date']),
        ]
    
    def __str__(self):
        return f"{self.intervention.student.last_name} - {self.status} ({self.date})"
    
    def save(self, *args, **kwargs):
        """Update parent intervention's last_status when saving update"""
        super().save(*args, **kwargs)
        # Update the intervention's last_status to match this update
        self.intervention.last_status = self.status
        self.intervention.save(update_fields=['last_status', 'updated_at'])
    
    def get_status_class(self):
        """Return CSS class for update card styling"""
        if self.status == 'Improved':
            return 'update-improved'
        elif self.status == 'No change':
            return 'update-nochange'
        elif self.status == 'Worsened':
            return 'update-worsened'
        return ''
    
# classrecord

class ClassRecord(models.Model):
    """
    Main class record for a teacher's subject and section.
    Represents one teacher's gradebook for one subject in one section.
    """
    QUARTER_CHOICES = [
        ('Q1', 'Quarter 1'),
        ('Q2', 'Quarter 2'),
        ('Q3', 'Quarter 3'),
        ('Q4', 'Quarter 4'),
    ]
    
    SCHOOL_YEAR_CHOICES = [
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027'),
        ('2027-2028', '2027-2028'),
    ]
    
    # Core Information
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='class_records',
        verbose_name="Teacher"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='class_records',
        verbose_name="Subject"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='class_records',
        verbose_name="Section"
    )
    quarter = models.CharField(
        max_length=2,
        choices=QUARTER_CHOICES,
        verbose_name="Quarter"
    )
    school_year = models.CharField(
        max_length=9,
        choices=SCHOOL_YEAR_CHOICES,
        default='2025-2026',
        verbose_name="School Year"
    )
    
    # Grading Criteria Weights (percentages)
    written_works_weight = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Written Works Weight (%)"
    )
    performance_tasks_weight = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Performance Tasks Weight (%)"
    )
    quarterly_assessment_weight = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Quarterly Assessment Weight (%)"
    )
    
    # Highest Possible Scores for each component (up to 10 items each)
    # Written Works HPS
    ww_hps_1 = models.PositiveIntegerField(default=10, verbose_name="WW Item 1 HPS")
    ww_hps_2 = models.PositiveIntegerField(default=10, verbose_name="WW Item 2 HPS")
    ww_hps_3 = models.PositiveIntegerField(default=10, verbose_name="WW Item 3 HPS")
    ww_hps_4 = models.PositiveIntegerField(default=10, verbose_name="WW Item 4 HPS")
    ww_hps_5 = models.PositiveIntegerField(default=10, verbose_name="WW Item 5 HPS")
    ww_hps_6 = models.PositiveIntegerField(default=10, verbose_name="WW Item 6 HPS")
    ww_hps_7 = models.PositiveIntegerField(default=10, verbose_name="WW Item 7 HPS")
    ww_hps_8 = models.PositiveIntegerField(default=10, verbose_name="WW Item 8 HPS")
    ww_hps_9 = models.PositiveIntegerField(default=10, verbose_name="WW Item 9 HPS")
    ww_hps_10 = models.PositiveIntegerField(default=10, verbose_name="WW Item 10 HPS")
    
    # Performance Tasks HPS
    pt_hps_1 = models.PositiveIntegerField(default=10, verbose_name="PT Item 1 HPS")
    pt_hps_2 = models.PositiveIntegerField(default=10, verbose_name="PT Item 2 HPS")
    pt_hps_3 = models.PositiveIntegerField(default=10, verbose_name="PT Item 3 HPS")
    pt_hps_4 = models.PositiveIntegerField(default=10, verbose_name="PT Item 4 HPS")
    pt_hps_5 = models.PositiveIntegerField(default=10, verbose_name="PT Item 5 HPS")
    pt_hps_6 = models.PositiveIntegerField(default=10, verbose_name="PT Item 6 HPS")
    pt_hps_7 = models.PositiveIntegerField(default=10, verbose_name="PT Item 7 HPS")
    pt_hps_8 = models.PositiveIntegerField(default=10, verbose_name="PT Item 8 HPS")
    pt_hps_9 = models.PositiveIntegerField(default=10, verbose_name="PT Item 9 HPS")
    pt_hps_10 = models.PositiveIntegerField(default=10, verbose_name="PT Item 10 HPS")
    
    # Quarterly Assessment HPS
    qa_hps_1 = models.PositiveIntegerField(default=50, verbose_name="QA Item 1 HPS")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Class Record"
        verbose_name_plural = "Class Records"
        ordering = ['-school_year', 'quarter', 'section', 'subject']
        unique_together = ['teacher', 'subject', 'section', 'quarter', 'school_year']
        indexes = [
            models.Index(fields=['teacher', 'section', 'quarter']),
            models.Index(fields=['school_year', 'quarter']),
        ]
    
    def __str__(self):
        return f"{self.subject.subject_name} - {self.section.name} ({self.quarter} {self.school_year})"
    
    def get_ww_hps_total(self):
        """Calculate total HPS for Written Works"""
        return sum([
            self.ww_hps_1, self.ww_hps_2, self.ww_hps_3, self.ww_hps_4, self.ww_hps_5,
            self.ww_hps_6, self.ww_hps_7, self.ww_hps_8, self.ww_hps_9, self.ww_hps_10
        ])
    
    def get_pt_hps_total(self):
        """Calculate total HPS for Performance Tasks"""
        return sum([
            self.pt_hps_1, self.pt_hps_2, self.pt_hps_3, self.pt_hps_4, self.pt_hps_5,
            self.pt_hps_6, self.pt_hps_7, self.pt_hps_8, self.pt_hps_9, self.pt_hps_10
        ])
    
    def get_qa_hps_total(self):
        """Calculate total HPS for Quarterly Assessment"""
        return self.qa_hps_1
    
    def validate_weights(self):
        """Ensure weights sum to 100%"""
        total = self.written_works_weight + self.performance_tasks_weight + self.quarterly_assessment_weight
        return total == 100


class StudentGrade(models.Model):
    """
    Individual student's grades for a specific class record.
    Stores raw scores for all components.
    """
    class_record = models.ForeignKey(
        ClassRecord,
        on_delete=models.CASCADE,
        related_name='student_grades',
        verbose_name="Class Record"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name="Student"
    )
    
    # Written Works Scores (raw scores, not percentages)
    ww_score_1 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 1")
    ww_score_2 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 2")
    ww_score_3 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 3")
    ww_score_4 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 4")
    ww_score_5 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 5")
    ww_score_6 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 6")
    ww_score_7 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 7")
    ww_score_8 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 8")
    ww_score_9 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 9")
    ww_score_10 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="WW Score 10")
    
    # Performance Tasks Scores
    pt_score_1 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 1")
    pt_score_2 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 2")
    pt_score_3 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 3")
    pt_score_4 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 4")
    pt_score_5 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 5")
    pt_score_6 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 6")
    pt_score_7 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 7")
    pt_score_8 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 8")
    pt_score_9 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 9")
    pt_score_10 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="PT Score 10")
    
    # Quarterly Assessment Score
    qa_score_1 = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="QA Score 1")
    
    # Computed Grades (auto-calculated)
    ww_total = models.FloatField(default=0, editable=False, verbose_name="WW Total")
    ww_percentage = models.FloatField(default=0, editable=False, verbose_name="WW Percentage")
    ww_weighted_score = models.FloatField(default=0, editable=False, verbose_name="WW Weighted Score")
    
    pt_total = models.FloatField(default=0, editable=False, verbose_name="PT Total")
    pt_percentage = models.FloatField(default=0, editable=False, verbose_name="PT Percentage")
    pt_weighted_score = models.FloatField(default=0, editable=False, verbose_name="PT Weighted Score")
    
    qa_percentage = models.FloatField(default=0, editable=False, verbose_name="QA Percentage")
    qa_weighted_score = models.FloatField(default=0, editable=False, verbose_name="QA Weighted Score")
    
    initial_grade = models.FloatField(default=0, editable=False, verbose_name="Initial Grade")
    quarterly_grade = models.PositiveIntegerField(default=0, editable=False, verbose_name="Quarterly Grade")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Student Grade"
        verbose_name_plural = "Student Grades"
        ordering = ['student__last_name', 'student__first_name']
        unique_together = ['class_record', 'student']
        indexes = [
            models.Index(fields=['class_record', 'student']),
            models.Index(fields=['quarterly_grade']),
        ]
    
    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} - {self.class_record.subject.subject_name} ({self.class_record.quarter})"
    
    def calculate_grades(self):
        """
        Calculate all grades based on raw scores and class record configuration.
        This method should be called whenever scores are updated.
        """
        cr = self.class_record
        
        # Calculate Written Works
        self.ww_total = sum([
            self.ww_score_1, self.ww_score_2, self.ww_score_3, self.ww_score_4, self.ww_score_5,
            self.ww_score_6, self.ww_score_7, self.ww_score_8, self.ww_score_9, self.ww_score_10
        ])
        ww_hps_total = cr.get_ww_hps_total()
        self.ww_percentage = (self.ww_total / ww_hps_total * 100) if ww_hps_total > 0 else 0
        self.ww_weighted_score = self.ww_percentage * (cr.written_works_weight / 100)
        
        # Calculate Performance Tasks
        self.pt_total = sum([
            self.pt_score_1, self.pt_score_2, self.pt_score_3, self.pt_score_4, self.pt_score_5,
            self.pt_score_6, self.pt_score_7, self.pt_score_8, self.pt_score_9, self.pt_score_10
        ])
        pt_hps_total = cr.get_pt_hps_total()
        self.pt_percentage = (self.pt_total / pt_hps_total * 100) if pt_hps_total > 0 else 0
        self.pt_weighted_score = self.pt_percentage * (cr.performance_tasks_weight / 100)
        
        # Calculate Quarterly Assessment
        qa_hps_total = cr.get_qa_hps_total()
        self.qa_percentage = (self.qa_score_1 / qa_hps_total * 100) if qa_hps_total > 0 else 0
        self.qa_weighted_score = self.qa_percentage * (cr.quarterly_assessment_weight / 100)
        
        # Calculate Initial Grade (sum of weighted scores)
        self.initial_grade = self.ww_weighted_score + self.pt_weighted_score + self.qa_weighted_score
        
        # Calculate Quarterly Grade (transmuted)
        self.quarterly_grade = self.transmute(self.initial_grade)
    
    def save(self, *args, **kwargs):
        """Auto-calculate grades before saving"""
        self.calculate_grades()
        super().save(*args, **kwargs)
    
    @staticmethod
    def transmute(initial_grade):
        """
        DepEd K-12 Grading System Transmutation Table
        Converts initial grade (0-100) to transmuted grade (60-100)
        """
        if initial_grade >= 100: return 100
        if initial_grade >= 98.40: return 99
        if initial_grade >= 96.80: return 98
        if initial_grade >= 95.20: return 97
        if initial_grade >= 93.60: return 96
        if initial_grade >= 92.00: return 95
        if initial_grade >= 90.40: return 94
        if initial_grade >= 88.80: return 93
        if initial_grade >= 87.20: return 92
        if initial_grade >= 85.60: return 91
        if initial_grade >= 84.00: return 90
        if initial_grade >= 82.40: return 89
        if initial_grade >= 80.80: return 88
        if initial_grade >= 79.20: return 87
        if initial_grade >= 77.60: return 86
        if initial_grade >= 76.00: return 85
        if initial_grade >= 74.40: return 84
        if initial_grade >= 72.80: return 83
        if initial_grade >= 71.20: return 82
        if initial_grade >= 69.60: return 81
        if initial_grade >= 68.00: return 80
        if initial_grade >= 66.40: return 79
        if initial_grade >= 64.80: return 78
        if initial_grade >= 63.20: return 77
        if initial_grade >= 61.60: return 76
        if initial_grade >= 60.00: return 75
        if initial_grade >= 56.00: return 74
        if initial_grade >= 52.00: return 73
        if initial_grade >= 48.00: return 72
        if initial_grade >= 44.00: return 71
        if initial_grade >= 40.00: return 70
        if initial_grade >= 36.00: return 69
        if initial_grade >= 32.00: return 68
        if initial_grade >= 28.00: return 67
        if initial_grade >= 24.00: return 66
        if initial_grade >= 20.00: return 65
        if initial_grade >= 16.00: return 64
        if initial_grade >= 12.00: return 63
        if initial_grade >= 8.00: return 62
        if initial_grade >= 4.00: return 61
        if initial_grade >= 0: return 60
        return 0
    
    def get_ww_scores_list(self):
        """Get list of all WW scores"""
        return [
            self.ww_score_1, self.ww_score_2, self.ww_score_3, self.ww_score_4, self.ww_score_5,
            self.ww_score_6, self.ww_score_7, self.ww_score_8, self.ww_score_9, self.ww_score_10
        ]
    
    def get_pt_scores_list(self):
        """Get list of all PT scores"""
        return [
            self.pt_score_1, self.pt_score_2, self.pt_score_3, self.pt_score_4, self.pt_score_5,
            self.pt_score_6, self.pt_score_7, self.pt_score_8, self.pt_score_9, self.pt_score_10
        ]
    
    def is_passing(self):
        """Check if student passed (75 and above)"""
        return self.quarterly_grade >= 75


class GradeSummary(models.Model):
    """
    Summary of a student's grades across all quarters for a subject.
    Used for final grade calculation and report generation.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grade_summaries',
        verbose_name="Student"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grade_summaries',
        verbose_name="Subject"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='grade_summaries',
        verbose_name="Section"
    )
    school_year = models.CharField(
        max_length=9,
        verbose_name="School Year"
    )
    
    # Quarterly Grades
    q1_grade = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="1st Quarter Grade"
    )
    q2_grade = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="2nd Quarter Grade"
    )
    q3_grade = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="3rd Quarter Grade"
    )
    q4_grade = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="4th Quarter Grade"
    )
    
    # Final Grade (average of all quarters, rounded)
    final_grade = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Final Grade"
    )
    
    # Remarks
    remarks = models.CharField(
        max_length=10,
        default='---',
        editable=False,
        verbose_name="Remarks"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Grade Summary"
        verbose_name_plural = "Grade Summaries"
        ordering = ['student__last_name', 'student__first_name', 'subject']
        unique_together = ['student', 'subject', 'section', 'school_year']
        indexes = [
            models.Index(fields=['student', 'school_year']),
            models.Index(fields=['section', 'school_year']),
        ]
    
    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} - {self.subject.subject_name} ({self.school_year})"
    
    def calculate_final_grade(self):
        """Calculate final grade as average of all quarterly grades"""
        grades = [self.q1_grade, self.q2_grade, self.q3_grade, self.q4_grade]
        non_zero_grades = [g for g in grades if g > 0]
        
        if non_zero_grades:
            self.final_grade = round(sum(non_zero_grades) / len(non_zero_grades))
        else:
            self.final_grade = 0
        
        # Determine remarks
        if self.final_grade >= 75:
            self.remarks = 'PASSED'
        elif self.final_grade > 0:
            self.remarks = 'FAILED'
        else:
            self.remarks = '---'
    
    def save(self, *args, **kwargs):
        """Auto-calculate final grade before saving"""
        self.calculate_final_grade()
        super().save(*args, **kwargs)
        
# Masterlist

class AdviserMasterlist(models.Model):
    """
    Main masterlist for an adviser's section.
    Represents the complete list of students under an adviser for a school year.
    An adviser can only have ONE section per school year.
    """
    SCHOOL_YEAR_CHOICES = [
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027'),
        ('2027-2028', '2027-2028'),
    ]
    
    # Core Information
    adviser = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='masterlist_sections',
        limit_choices_to={'is_adviser': True},
        verbose_name="Adviser"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='masterlist_records',
        verbose_name="Section"
    )
    school_year = models.CharField(
        max_length=9,
        choices=SCHOOL_YEAR_CHOICES,
        default='2025-2026',
        verbose_name="School Year"
    )
    
    # Statistics (auto-computed)
    total_students = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Total Students"
    )
    male_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Male Count"
    )
    female_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Female Count"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Set to False to archive this masterlist"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Adviser Masterlist"
        verbose_name_plural = "Adviser Masterlists"
        ordering = ['-school_year', 'section__name']
        unique_together = ['adviser', 'section', 'school_year']
        indexes = [
            models.Index(fields=['adviser', 'school_year']),
            models.Index(fields=['section', 'school_year']),
        ]
    
    def __str__(self):
        return f"{self.adviser.full_name} - {self.section.name} ({self.school_year})"
    
    def update_statistics(self):
        """Update student count statistics"""
        students = self.student_entries.filter(is_active=True)
        self.total_students = students.count()
        self.male_count = students.filter(student__gender='M').count()
        self.female_count = students.filter(student__gender='F').count()
    
    def save(self, *args, **kwargs):
        """Auto-update statistics before saving"""
        super().save(*args, **kwargs)
        self.update_statistics()
        super().save(update_fields=['total_students', 'male_count', 'female_count', 'updated_at'])
    
    def get_active_students(self):
        """Get all active students in this masterlist"""
        return self.student_entries.filter(is_active=True).select_related('student')
    
    def get_students_by_quarter(self, quarter):
        """Get students with specific quarter status"""
        return self.student_entries.filter(
            is_active=True,
            quarter_enrollments__quarter=quarter
        ).select_related('student').distinct()


class MasterlistStudent(models.Model):
    """
    Individual student entry in an adviser's masterlist.
    Links a student to a specific masterlist with additional tracking info.
    """
    QUARTER_CHOICES = [
        ('Q1', 'Quarter 1'),
        ('Q2', 'Quarter 2'),
        ('Q3', 'Quarter 3'),
        ('Q4', 'Quarter 4'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Probation', 'Probation'),
        ('Dropped', 'Dropped'),
        ('Transferred', 'Transferred'),
        ('Graduated', 'Graduated'),
    ]
    
    # Core Relations
    masterlist = models.ForeignKey(
        AdviserMasterlist,
        on_delete=models.CASCADE,
        related_name='student_entries',
        verbose_name="Masterlist"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='masterlist_entries',
        verbose_name="Student"
    )
    
    # Enrollment Info
    enrollment_date = models.DateField(
        default=timezone.now,
        verbose_name="Enrollment Date"
    )
    
    # Student Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active',
        verbose_name="Status"
    )
    
    # Academic Status Flags
    is_honor_student = models.BooleanField(
        default=False,
        verbose_name="Is Honor Student",
        help_text="Student is in the honor roll"
    )
    is_at_risk = models.BooleanField(
        default=False,
        verbose_name="Is At Risk",
        help_text="Student is at risk of failing"
    )
    has_intervention = models.BooleanField(
        default=False,
        verbose_name="Has Active Intervention",
        help_text="Student has active intervention plan"
    )
    
    # Additional Info
    remarks = models.TextField(
        blank=True,
        verbose_name="Remarks",
        help_text="Additional notes about the student"
    )
    
    # Activity tracking
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Student is currently enrolled in this section"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Masterlist Student"
        verbose_name_plural = "Masterlist Students"
        ordering = ['student__last_name', 'student__first_name']
        unique_together = ['masterlist', 'student']
        indexes = [
            models.Index(fields=['masterlist', 'is_active']),
            models.Index(fields=['student', 'status']),
            models.Index(fields=['is_honor_student']),
            models.Index(fields=['is_at_risk']),
        ]
    
    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} - {self.masterlist.section.name}"
    
    def save(self, *args, **kwargs):
        """Update masterlist statistics when saving"""
        super().save(*args, **kwargs)
        # Trigger masterlist statistics update
        self.masterlist.update_statistics()
        self.masterlist.save(update_fields=['total_students', 'male_count', 'female_count', 'updated_at'])
    
    def delete(self, *args, **kwargs):
        """Update masterlist statistics when deleting"""
        masterlist = self.masterlist
        super().delete(*args, **kwargs)
        masterlist.update_statistics()
        masterlist.save(update_fields=['total_students', 'male_count', 'female_count', 'updated_at'])
    
    def get_full_name(self):
        """Get student's full name"""
        return f"{self.student.last_name}, {self.student.first_name} {self.student.middle_name}".strip()
    
    def get_lrn(self):
        """Get student's LRN"""
        return self.student.lrn
    
    def get_age(self):
        """Get student's age"""
        return self.student.age
    
    def get_gender(self):
        """Get student's gender"""
        return self.student.gender
    
    def get_current_quarter_grades(self, quarter):
        """Get student's grades for a specific quarter"""
        # This will reference the StudentGrade model from ClassRecord
        from teacher.models import StudentGrade
        return StudentGrade.objects.filter(
            student=self.student,
            class_record__quarter=quarter,
            class_record__school_year=self.masterlist.school_year
        ).select_related('class_record__subject')


class QuarterEnrollment(models.Model):
    """
    Tracks student enrollment status per quarter.
    Allows flexible tracking of when students join/leave during the year.
    """
    QUARTER_CHOICES = [
        ('Q1', 'Quarter 1'),
        ('Q2', 'Quarter 2'),
        ('Q3', 'Quarter 3'),
        ('Q4', 'Quarter 4'),
    ]
    
    masterlist_student = models.ForeignKey(
        MasterlistStudent,
        on_delete=models.CASCADE,
        related_name='quarter_enrollments',
        verbose_name="Masterlist Student"
    )
    quarter = models.CharField(
        max_length=2,
        choices=QUARTER_CHOICES,
        verbose_name="Quarter"
    )
    is_enrolled = models.BooleanField(
        default=True,
        verbose_name="Is Enrolled",
        help_text="Student is enrolled for this quarter"
    )
    
    # Attendance tracking (optional)
    days_present = models.PositiveIntegerField(
        default=0,
        verbose_name="Days Present"
    )
    days_absent = models.PositiveIntegerField(
        default=0,
        verbose_name="Days Absent"
    )
    days_tardy = models.PositiveIntegerField(
        default=0,
        verbose_name="Days Tardy"
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        verbose_name="Quarter Notes"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Quarter Enrollment"
        verbose_name_plural = "Quarter Enrollments"
        ordering = ['quarter']
        unique_together = ['masterlist_student', 'quarter']
        indexes = [
            models.Index(fields=['masterlist_student', 'quarter']),
            models.Index(fields=['is_enrolled']),
        ]
    
    def __str__(self):
        return f"{self.masterlist_student.student.last_name} - {self.quarter} ({'Enrolled' if self.is_enrolled else 'Not Enrolled'})"
    
    def get_attendance_percentage(self):
        """Calculate attendance percentage"""
        total_days = self.days_present + self.days_absent
        if total_days == 0:
            return 0
        return round((self.days_present / total_days) * 100, 2)
    
    def get_attendance_rate(self):
        """Get attendance rate as string"""
        percentage = self.get_attendance_percentage()
        if percentage >= 95:
            return 'Excellent'
        elif percentage >= 85:
            return 'Good'
        elif percentage >= 75:
            return 'Fair'
        else:
            return 'Poor'


class MasterlistNote(models.Model):
    """
    Notes/logs made by adviser about students in masterlist.
    For tracking important events, observations, or actions taken.
    """
    NOTE_TYPE_CHOICES = [
        ('General', 'General Note'),
        ('Academic', 'Academic Concern'),
        ('Behavioral', 'Behavioral Issue'),
        ('Achievement', 'Achievement/Award'),
        ('Parent Contact', 'Parent Contact'),
        ('Intervention', 'Intervention Action'),
        ('Medical', 'Medical/Health'),
    ]
    
    masterlist_student = models.ForeignKey(
        MasterlistStudent,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Masterlist Student"
    )
    note_type = models.CharField(
        max_length=20,
        choices=NOTE_TYPE_CHOICES,
        default='General',
        verbose_name="Note Type"
    )
    note = models.TextField(
        verbose_name="Note Content"
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Date"
    )
    
    # Who created the note
    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='masterlist_notes',
        verbose_name="Created By"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Masterlist Note"
        verbose_name_plural = "Masterlist Notes"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['masterlist_student', '-date']),
            models.Index(fields=['note_type']),
        ]
    
    def __str__(self):
        return f"{self.note_type} - {self.masterlist_student.student.last_name} ({self.date})"
    
# Attendance

class AttendanceRecord(models.Model):
    """
    Main attendance record for a section.
    Represents the complete attendance data for one section in one month/quarter.
    One record per section per month.
    """
    
    # Core Information
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name="Section"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name="Teacher (Adviser)",
        help_text="Teacher who manages this attendance record"
    )
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name="School Year"
    )
    
    # Period Information
    quarter = models.CharField(
        max_length=2,
        choices=[
            ('Q1', 'Quarter 1'),
            ('Q2', 'Quarter 2'),
            ('Q3', 'Quarter 3'),
            ('Q4', 'Quarter 4'),
        ],
        verbose_name="Quarter"
    )
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Month (1-12)"
    )
    year = models.IntegerField(
        verbose_name="Year"
    )
    
    # School Details (stored for SF2 form)
    school_name = models.CharField(
        max_length=200,
        default="Cagayan de Oro National High School",
        verbose_name="School Name"
    )
    school_id = models.CharField(
        max_length=20,
        default="304144",
        verbose_name="School ID"
    )
    grade_level = models.CharField(
        max_length=20,
        default="Grade 7",
        verbose_name="Grade Level"
    )
    
    # Summary Data (computed from individual student attendance)
    total_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Total School Days in Month",
        help_text="Number of school days (Mon-Fri) in this month"
    )
    
    # Monthly Summary Fields
    # Enrollment
    enrollment_male = models.PositiveIntegerField(default=0, verbose_name="Male Enrollment")
    enrollment_female = models.PositiveIntegerField(default=0, verbose_name="Female Enrollment")
    
    # Late Enrollees (user input)
    late_enrollees_male = models.PositiveIntegerField(default=0, verbose_name="Late Enrollees - Male")
    late_enrollees_female = models.PositiveIntegerField(default=0, verbose_name="Late Enrollees - Female")
    
    # Registered Learners (computed)
    registered_male = models.PositiveIntegerField(default=0, verbose_name="Registered - Male")
    registered_female = models.PositiveIntegerField(default=0, verbose_name="Registered - Female")
    
    # Average Daily Attendance (computed)
    avg_attendance_male = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Avg Attendance - Male")
    avg_attendance_female = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Avg Attendance - Female")
    
    # Percentage of Attendance (computed)
    attendance_percentage_male = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Attendance % - Male")
    attendance_percentage_female = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Attendance % - Female")
    
    # Dropped/Transferred counts (computed from remarks)
    dropped_male = models.PositiveIntegerField(default=0, verbose_name="Dropped - Male")
    dropped_female = models.PositiveIntegerField(default=0, verbose_name="Dropped - Female")
    transferred_out_male = models.PositiveIntegerField(default=0, verbose_name="Transferred Out - Male")
    transferred_out_female = models.PositiveIntegerField(default=0, verbose_name="Transferred Out - Female")
    transferred_in_male = models.PositiveIntegerField(default=0, verbose_name="Transferred In - Male")
    transferred_in_female = models.PositiveIntegerField(default=0, verbose_name="Transferred In - Female")
    
    # Signature Fields
    adviser_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Adviser Name"
    )
    principal_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Principal/School Head Name"
    )
    
    # Status
    is_finalized = models.BooleanField(
        default=False,
        verbose_name="Is Finalized",
        help_text="Mark as finalized to prevent further edits"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        ordering = ['-year', '-month', 'section']
        unique_together = ['section', 'school_year', 'quarter', 'month', 'year']
        indexes = [
            models.Index(fields=['section', 'school_year', 'quarter']),
            models.Index(fields=['teacher', 'year', 'month']),
        ]
    
    def __str__(self):
        month_name = self.get_month_name()
        return f"{self.section.name} - {month_name} {self.year} ({self.quarter})"
    
    def get_month_name(self):
        """Get month name from month number"""
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        return months[self.month] if 1 <= self.month <= 12 else ''
    
    def calculate_school_days(self):
        """
        Calculate number of school days (Mon-Fri) in the month.
        Uses the quarter date ranges from SchoolYear model.
        """
        from datetime import date, timedelta
        
        # Get start and end dates for this month within the quarter
        start_date = date(self.year, self.month, 1)
        
        # Get last day of month
        if self.month == 12:
            end_date = date(self.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(self.year, self.month + 1, 1) - timedelta(days=1)
        
        # Count weekdays (Mon-Fri)
        school_days = 0
        current_date = start_date
        while current_date <= end_date:
            # 0=Monday, 6=Sunday
            if current_date.weekday() < 5:  # Monday to Friday
                school_days += 1
            current_date += timedelta(days=1)
        
        self.total_days = school_days
        return school_days
    
    def update_summary_statistics(self):
        """
        Recalculate all summary statistics from student attendance entries.
        Should be called whenever student attendance is updated.
        """
        students = self.student_attendance.all()
        
        # Count by gender
        male_students = students.filter(student__gender='Male')
        female_students = students.filter(student__gender='Female')
        
        self.enrollment_male = male_students.count()
        self.enrollment_female = female_students.count()
        
        # Registered = Enrollment + Late Enrollees
        self.registered_male = self.enrollment_male + self.late_enrollees_male
        self.registered_female = self.enrollment_female + self.late_enrollees_female
        
        # Calculate average daily attendance (sum of present days / total students)
        total_present_male = sum(s.get_present_days() for s in male_students)
        total_present_female = sum(s.get_present_days() for s in female_students)
        
        if self.total_days > 0:
            self.avg_attendance_male = round(total_present_male / self.total_days, 2) if self.total_days else 0
            self.avg_attendance_female = round(total_present_female / self.total_days, 2) if self.total_days else 0
        
        # Calculate attendance percentage
        # Formula: (Total Daily Attendance / (No. of days × Enrolment)) × 100
        if self.total_days > 0 and self.enrollment_male > 0:
            self.attendance_percentage_male = round(
                (total_present_male / (self.total_days * self.enrollment_male)) * 100, 2
            )
        else:
            self.attendance_percentage_male = 0
            
        if self.total_days > 0 and self.enrollment_female > 0:
            self.attendance_percentage_female = round(
                (total_present_female / (self.total_days * self.enrollment_female)) * 100, 2
            )
        else:
            self.attendance_percentage_female = 0
        
        # Count dropped/transferred from remarks
        self.dropped_male = male_students.filter(remarks__icontains='drop').count()
        self.dropped_female = female_students.filter(remarks__icontains='drop').count()
        
        self.transferred_out_male = male_students.filter(remarks__icontains='transfer out').count()
        self.transferred_out_female = female_students.filter(remarks__icontains='transfer out').count()
        
        self.transferred_in_male = male_students.filter(remarks__icontains='transfer in').count()
        self.transferred_in_female = female_students.filter(remarks__icontains='transfer in').count()
    
    def get_at_risk_students(self):
        """
        Get students who are at risk of dropout (5+ absences).
        Returns queryset of StudentAttendance with warning flags.
        """
        return self.student_attendance.filter(
            total_absences__gte=5,
            is_dropout=False
        ).select_related('student')
    
    def get_dropout_students(self):
        """Get students marked as potential dropouts (7+ absences)"""
        return self.student_attendance.filter(
            total_absences__gte=7
        ).select_related('student')


class StudentAttendance(models.Model):
    """
    Individual student's attendance for a specific month.
    Stores daily attendance codes and computes totals.
    """
    
    # Relations
    attendance_record = models.ForeignKey(
        AttendanceRecord,
        on_delete=models.CASCADE,
        related_name='student_attendance',
        verbose_name="Attendance Record"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='monthly_attendance',
        verbose_name="Student"
    )
    
    # Daily Attendance (stored as JSON array for flexibility)
    # Format: ["", "X", "", "T", "E", ...] for each school day
    # "" = Present, "X" or "E" = Absent, "T" = Tardy
    daily_attendance = models.JSONField(
        default=list,
        verbose_name="Daily Attendance Codes",
        help_text="Array of attendance codes for each school day"
    )
    
    # Computed Totals
    total_absences = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Absences"
    )
    total_tardies = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Tardies"
    )
    total_present = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Present Days"
    )
    
    # Remarks (for dropped/transferred students)
    remarks = models.TextField(
        blank=True,
        verbose_name="Remarks",
        help_text="Note reasons for absences, dropout, transfer, etc."
    )
    
    # Warning Flags
    is_at_risk = models.BooleanField(
        default=False,
        verbose_name="At Risk of Dropout",
        help_text="Student has 5-6 absences"
    )
    is_dropout = models.BooleanField(
        default=False,
        verbose_name="Subject to Dropout",
        help_text="Student has 7+ absences"
    )
    has_valid_excuse = models.BooleanField(
        default=False,
        verbose_name="Has Valid Excuse",
        help_text="Teacher marked absences as excused"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Student Attendance"
        verbose_name_plural = "Student Attendance Records"
        ordering = ['student__last_name', 'student__first_name']
        unique_together = ['attendance_record', 'student']
        indexes = [
            models.Index(fields=['attendance_record', 'student']),
            models.Index(fields=['total_absences']),
            models.Index(fields=['is_at_risk']),
            models.Index(fields=['is_dropout']),
        ]
    
    def __str__(self):
        return f"{self.student.last_name}, {self.student.first_name} - {self.attendance_record}"
    
    def calculate_totals(self):
        """
        Calculate totals from daily_attendance array.
        Updates total_absences, total_tardies, total_present.
        """
        if not self.daily_attendance:
            self.daily_attendance = []
        
        self.total_absences = 0
        self.total_tardies = 0
        self.total_present = 0
        
        for code in self.daily_attendance:
            code_upper = str(code).strip().upper()
            if code_upper in ['X', 'E']:
                self.total_absences += 1
            elif code_upper == 'T':
                self.total_tardies += 1
                self.total_present += 1  # Tardy counts as present but late
            elif code_upper == '':
                self.total_present += 1
        
        # Update warning flags
        self.is_at_risk = (5 <= self.total_absences < 7) and not self.has_valid_excuse
        self.is_dropout = (self.total_absences >= 7) and not self.has_valid_excuse
    
    def save(self, *args, **kwargs):
        """Auto-calculate totals before saving"""
        self.calculate_totals()
        super().save(*args, **kwargs)
        
        # Update parent record statistics
        self.attendance_record.update_summary_statistics()
        self.attendance_record.save()
    
    def get_present_days(self):
        """Get total present days (including tardy)"""
        return self.total_present
    
    def get_attendance_percentage(self):
        """Calculate attendance percentage for this student"""
        total_days = self.attendance_record.total_days
        if total_days == 0:
            return 0
        return round((self.total_present / total_days) * 100, 2)
    
    def get_warning_message(self):
        """Get appropriate warning message based on absence count"""
        if self.has_valid_excuse:
            return "Valid excuse provided"
        elif self.is_dropout:
            return f"⚠️ DROPOUT RISK: {self.total_absences} absences (7+ threshold)"
        elif self.is_at_risk:
            remaining = 7 - self.total_absences
            return f"⚠️ WARNING: {self.total_absences} absences ({remaining} more until dropout threshold)"
        return ""
    
    def get_status_class(self):
        """Get CSS class for status badge"""
        if self.is_dropout:
            return "bg-red-100 text-red-800 border-red-300"
        elif self.is_at_risk:
            return "bg-yellow-100 text-yellow-800 border-yellow-300"
        elif self.total_absences > 0:
            return "bg-blue-100 text-blue-800 border-blue-300"
        return "bg-green-100 text-green-800 border-green-300"


class AttendanceHistory(models.Model):
    """
    History/audit log for attendance record changes.
    Tracks when attendance was saved, who modified it, and key metrics.
    """
    
    attendance_record = models.ForeignKey(
        AttendanceRecord,
        on_delete=models.CASCADE,
        related_name='history_logs',
        verbose_name="Attendance Record"
    )
    
    # Action Info
    action = models.CharField(
        max_length=50,
        choices=[
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('finalized', 'Finalized'),
            ('exported', 'Exported to Excel'),
        ],
        verbose_name="Action"
    )
    
    # Snapshot of key metrics at time of save
    snapshot_data = models.JSONField(
        default=dict,
        verbose_name="Data Snapshot",
        help_text="JSON snapshot of key metrics"
    )
    
    # Who and When
    modified_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_history',
        verbose_name="Modified By"
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name="Timestamp"
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    class Meta:
        verbose_name = "Attendance History"
        verbose_name_plural = "Attendance Histories"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['attendance_record', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.attendance_record} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
    
    def get_formatted_date(self):
        """Get formatted date for display"""
        return self.timestamp.strftime('%B %d, %Y')
    
    def get_formatted_time(self):
        """Get formatted time for display"""
        return self.timestamp.strftime('%I:%M %p')
    
# cLASSRECORD WARNING
class EarlyWarningAlert(models.Model):
    """
    Tracks early warning alerts for students at risk of failing.
    """
    WARNING_TYPE_CHOICES = [
        ('at_risk', 'At Risk (70-74, Quarter In Progress)'),
        ('failed', 'Failed (<75, Quarter Complete)'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('dismissed', 'Dismissed'),
        ('intervention_created', 'Intervention Created'),
        ('resolved', 'Resolved'),
    ]
    
    student_grade = models.ForeignKey(StudentGrade, on_delete=models.CASCADE, related_name='early_warnings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='early_warnings')
    class_record = models.ForeignKey(ClassRecord, on_delete=models.CASCADE, related_name='early_warnings')
    
    warning_type = models.CharField(max_length=10, choices=WARNING_TYPE_CHOICES)
    current_grade = models.PositiveIntegerField()
    initial_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0) 
    required_performance = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    intervention = models.ForeignKey('Intervention', on_delete=models.SET_NULL, null=True, blank=True)
    
    flagged_at = models.DateTimeField(auto_now_add=True)
    viewed_by_teacher = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Early Warning Alert"
        ordering = ['-flagged_at']
    
    def __str__(self):
        return f"{self.student.last_name} - {self.warning_type} - Grade {self.current_grade}"