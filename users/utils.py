from django.utils import timezone
from django.core.cache import cache
from .models import ReferralCampaign, Reward, Referral

REWARD_RULES = {
    'tier1': {'points': 100, 'badge': 'Bronze'},
    'tier2': {'points': 50, 'badge': 'Silver'},
    'tier3': {'points': 25, 'badge': 'Gold'},
    'milestones': {
        500: 'Exclusive Content',
        1000: 'Premium Membership'
    }
}

def get_campaign_multiplier():
    now = timezone.now()
    active_campaign = ReferralCampaign.objects.filter(
        start_date__lte=now,
        end_date__gte=now,
        is_active=True
    ).first()
    return active_campaign.multiplier if active_campaign else 1.0

def calculate_rewards(user):
    cache_key = f"user_rewards_{user.id}"
    cached = cache.get(cache_key)
    
    if cached:
        return cached
    
    referrals = Referral.objects.filter(referrer_id=user.pk, is_active=True)
    multiplier = get_campaign_multiplier()
    
    total_points = sum(
        REWARD_RULES[f'tier{ref.tier}']['points'] * multiplier
        for ref in referrals
    )
    
    reward, created = Reward.objects.update_or_create(
        user=user,
        defaults={'points': total_points}
    )
    
    # Update unlocked tiers
    unlocked = []
    for ref in referrals:
        badge = REWARD_RULES[f'tier{ref.tier}']['badge']
        if badge not in reward.unlocked_tiers:
            unlocked.append(badge)
    
    # Check milestones
    for milestone, reward_name in REWARD_RULES['milestones'].items():
        if total_points >= milestone and reward_name not in reward.unlocked_tiers:
            unlocked.append(reward_name)
    
    if unlocked:
        reward.unlocked_tiers = list(set(reward.unlocked_tiers + unlocked))
        reward.save()
    
    cache.set(cache_key, reward, timeout=300)
    return reward