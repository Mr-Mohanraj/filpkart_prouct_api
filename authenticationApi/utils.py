import jwt
import random
from .models import User, ApiAccessToken
import datetime
from rest_framework import exceptions


def create_access_token(id):
    """Create a access token based on the user id or pk"""
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
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


def encode_api_access_token(data, key: str = "token create"):
    try:
        token = jwt.encode(data, key, algorithm="HS256")

        return token
    except:
        raise exceptions.AuthenticationFailed('Token Unauthenticated')


def decode_api_access_token(token, key: str = "token create"):
    try:
        values = jwt.decode(token, key, algorithms=["HS256"])
        return values
    except:
        raise exceptions.AuthenticationFailed('Token Unauthenticated')


def random_number_generator():
    ran_num = ""
    for _ in range(5):
        ran_num += str(random.randint(0, 9)) + str(_)
    return ran_num


def check_user(token, password):
    """It's return always true to the user for user token is correct"""
    de_token = decode_api_access_token(token)
    try:
        user = User.objects.get(pk=de_token["user"])
        pi = ApiAccessToken.objects.get(user=user.pk)
        msg = "Done"
        if not (pi.token == token):
            msg = "Token is wrong"

        if not (pi.random_number == password):
            msg = "password is wrong"

        return (msg, True)

    except Exception as e:
        return ("Wrong user", False)


def delete_api_access_token(data, key):
    pass
