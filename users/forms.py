from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    referral_code = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_referral_code(self):
        code = self.cleaned_data.get('referral_code')
        if code:
            if not CustomUser.objects.filter(referral_code=code).exists():
                raise forms.ValidationError("Invalid referral code")
        return code