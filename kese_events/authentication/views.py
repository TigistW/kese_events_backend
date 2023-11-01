from django.shortcuts import render, HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import get_user_model
from authentication.models import OTP, UserProfile
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView, csrf_exempt
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from . serializers import  CustomTokenObtainPairSerializer, OTPSerializer, SignUpWithEmailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random
from django.views.decorators.csrf import csrf_exempt

# Import your serializer here

@method_decorator(csrf_exempt, name='dispatch')
class SignUpEmailAPIView(APIView):
    """
    API view for sign up API with OTP generation and email sending.
    """
    permission_classes = []

    def post(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirmPassword')

        print(password, confirm_password)
        if password == confirm_password:
            serializer = SignUpWithEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            
            # Generate a random 4-digit OTP
            otp = str(random.randint(1000, 9999))
            
            otp_instance = OTP.objects.create(user_id=user.pk, code=otp)
            # Send the OTP via email to the user
            subject = 'Your OTP'
            message = f'Your OTP is: {otp}'
            from_email = settings.EMAIL_HOST_USER  # Use your email address here
            recipient_list = [user.email]  # Use the user's email address from the serializer
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            response_data = {
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
            }

            response = {
                'statusCode': status.HTTP_201_CREATED,
                'data': response_data,
            }   
                
        else:
            response = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'data': {'Password fields did not match.'},
            }
            
        return Response(response, status=response['statusCode'])

    
@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
class CheckEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            
            email = request.data.get('email')
            User = get_user_model()
            user_exists = User.objects.filter(email=email).exists()
            message = ""
            
            if (user_exists):
                message = "Email already exists"
            else:
                message = "Email not found"
            
            response_data = {
                "statusCode": 200,
                "message":message
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        email = request.data.get('email', '') # Assuming the user is authenticated
        otp_code = request.data.get('otp', '')
        print(email, otp_code)
        try:
            otp = OTP.objects.filter(user__email=email).latest('created_at')
            print(otp)
        except OTP.DoesNotExist:
            return Response({'message': 'No OTP found for this user'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.code == otp_code:
            # You can implement additional logic here for successful verification
            response_data = {
                'statusCode': status.HTTP_200_OK,
                'message': 'Account successfully verified',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'OTP verification failed',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user  # The authenticated user
        user_data = {
            'id': user.id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'email': user.email,
            'profilePicture':user.profile_picture_url,
            'phoneNumber': str(user.phone_number)
        }
        response_data = {
            "data":user_data,
            "statusCode":200
        }
        return Response(response_data, status=status.HTTP_200_OK)