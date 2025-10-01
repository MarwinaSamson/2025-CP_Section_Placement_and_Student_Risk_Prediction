from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notification, StudentRequirements
from .forms import StudentRequirementsForm

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