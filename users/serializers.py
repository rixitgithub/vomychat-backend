from rest_framework import serializers
from .models import CustomUser, Referral, Reward
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    referred_by_code = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'referred_by_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_referred_by_code(self, value):
        if value:
            try:
                return CustomUser.objects.get(referral_code=value)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid referral code.")
        return None

    def create(self, validated_data):
        referred_by = validated_data.pop('referred_by_code', None)
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        if referred_by:
            user.referred_by = referred_by
            user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['referral_code'] = str(instance.referral_code)
        return data

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['points', 'unlocked_tiers', 'last_updated']

class ReferralSerializer(serializers.ModelSerializer):
    referred_user = serializers.StringRelatedField()
    
    class Meta:
        model = Referral
        fields = ['tier', 'referred_user', 'created_at']