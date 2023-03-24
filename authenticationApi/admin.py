from django.contrib import admin
from .models import ApiAccessToken, Reset, UserToken,User

admin.site.register((ApiAccessToken, Reset, UserToken,User))