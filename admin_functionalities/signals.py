from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, StudentRequirements,  CustomUser, Teacher
from datetime import date


@receiver(post_save, sender=Student)
def create_requirements(sender, instance, created, **kwargs):
    if created:
        StudentRequirements.objects.create(student=instance)

@receiver(post_save, sender=CustomUser)
def sync_teacher_from_user(sender, instance, created, **kwargs):
    """
    Automatically creates or updates a Teacher record whenever
    a CustomUser is marked as an adviser or subject teacher.
    Skips date_of_birth if not provided in CustomUser.
    """
    if instance.is_adviser or instance.is_subject_teacher:
        # Prepare defaults dynamically, without forcing date_of_birth
        teacher_data = {
            'employee_id': getattr(instance, 'employee_id', f"E-{instance.id}"),
            'first_name': instance.first_name,
            'middle_name': instance.middle_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'phone': 'N/A',
            'position': getattr(instance, 'position', 'Teacher I'),
            'department': getattr(instance, 'department', 'General Department'),
            'address': '',
        }

        # ✅ Add date_of_birth only if it exists in CustomUser
        if hasattr(instance, 'date_of_birth') and instance.date_of_birth:
            teacher_data['date_of_birth'] = instance.date_of_birth

        teacher, _ = Teacher.objects.get_or_create(
            user=instance,
            defaults=teacher_data
        )

        # Update teacher info safely
        teacher.is_adviser = instance.is_adviser
        teacher.is_subject_teacher = instance.is_subject_teacher
        teacher.first_name = instance.first_name
        teacher.middle_name = instance.middle_name
        teacher.last_name = instance.last_name
        teacher.email = instance.email
        teacher.department = getattr(instance, 'department', teacher.department)
        teacher.position = getattr(instance, 'position', teacher.position)

        # ✅ Update date_of_birth only if it's present
        if hasattr(instance, 'date_of_birth') and instance.date_of_birth:
            teacher.date_of_birth = instance.date_of_birth

        teacher.save()
    else:
        # Optional: deactivate teacher if user no longer has teaching roles
        Teacher.objects.filter(user=instance).update(is_active=False)