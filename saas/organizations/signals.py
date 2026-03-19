from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization, Membership


@receiver(post_save, sender=Organization)
def create_owner_membership(sender, instance, created, **kwargs):
    if created:
        Membership.objects.create(
            user=instance.owner,
            organization=instance,
            role="ADMIN"
        )