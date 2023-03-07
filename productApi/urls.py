from django.urls import path
from productApi import views

urlpatterns = [
    path('', views.home, name="home"),
    path('get/<str:name>/', views.get_data, name='dataget'),
    path('get/<str:name>/webview/', views.get_data_webview, name='webview'),
]
