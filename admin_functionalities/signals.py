from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, StudentRequirements

@receiver(post_save, sender=Student)
def create_requirements(sender, instance, created, **kwargs):
    if created:
        StudentRequirements.objects.create(student=instance)
