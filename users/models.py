import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email

class Referral(models.Model):
    TIER_CHOICES = [(1, 'Direct'), (2, 'Level 2'), (3, 'Level 3')]
    
    referrer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referrals_made')
    referred_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='referral_received')
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['referrer', 'tier']),
            models.Index(fields=['created_at']),
        ]

class Reward(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='rewards')
    points = models.PositiveIntegerField(default=0)
    unlocked_tiers = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)

class ReferralCampaign(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    multiplier = models.FloatField(default=1.0)
    is_active = models.BooleanField(default=True)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()