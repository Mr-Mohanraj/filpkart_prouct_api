from django.urls import path
from .views import (RegisterApiView, LoginApiView, ResetAPIView,
                    UserApiView, RefreshAPIView, ResetAPIView, ForgetAPIView)

from .api_management import (ApiTokenCheckView, ApiTokenCreateView,
                             ApiTokenDeleteView, ApiTokenReadView, ApiTokenRefreshView)
# api_management these are inherits from the ApiView class from rest framework


urlpatterns = [
    path('user/register/', RegisterApiView.as_view()),
    path('user/login/', LoginApiView.as_view()),
    path('user/user/', UserApiView.as_view()),
    path('user/refresh/', RefreshAPIView.as_view()),
    path('user/reset/<str:token>/', ResetAPIView.as_view()),
    path('user/forget/', ForgetAPIView.as_view()),
    path('developer/<str:username>/create/',
         ApiTokenCreateView.as_view()),
    path('developer/<str:username>/refresh/',
         ApiTokenRefreshView.as_view()),
    path('developer/<str:username>/view/', ApiTokenReadView.as_view()),
    path('developer/<str:username>/delete/',
         ApiTokenDeleteView.as_view()),
    path('api/<str:token>@<str:password>/',
         ApiTokenCheckView.as_view()),
]
