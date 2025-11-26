from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import StudentRequirementsForm
from teacher.models import (
    Intervention,
    InterventionUpdate,
    
)

from .models import CustomUser, Notification, StudentRequirements, SchoolYear



@admin.register(CustomUser )
class CustomUserAdmin(UserAdmin):
    model = CustomUser 
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'is_read', 'created_at')
    list_filter = ('notification_type', 'program', 'is_read')

class StudentRequirementsInline(admin.StackedInline):
    model = StudentRequirements
    form = StudentRequirementsForm
    can_delete = False
    verbose_name_plural = 'Enrollment Requirements'
    fk_name = 'student'
    
class InterventionUpdateInline(admin.TabularInline):
    """Inline display of updates within intervention admin"""
    model = InterventionUpdate
    extra = 1
    fields = ('date', 'status', 'note', 'created_by')
    readonly_fields = ('created_at',)
    ordering = ['-date']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Auto-populate created_by with current user if they're a teacher"""
        if db_field.name == "created_by" and hasattr(request, 'user'):
            if hasattr(request.user, 'teacher'):
                kwargs["initial"] = request.user.teacher.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = (
        'student_name', 
        'intervention_type',
        'subject_name',
        'created_by', 
        'quarter', 
        'last_status',
        'start_date',
        'review_date',
        'is_active',
        'created_at'
    )
    list_filter = (
        'intervention_type',
        'quarter', 
        'last_status', 
        'is_active',
        'subject',
        'created_at',
        'created_by'
    )
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__lrn',
        'reason',
        'smart_goal',
        'subject__subject_name',
        'subject__subject_code',
    )
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'created_by')
        }),
        ('Intervention Details', {
            'fields': (
                'intervention_type',
                'subject',
                'quarter',
                'start_date',
                'review_date'
            )
        }),
        ('Plan', {
            'fields': ('reason', 'smart_goal')
        }),
        ('Status', {
            'fields': ('last_status', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [InterventionUpdateInline]
    
    def student_name(self, obj):
        return f"{obj.student.last_name}, {obj.student.first_name}"
    student_name.short_description = 'Student'
    student_name.admin_order_field = 'student__last_name'
    
    def subject_name(self, obj):
        return obj.subject.subject_name if obj.subject else '-'
    subject_name.short_description = 'Subject'
    subject_name.admin_order_field = 'subject__subject_name'
    
    def get_queryset(self, request):
        """Optimize queries with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('student', 'created_by', 'subject')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Auto-populate created_by with current user if they're a teacher"""
        if db_field.name == "created_by" and hasattr(request, 'user'):
            if hasattr(request.user, 'teacher'):
                kwargs["initial"] = request.user.teacher.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(InterventionUpdate)
class InterventionUpdateAdmin(admin.ModelAdmin):
    list_display = (
        'intervention_student',
        'intervention_type',
        'date',
        'status',
        'note_preview',
        'created_by',
        'created_at'
    )
    list_filter = (
        'status',
        'date',
        'created_at',
        'intervention__intervention_type'
    )
    search_fields = (
        'intervention__student__first_name',
        'intervention__student__last_name',
        'intervention__subject__subject_name',
        'note'
    )
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Update Information', {
            'fields': ('intervention', 'date', 'status', 'note', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def intervention_student(self, obj):
        return f"{obj.intervention.student.last_name}, {obj.intervention.student.first_name}"
    intervention_student.short_description = 'Student'
    intervention_student.admin_order_field = 'intervention__student__last_name'
    
    def intervention_type(self, obj):
        return obj.intervention.get_intervention_type_display()
    intervention_type.short_description = 'Type'
    
    def note_preview(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_preview.short_description = 'Note Preview'
    
    def get_queryset(self, request):
        """Optimize queries"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'intervention',
            'intervention__student',
            'intervention__subject',
            'created_by'
        )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Auto-populate created_by with current user if they're a teacher"""
        if db_field.name == "created_by" and hasattr(request, 'user'):
            if hasattr(request.user, 'teacher'):
                kwargs["initial"] = request.user.teacher.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Add to admin_functionalities/admin.py
from django.contrib import admin
from .models import SchoolYear

@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active']
    search_fields = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'start_date', 'end_date', 'is_current', 'is_active')
        }),
        ('Quarter 1', {
            'fields': ('q1_start', 'q1_end'),
            'classes': ('collapse',)
        }),
        ('Quarter 2', {
            'fields': ('q2_start', 'q2_end'),
            'classes': ('collapse',)
        }),
        ('Quarter 3', {
            'fields': ('q3_start', 'q3_end'),
            'classes': ('collapse',)
        }),
        ('Quarter 4', {
            'fields': ('q4_start', 'q4_end'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Validate before saving"""
        obj.full_clean()
        super().save_model(request, obj, form, change)



