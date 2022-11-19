from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.loginView.as_view(), name='login'),
    path('home/', views.DetailView.as_view(), name='home'),
]
