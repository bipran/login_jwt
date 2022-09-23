from unicodedata import name
from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.RegisterUser.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('home/',views.HomeView.as_view(),name='home')
]
