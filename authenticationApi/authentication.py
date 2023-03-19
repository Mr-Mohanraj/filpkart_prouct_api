import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from .models import User


class JWTAuthentication(BaseAuthentication):
    """Use to find the user is already register or not. based on the token in cookies inside the browsers"""
    def authenticate(self, request):
        auth = get_authorization_header(request=request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = User.objects.get(pk=id)

            return (user, None)

        raise exceptions.AuthenticationFailed('Unauthenticated')


def create_access_token(id):
    """Create a access token based on the user id or pk"""
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        'iat': datetime.datetime.utcnow()


    }, 'access_secret', algorithm='HS256')


def decode_access_token(token):
    """decode a access token to the encode user id"""
    
    try:
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('Token Unauthenticated')


def create_refresh_token(id):
    """Create a refresh token for  activate the access token based on the user id or pk"""
    
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')


def decode_refresh_token(token):
    """decode a refresh token to the user id"""
    
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('Token Unauthenticated')
