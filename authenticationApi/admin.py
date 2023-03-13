from django.contrib import admin

# Register your models here.
from .models import ApiAccessToken, Reset, UserToken,User

admin.site.register((ApiAccessToken, Reset, UserToken,User))