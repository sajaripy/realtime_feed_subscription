from rest_framework import serializers
from .models import UserSubscription, User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email','password', 'password2', 'role']

    def validate(self, data):
        if data['password'] != data['password2']:
             raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        return data

    def create(self, data):
        password = data.pop('password2', '')
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    # username = serializers.
    # email = serializers.EmailField(max_length = 200)
    class Meta:
        model = User
        fields = ['username','password']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    gc_name = serializers.CharField(max_length = 100)
    class Meta:
        model = UserSubscription
        fields = ['gc_name']
