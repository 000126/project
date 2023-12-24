from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.SignupView.as_view(), name='registration'),
    path('login/', views.VerifyOtpView.as_view(), name='verify_func'),
    path('login/', views.LoginView.as_view(), name='login_func'),
    path('', views.index),
    path('signup', views.signup),
    path('login', views.handlelogin),
    path('logout', views.handleLogout, name="logout "),


]
