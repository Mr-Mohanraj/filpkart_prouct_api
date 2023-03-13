import jwt
import random

def encode_api_access_token(data, key:str="token create"):
    token = jwt.encode(data, key, algorithm="HS256")
    return token

def decode_api_access_token(token, key:str="token create"):
    values = jwt.decode(token,key, algorithms=["HS256"])
    return values

def delete_api_access_token(data, key):
    pass

def random_number_generator():
    ran_num = ""
    for _ in range(5):
        ran_num += str(random.randint(0, 9)) + str(_)
    return ran_num

# def encrypt_data(data:str, number:int=10) -> str:
#     data_en = ""
#     for i in data:
#         data_en += i+1+i