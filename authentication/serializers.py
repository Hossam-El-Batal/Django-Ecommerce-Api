from rest_framework import serializers
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib import auth

class register_serializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','isAdmin']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "email already exists"})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": " username already exists"})
        
        if not username.isalnum():
            raise serializers.ValidationError({"username": "username must be alphanumerical"})
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    


class login_serializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=50, min_length=8,write_only=True)
    username = serializers.CharField(max_length=255, min_length=5)
    tokens = serializers.SerializerMethodField()

        
    class Meta:
        model = User
        fields = ['username','password','tokens']
        
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
    
        return {
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()
        }
        
    def get_tokens(self, obj):
        
        return obj['tokens'] 


class logout_serializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh', '')
        if not refresh:
            raise serializers.ValidationError('Refresh token is required.')
        self.token = refresh
        return attrs

    def save(self, **kwargs):
        
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except TokenError:
            raise serializers.ValidationError('Invalid refresh token.')