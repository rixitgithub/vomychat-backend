from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Referral

@receiver(post_save, sender=CustomUser)
def create_referral_network(sender, instance, created, **kwargs):
    if created and instance.referred_by:
        try:
            # Tier 1 (Direct)
            Referral.objects.create(
                referrer=instance.referred_by,
                referred_user=instance,
                tier=1
            )
            
            # Tier 2
            if instance.referred_by.referred_by:
                Referral.objects.create(
                    referrer=instance.referred_by.referred_by,
                    referred_user=instance,
                    tier=2
                )
            
            # Tier 3
            if instance.referred_by.referred_by and instance.referred_by.referred_by.referred_by:
                Referral.objects.create(
                    referrer=instance.referred_by.referred_by.referred_by,
                    referred_user=instance,
                    tier=3
                )
        except Exception as e:
            print(f"Error creating referrals: {str(e)}")