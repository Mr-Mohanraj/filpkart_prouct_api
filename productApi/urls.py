from django.urls import path
from productApi import views

urlpatterns = [
    path('', views.home, name="home"),
    path('get/<str:name>/webview/', views.get_data_webview, name='webview'),
    path('api/<str:token>@<str:password>/search',
         views.ProductListApi.as_view()),
]
