from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from authenticationApi.authentication import create_refresh_token
from authenticationApi.authentication import decode_refresh_token
from authenticationApi.authentication import JWTAuthentication


from authenticationApi.authentication import create_access_token

from .models import User, Reset
from .serializers import UserSerializer
from django.core.mail import send_mail
import random

import string


class RegisterApiView(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match!')

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginApiView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

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
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RefreshAPIVew(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        access_token = create_access_token(id)

        return Response({
            'token': access_token
        })


class ForgetAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase +
                        string.digits) for _ in range(10))

        Reset.objects.create(
            email=email,
            token=token
        )

        url = 'http://127.0.0.1:8899/api/reset/' + token

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
    def post(self, request):
        data = request.data
        print(">>>>>>", data)
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match')

        user = User.objects.filter(token=data['token']).first()

        if not user:
            raise exceptions.APIException('Invalid link!')

        user.set_password(data['password'])
        user.save()

        return Response({
            'message': 'success'
        })
# def get(self, request):
#     auth = get_authorization_header(request=request).split()

#     if auth and len(auth) == 2:
#         token = auth[1].decode('utf-8')
#         id = decode_access_token(token)

#         user = User.objects.get(pk=id)

#         if user:
#             serializer = UserSerializer(user)

#             return Response(serializer.data)
#     raise exceptions.AuthenticationFailed('Unauthenticated')
