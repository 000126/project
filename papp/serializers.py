from django.contrib.auth.models import User
from rest_framework import serializers
from . models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"})

    class Meta:
        model = CustomUser
        fields = ["email", "password", "confirm_password"]
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(validated_data['email'], validated_data['password'])


class OTPverifySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email_otp"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ["email", '-password']
