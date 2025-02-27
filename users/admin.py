# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Referral

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Which columns appear in the list view
    list_display = ('username', 'email', 'referral_code', 'referred_by', 'is_staff', 'is_active')
    
    # If you want to be able to search by these fields
    search_fields = ('username', 'email', 'referral_code')

    # Optional: If you want to show extra fields on the detail page (besides the default)
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('referral_code', 'referred_by')
        }),
    )

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'tier', 'created_at')
    search_fields = ('referrer__email', 'referred_user__email')
    list_filter = ('tier', 'created_at')
