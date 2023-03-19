from django.urls import path
from .views import (RegisterApiView, LoginApiView, ResetAPIView,
                    UserApiView, RefreshAPIView, ResetAPIView, ForgetAPIView, 
                    ApiAccessTokenCheckApiView, ApiAccessTokenCreateApiView, ApiAccessTokenReadApiView, 
                    ApiAccessTokenDeleteApiView, ApiAccessTokenRefreshApiView)


urlpatterns = [
    path('user/register/', RegisterApiView.as_view()),
    path('user/login/', LoginApiView.as_view()),
    path('user/user/', UserApiView.as_view()),
    path('user/refresh/', RefreshAPIView.as_view()),
    path('user/reset/', ResetAPIView.as_view()),
    path('user/forgot/', ForgetAPIView.as_view()),
    path('developer/<str:username>/create/',
         ApiAccessTokenCreateApiView.as_view()),
    path('developer/<str:username>/refresh/',
         ApiAccessTokenRefreshApiView.as_view()),
    path('developer/<str:username>/view/', ApiAccessTokenReadApiView.as_view()),
    path('developer/<str:username>/delete/',
         ApiAccessTokenDeleteApiView.as_view()),
    path('api/<str:token>@<str:password>/',
         ApiAccessTokenCheckApiView.as_view()),
]