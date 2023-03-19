from django.db import models
from authenticationApi.models import User


class ApiUser(models.Model):
    api_user = models.OneToOneField(
        User, models.CASCADE, related_name='api_user')
    # blank for checking form validation
    api_token = models.TextField(
        max_length=150, default=0, null=True, blank=True)
    token_activation_time = models.DateTimeField(auto_now_add=True)
    token_last_usage = models.DateTimeField(blank=True, null=True)
    token_delete_time = models.DateTimeField(blank=True, null=True)
    api_token_password = models.TextField(
        max_length=10, blank=True, null=True)
