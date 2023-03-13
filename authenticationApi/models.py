
from django.db import models
from django.contrib.auth.models import AbstractUser

Number = [
    (1),
    (2),
    (3)
]

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=500, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    # username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


class ApiAccessToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=300, default="api token", blank=True)
    TPassword = models.CharField(max_length=30, default="api token password", blank=True)
    lastTimeUse = models.DateTimeField(auto_now_add=True, blank=True)
    createToken = models.DateTimeField(auto_now=True, blank=True)
    requestCount = models.PositiveIntegerField(default=0,blank=True)
    random_number = models.CharField(max_length=10, blank=True, unique=True, default="23223434")
    
    def __str__(self):
        return f"({self.user.username}, {self.token}, {self.TPassword})"
    
    
