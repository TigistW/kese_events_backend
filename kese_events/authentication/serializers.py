from rest_framework.views import APIView
from authentication.models import OTP, UserProfile
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class SignUpWithEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user using signup form
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}} 
    def create(self, validated_data): 
        if validate_password(validated_data['password']) == None:
            password = make_password(validated_data['password'])                          
            user = UserProfile.objects.create(
                    email=validated_data['email'],
                    password=password, 
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
        )
        return user
class SignUpWithPhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user using signup form
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}} 
    def create(self, validated_data): 
        if validate_password(validated_data['password']) == None:
            password = make_password(validated_data['password'])                          
            user = UserProfile.objects.create(
                    phone_number=validated_data['phone_number'],
                    password=password, 
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
        )
        return user
   
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        # email = user.email
        token = data["access"]
        
        # Customize the response format
        # Serialize the user profile
        user_profile = UserProfileSerializer(user)
        
        # Customize the response format
        response_data = {
            "statusCode": 200,
            "data": {
                # "email": email,
                "token": token,
                "user_profile": user_profile.data,
            },
        },
        print(response_data[0])
        return response_data[0]
    
    
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('user', 'code', 'created_at')
    def create(self, validated_data):  # Use "validated_data" instead of "data"
        otp_model = OTP.objects.create(
            user=validated_data['user'],
            code=validated_data['code'],
        )
        
        return otp_model