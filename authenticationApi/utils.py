import jwt
import random
from .models import User, ApiAccessToken


def encode_api_access_token(data, key: str = "token create"):
    token = jwt.encode(data, key, algorithm="HS256")
    return token


def decode_api_access_token(token, key: str = "token create"):
    values = jwt.decode(token, key, algorithms=["HS256"])
    return values


def delete_api_access_token(data, key):
    pass


def random_number_generator():
    ran_num = ""
    for _ in range(5):
        ran_num += str(random.randint(0, 9)) + str(_)
    return ran_num


def check_user(token, password):
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
