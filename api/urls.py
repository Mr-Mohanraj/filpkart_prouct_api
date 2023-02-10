from django.urls import path 
from api import views

urlpatterns = [
    path('',views.home, name="home"),
    path('get/<str:productname>/', views.data_get, name='dataget'),
]
