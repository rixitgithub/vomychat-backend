from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegistrationForm
from .models import CustomUser, Referral
from .utils import calculate_rewards

@require_http_methods(['GET', 'POST'])
def registration_view(request):
    # Check if a referral code is provided in the URL
    referral_from_url = request.GET.get('referral')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # If referral code is in the URL, use that;
            # otherwise, use the value from the form (if provided)
            if referral_from_url:
                try:
                    referrer = CustomUser.objects.get(referral_code=referral_from_url)
                except CustomUser.DoesNotExist:
                    referrer = None
            else:
                referral_code = form.cleaned_data.get('referral_code')
                if referral_code:
                    try:
                        referrer = CustomUser.objects.get(referral_code=referral_code)
                    except CustomUser.DoesNotExist:
                        referrer = None
                else:
                    referrer = None

            user.referred_by = referrer
            user.set_password(form.cleaned_data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            response = redirect('dashboard')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            return response
    else:
        # Prepare initial data for the form; if referral code exists, pass it in.
        initial_data = {}
        if referral_from_url:
            initial_data['referral_code'] = referral_from_url
        
        form = RegistrationForm(initial=initial_data)
        # If a referral code came in via the URL, remove the field from the form.
        if referral_from_url and 'referral_code' in form.fields:
            form.fields.pop('referral_code')
    
    return render(request, 'registration.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    referrals = Referral.objects.filter(referrer=user)
    reward = calculate_rewards(user)
    
    tier_counts = {
        1: referrals.filter(tier=1).count(),
        2: referrals.filter(tier=2).count(),
        3: referrals.filter(tier=3).count()
    }
    
    return render(request, 'dashboard.html', {
        'user': user,
        'total_referrals': referrals.count(),
        'referral_link': f"{request.scheme}://{request.get_host()}/register?referral={user.referral_code}",
        'referral_tiers': [tier_counts[1], tier_counts[2], tier_counts[3]],
        'reward': reward
    })