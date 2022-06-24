from rest_framework import serializers
from .models import Consultant, User, Visitor
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ConsultantRegisterSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(many=False)
    
    class Meta:
        model = Consultant
        fields = '__all__'
            
    def create(self, validated_date):
        user_data = validated_date.pop("user")
        usr = User.objects.create_user(**user_data)
        usr.is_consultant = True
        usr.save()
        consultant = Consultant.objects.create(user_id=usr.id, **validated_date)
        return consultant


class VisitorRegisterSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(many=False)
    
    class Meta:
        model = Visitor
        fields = '__all__'
            
    def create(self, validated_date):
        user_data = validated_date.pop("user")
        usr = User.objects.create_user(**user_data)
        usr.is_visitor = True
        usr.save()
        visitor = Visitor.objects.create(user_id=usr.id, **validated_date)
        return visitor


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=2000)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6, max_length=200,write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self,obj):
        user = User.objects.get(username=obj['username'])

        return {
            'access':user.tokens()['access'],
            'refresh':user.tokens()['refresh'],
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username,password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials.Try again!')
        if not user.is_active:
            raise AuthenticationFailed('Account not active.Contact admin!')
        
        if not user.is_verified:
            raise AuthenticationFailed('Please Verify your email!')
        
        return {
            'username':user.username,
            'token':user.tokens,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'
