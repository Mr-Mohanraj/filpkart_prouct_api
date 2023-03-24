import string
import random

# django package imports
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import login, logout

# django rest framework imports
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated

# apps package import
from authenticationApi.utils import (
    create_access_token, decode_access_token, create_refresh_token, decode_refresh_token)
from authenticationApi.authentication import JWTAuthentication
from .models import User, Reset, ApiAccessToken
from .serializers import UserSerializer, LoginSerializer, ForgotSerializer, ResetSerializer, ApiTokenSerializer


class RegisterApiView(APIView):
    """Register view for register user for access the api"""
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        try:
            if data['password'] != data['password_confirm']:
                raise exceptions.APIException('Password do not match!')
        except:
            print("please enter your password")
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = data["email"]
        user = User.objects.get(email=email)
        login(request, user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginApiView(APIView):
    """Login view for register user for access the api"""
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            return Response("please enter your email and password or create a account <a href=''>register</a>")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refresh_token',
                            value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }

        return response


class UserApiView(APIView):
    """User view for register user for access the api"""

    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshAPIView(APIView):
    """Refresh view for register user for access the api. just use the api path user/refresh/ """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # serializer_class =

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })


class ForgetAPIView(APIView):
    """Forgot view for register user for access the api"""
    # serializer_class = ForgotSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase +
                        string.digits) for _ in range(10))

        Reset.objects.create(
            email=email,
            token=token
        )
        url = request.build_absolute_uri('/')
        url = f'{url}user/reset/{token}'

        send_mail(
            subject='Reset your password',
            message='Click <a href="%s">here</a> to ree your password' % url,
            from_email='from_mail@gmail.com',
            recipient_list=[email]
        )

        return Response({
            'message': 'success'
        })


class ResetAPIView(APIView):
    """Reset view for register user for access the api"""
    # permission_classes = [IsAuthenticated]
    serializer_classes = ResetSerializer

    def post(self, request):
        data = request.data
        try:
            if data['password'] != data['password_confirm']:
                raise exceptions.APIException('Passwords do not match')
        except KeyError:
            return Response("Please enter the password and password_confirm")

        reset = Reset.objects.filter(token=data['token']).first()
        try:
            user = get_object_or_404(User, email=reset.email)
        except Http404:
            return Response("Enter correct email id same as a register email")

        if not user:
            raise exceptions.APIException('Invalid link!')

        user.set_password(data['password'])
        user.save()
        logout(request)

        return Response({
            'message': 'success, Please Login again'
        })
