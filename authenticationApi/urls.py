from django.urls import path
from .views import (RegisterApiView, LoginApiView, ResetAPIView,
                    UserApiView, RefreshAPIVew, ResetAPIView, ForgetAPIView)


urlpatterns = [
    path('register', RegisterApiView.as_view()),
    path('login', LoginApiView.as_view()),
    path('user', UserApiView.as_view()),
    path('refresh', RefreshAPIVew.as_view()),
    path('reset', ResetAPIView.as_view()),
    path('forgot', ForgetAPIView.as_view())
]
