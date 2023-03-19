from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from authenticationApi.authentication import create_refresh_token
from authenticationApi.authentication import decode_refresh_token
from authenticationApi.authentication import JWTAuthentication
from rest_framework import status

from authenticationApi.authentication import create_access_token

from .models import User, Reset, ApiAccessToken
from .serializers import UserSerializer, LoginSerializer, ForgotSerializer, ResetSerializer, ApiTokenSerializer
from django.core.mail import send_mail
import random
from .utils import encode_api_access_token, decode_api_access_token, random_number_generator

import string
from rest_framework.permissions import IsAuthenticated


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

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginApiView(APIView):
    """Login view for register user for access the api"""
    serializer_class = LoginSerializer

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
    serializer_class = ForgotSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase +
                        string.digits) for _ in range(10))

        self.serializer_class.objects.create(
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
    """Reset view for register user for access the api"""
    permission_classes = [IsAuthenticated]
    serializer_classes = ResetSerializer

    def post(self, request):
        data = request.data
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


class ApiAccessTokenCreateApiView(APIView):
    """Token create for access for the api viva http methods"""
    serializer_class = ApiTokenSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        num = random_number_generator()
        data = {"user": user.pk, "luckyNumber": num}
        token = encode_api_access_token(data, "token create")
        pi = ApiAccessToken.objects.create(
            user=user, token=token, TPassword=num)
        pi.random_number = num
        pi.save()
        return Response({"token": token, "random number": num, "password": num}, status.HTTP_201_CREATED)


class ApiAccessTokenRefreshApiView(APIView):
    """Token refresh for access for the api viva http methods"""
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        num = random_number_generator()
        data = {"user": user.pk, "luckyNumber": num}
        token = encode_api_access_token(data, "token create")
        pi = ApiAccessToken.objects.get(user=user.pk)
        pi.token = token
        pi.random_number = num
        pi.TPassword = num
        pi.save()
        return Response({"result": "Token was reset successfully"}, status.HTTP_205_RESET_CONTENT)


class ApiAccessTokenReadApiView(APIView):
    """Token read for access for the api viva http methods"""

    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        pi = ApiAccessToken.objects.get(user=user.pk)
        print(pi)
        return Response({"token": pi.token, "password": pi.TPassword}, status.HTTP_200_OK)


class ApiAccessTokenCheckApiView(APIView):
    """Token check api for access for the api viva http methods"""

    permission_classes = [IsAuthenticated]

    def get(self, request, token, password):
        de_token = decode_api_access_token(token)
        user = User.objects.get(pk=de_token["user"])
        pi = ApiAccessToken.objects.get(user=user.pk)
        msg = "Done"
        if not (pi.token == token):
            msg = "Token is wrong"

        if not (pi.random_number == password):
            msg = "password is wrong"

        return Response({"results": de_token, "msg": msg}, status.HTTP_200_OK)


class ApiAccessTokenDeleteApiView(APIView):
    """Token delete for access for the api viva http methods"""
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            # request.user.username
            user = get_object_or_404(User, username=username)
            token = ApiAccessToken.objects.get(user=user)
            token.delete()
        except:
            exceptions.APIException('Invalid username')
            return Response({"results": "deleteToken failures"}, status.HTTP_404_NOT_FOUND)
        return Response({"results": "deleteToken Successfully"}, status.HTTP_204_NO_CONTENT)
