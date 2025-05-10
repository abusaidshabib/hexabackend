from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, error_messages={
                                     "min_length": "Password must be at least 8 characters long."})  # Add this line to the password field
    password2 = serializers.CharField(write_only=True, min_length=8, error_messages={
        "min_length": "Password must be at least 8 characters long."})

    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number', 'store_name', 'is_active',
                  'is_admin', 'is_shopkeeper', 'profile_photo', 'gender', 'password2', 'password', 'store_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(user=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is not active.")

        attrs['user'] = user
        return attrs
