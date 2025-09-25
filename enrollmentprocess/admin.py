# from django.contrib import admin
# from .models import Student, Family, StudentNonAcademic, StudentAcademic, SectionPlacement

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['lrn', 'last_name', 'first_name', 'age', 'gender', 'section_placement', 'is_sped', 'is_working_student']  # Removed 'created_at'; added existing flags for quick views
#     list_filter = ['gender', 'is_sped', 'is_working_student', 'section_placement', 'enrolling_as']  # All existing fields
#     search_fields = ['lrn', 'last_name', 'first_name']  # Removed 'email'—add to model if needed
#     readonly_fields = ['lrn', 'date_of_birth']  # Existing key fields
#     fieldsets = (
#         ('Basic Info', {'fields': ('lrn', 'last_name', 'first_name', 'middle_name', 'age', 'gender')}),
#         ('Enrollment Details', {'fields': ('enrolling_as', 'is_sped', 'sped_details', 'is_working_student', 'working_details', 'section_placement')}),
#         ('Background', {'fields': ('address', 'date_of_birth', 'place_of_birth', 'religion', 'dialect_spoken', 'ethnic_tribe', 'last_school_attended', 'previous_grade_section', 'last_school_year')}),
#         ('Relationships', {'fields': ('family_data',)}),
#         ('Media', {'fields': ('photo',)}),
#     )

# @admin.register(Family)
# class FamilyAdmin(admin.ModelAdmin):
#     list_display = ['father_family_name', 'mother_first_name', 'guardian_first_name', 'father_contact_number']  # Existing fields
#     list_filter = ['father_occupation', 'mother_occupation']  # Existing
#     search_fields = ['father_family_name', 'mother_first_name', 'guardian_family_name', 'mother_email', 'father_email', 'guardian_email']  # Emails exist here
#     fieldsets = (
#         ("Father's Info", {'fields': ('father_family_name', 'father_first_name', 'father_middle_name', 'father_age', 'father_occupation', 'father_dob', 'father_contact_number', 'father_email')}),
#         ("Mother's Info", {'fields': ('mother_family_name', 'mother_first_name', 'mother_middle_name', 'mother_age', 'mother_occupation', 'mother_dob', 'mother_contact_number', 'mother_email')}),
#         ("Guardian's Info", {'fields': ('guardian_family_name', 'guardian_first_name', 'guardian_middle_name', 'guardian_age', 'guardian_occupation', 'guardian_dob', 'guardian_address', 'guardian_relationship', 'guardian_contact_number', 'guardian_email')}),
#         ('Media', {'fields': ('parent_photo',)}),
#     )

# @admin.register(StudentNonAcademic)
# class StudentNonAcademicAdmin(admin.ModelAdmin):
#     list_display = ['student', 'study_hours', 'confidence_level', 'quiet_place']  # Existing
#     list_filter = ['study_hours', 'parent_help', 'quiet_place', 'confidence_level', 'house_type']  # Existing
#     search_fields = ['student__last_name', 'student__first_name', 'hobbies']  # Via related Student
#     raw_id_fields = ['student']  # For performance

# @admin.register(StudentAcademic)
# class StudentAcademicAdmin(admin.ModelAdmin):
#     list_display = ['student', 'overall_average', 'dost_exam_result', 'is_pwd', 'is_working_student']  # Existing
#     list_filter = ['dost_exam_result', 'is_pwd', 'is_working_student']  # Removed 'overall_average' from filter (it's numeric, but filter works)
#     search_fields = ['student__lrn', 'student__last_name']  # Via Student
#     readonly_fields = ['lrn', 'overall_average']  # Existing computed/locked
#     fieldsets = (
#         ('Basic', {'fields': ('lrn', 'dost_exam_result', 'report_card')}),
#         ('Grades', {'fields': ('mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao', 'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh', 'overall_average')}),
#         ('Details', {'fields': ('is_working_student', 'work_type', 'is_pwd', 'disability_type', 'agreed_to_terms')}),
#     )

# @admin.register(SectionPlacement)
# class SectionPlacementAdmin(admin.ModelAdmin):
#     list_display = ['student', 'selected_program', 'placement_date']  # Existing
#     list_filter = ['selected_program', 'placement_date']  # Existing
#     search_fields = ['student__lrn', 'student__last_name']  # Via Student
#     readonly_fields = ['placement_date']  # Existing
#     raw_id_fields = ['student']

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Family, Student, StudentNonAcademic, StudentAcademic, SectionPlacement

# Inline classes for related models (to edit them from the parent Student page)
class StudentNonAcademicInline(admin.StackedInline):
    model = StudentNonAcademic
    can_delete = True
    verbose_name_plural = "Non-Academic Data"

class StudentAcademicInline(admin.StackedInline):
    model = StudentAcademic
    can_delete = True
    verbose_name_plural = "Academic Data"

class SectionPlacementInline(admin.TabularInline):
    model = SectionPlacement
    extra = 1  # Allows adding one new placement by default
    verbose_name_plural = "Section Placements"

# REMOVED: FamilyInline (causing the error) - See explanation above

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('lrn', 'full_name', 'gender', 'age', 'is_sped', 'is_working_student', 'section_placement', 'family_link')
    list_filter = ('gender', 'is_sped', 'is_working_student', 'enrolling_as')
    search_fields = ('lrn', 'first_name', 'last_name', 'middle_name', 'address')
    inlines = [StudentNonAcademicInline, StudentAcademicInline, SectionPlacementInline]  # REMOVED FamilyInline
    readonly_fields = ('photo',)  # Make photo read-only after upload if needed

    fieldsets = (
        ('Basic Information', {
            'fields': ('lrn', 'enrolling_as', 'is_sped', 'sped_details', 'is_working_student', 'working_details', 'photo')
        }),
        ('Personal Details', {
            'fields': ('last_name', 'first_name', 'middle_name', 'address', 'age', 'gender', 'date_of_birth', 'place_of_birth')
        }),
        ('Background', {
            'fields': ('religion', 'dialect_spoken', 'ethnic_tribe', 'last_school_attended', 'previous_grade_section', 'last_school_year')
        }),
        ('Placement', {
            'fields': ('family_data', 'section_placement'),
            'classes': ('collapse',)  # Collapsible fieldset
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name or ''} {obj.last_name}".strip()
    full_name.short_description = 'Full Name'

    def family_link(self, obj):
        """
        Custom method to display a link to the related Family in the list view.
        If no family, shows 'No Family Assigned'.
        """
        if obj.family_data:
            url = reverse('admin:enrollmentprocess_family_change', args=[obj.family_data.pk])
            return format_html('<a href="{}">View Family</a>', url)
        return 'No Family Assigned'
    family_link.short_description = 'Family Data'

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('father_full_name', 'mother_full_name', 'guardian_full_name', 'father_contact_number')
    list_filter = ('father_occupation', 'mother_occupation', 'guardian_occupation')
    search_fields = ('father_first_name', 'father_family_name', 'mother_first_name', 'mother_family_name', 'guardian_first_name', 'guardian_family_name')
    readonly_fields = ('parent_photo',)  # Make photo read-only after upload if needed

    # Optional: Add inline for Students here (reverse: edit Students from Family page)
    # This works because Students FK to Family
    class StudentInline(admin.TabularInline):
        model = Student
        extra = 1
        verbose_name_plural = "Related Students"

    inlines = [StudentInline]  # Allows editing related students from the Family page

    fieldsets = (
        ('Father\'s Information', {
            'fields': ('father_family_name', 'father_first_name', 'father_middle_name', 'father_age', 'father_occupation', 'father_dob', 'father_contact_number', 'father_email')
        }),
        ('Mother\'s Information', {
            'fields': ('mother_family_name', 'mother_first_name', 'mother_middle_name', 'mother_age', 'mother_occupation', 'mother_dob', 'mother_contact_number', 'mother_email')
        }),
        ('Guardian\'s Information (if applicable)', {
            'fields': ('guardian_family_name', 'guardian_first_name', 'guardian_middle_name', 'guardian_age', 'guardian_occupation', 'guardian_dob', 'guardian_address', 'guardian_relationship', 'guardian_contact_number', 'guardian_email'),
            'classes': ('collapse',)  # Collapsible if not always needed
        }),
        ('Documents', {
            'fields': ('parent_photo',),
            'classes': ('collapse',)
        }),
    )

    def father_full_name(self, obj):
        return f"{obj.father_first_name} {obj.father_middle_name or ''} {obj.father_family_name}".strip()
    father_full_name.short_description = "Father's Full Name"

    def mother_full_name(self, obj):
        return f"{obj.mother_first_name} {obj.mother_middle_name or ''} {obj.mother_family_name}".strip()
    mother_full_name.short_description = "Mother's Full Name"

    def guardian_full_name(self, obj):
        return f"{obj.guardian_first_name} {obj.guardian_middle_name or ''} {obj.guardian_family_name}".strip()
    guardian_full_name.short_description = "Guardian's Full Name"

@admin.register(StudentNonAcademic)
class StudentNonAcademicAdmin(admin.ModelAdmin):
    list_display = ('student', 'study_hours', 'live_with', 'confidence_level')
    list_filter = ('study_with', 'parent_help', 'house_type', 'transport_mode')
    search_fields = ('student__first_name', 'student__last_name', 'hobbies', 'personality_traits')
    raw_id_fields = ('student',)  # Use ID lookup for large student lists

    fieldsets = (
        ('Study Habits', {
            'fields': ('study_hours', 'study_place', 'study_with')
        }),
        ('Family Support', {
            'fields': ('live_with', 'parent_help', 'highest_education', 'marital_status')
        }),
        ('Living Environment', {
            'fields': ('house_type', 'quiet_place', 'study_area')
        }),
        ('Transportation', {
            'fields': ('transport_mode', 'travel_time')
        }),
        ('Learning Resources', {
            'fields': ('access_resources', 'computer_use')
        }),
        ('Personality & Interests', {
            'fields': ('hobbies', 'personality_traits', 'confidence_level')
        }),
    )

@admin.register(StudentAcademic)
class StudentAcademicAdmin(admin.ModelAdmin):
    list_display = ('student', 'overall_average', 'dost_exam_result', 'is_working_student', 'is_pwd')
    list_filter = ('is_working_student', 'is_pwd', 'dost_exam_result')
    search_fields = ('student__first_name', 'student__last_name', 'lrn')
    raw_id_fields = ('student',)  # Use ID lookup for large student lists
    readonly_fields = ('report_card',)  # Make file read-only after upload if needed

    fieldsets = (
        ('Basic Academic Info', {
            'fields': ('lrn', 'dost_exam_result', 'report_card')
        }),
        ('Grade 6 Subjects', {
            'fields': ('mathematics', 'araling_panlipunan', 'english', 'edukasyon_pagpapakatao', 'science', 'edukasyon_pangkabuhayan', 'filipino', 'mapeh', 'overall_average')
        }),
        ('Additional Details', {
            'fields': ('is_working_student', 'work_type', 'is_pwd', 'disability_type', 'agreed_to_terms')
        }),
    )

@admin.register(SectionPlacement)
class SectionPlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'selected_program', 'placement_date')
    list_filter = ('selected_program', 'placement_date')
    search_fields = ('student__first_name', 'student__last_name', 'student__lrn')
    raw_id_fields = ('student',)  # Use ID lookup for large student lists
    readonly_fields = ('placement_date',)  # Auto-generated, so read-only

    fieldsets = (
        ('Placement Details', {
            'fields': ('student', 'selected_program', 'placement_date')
        }),
    )
