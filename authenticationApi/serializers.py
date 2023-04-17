from rest_framework import serializers
from .models import User,Reset, ApiAccessToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]
        # extra_kwargs = {
        #     "password":{"read_only":True}
        # }

class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reset
        fields = ["id", "email"]

class ResetSerializer(serializers.Serializer):
    password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = ["password", "password_confirm"]
        extra_kwargs = {
            "password":{"read_only":True},
        }

class ApiTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiAccessToken
        fields = ["user", "token", "TPassword", "random_number"]