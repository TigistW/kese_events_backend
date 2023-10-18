"""kese_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from  .views import CustomTokenObtainPairView, SignUpEmailAPIView, CheckEmailView, UserDetailView, VerifyOTP
from rest_framework_simplejwt.views import  TokenRefreshView, TokenVerifyView

app_name = 'authentication'
urlpatterns = [
    path('signup_with_email/', SignUpEmailAPIView.as_view(), name='signup'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('verify_otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('current_user/', UserDetailView.as_view(), name='current_user'),
    
]

