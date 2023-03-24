import datetime

# django package imports
from django.shortcuts import get_object_or_404
from rest_framework import status


# django rest framework imports
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

# apps package import

from authenticationApi.authentication import JWTAuthentication
from .models import User, ApiAccessToken
from .serializers import ApiTokenSerializer

from .utils import encode_api_access_token, decode_api_access_token, random_number_generator


class ApiTokenCreateView(APIView):
    """Token create for access for the api viva http methods"""
    serializer_class = ApiTokenSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        print(user, request.user)
        num = random_number_generator()
        data = {"user": user.pk,
                "luckyNumber": num,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
                'iat': datetime.datetime.utcnow()
                }
        token = encode_api_access_token(data, "token create")
        pi = ApiAccessToken.objects.create(
            user=user, token=token, TPassword=num)
        pi.random_number = num
        pi.save()
        return Response({"token": token, "random number": num, "password": num, "msg": "every 5 days once refresh please me! You faithfully API"}, status.HTTP_201_CREATED)


class ApiTokenRefreshView(APIView):
    """Token refresh for access for the api viva http methods"""
    # permission_classes = [IsAuthenticated]

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


class ApiTokenReadView(APIView):
    """Token read for access for the api viva http methods"""

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        pi = ApiAccessToken.objects.get(user=user.pk)
        print(pi)
        return Response({"token": pi.token, "password": pi.TPassword}, status.HTTP_200_OK)


class ApiTokenCheckView(APIView):
    """Token check api for access for the api viva http methods"""

    # permission_classes = [IsAuthenticated]

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


class ApiTokenDeleteView(APIView):
    """Token delete for access for the api viva http methods"""
    # permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            # request.user.username
            user = get_object_or_404(User, username=username)
            token = ApiAccessToken.objects.get(user=user)
            token.delete()
        except:
            exceptions.APIException('Invalid username')
            return Response({"results": "deleteToken failures, check your username"}, status.HTTP_404_NOT_FOUND)
        return Response({"results": "deleteToken Successfully"}, status.HTTP_204_NO_CONTENT)
