from rest_framework.views import APIView
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from . models import *
from django.contrib import messages
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework import status
import random
from django.contrib.auth import authenticate
from utilities import send_email_sendgrid
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    return render(request, 'index.html')


class SignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if serializer.is_valid(raise_exception=True):
            if password != confirm_password:
                return Response(
                    {
                        'message': "Password and confirm password does't match ",
                        "data": None,
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                )
            user = serializer.save()
            # generate& send otp
            otp = str(random.randint(100000, 999999))
            user.email_otp = otp
            user.status = "signup successful"
            send_email_sendgrid(user.email, "Your otp is {}".format(otp))
            return Response(
                {
                    'message': "otp has been sent on your email",
                    "data": None,
                    "status": status.HTTP_200_OK

                }
            )


class VerifyOtpView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')

        if not otp or not email:
            return Response(
                {
                    'message': "email otp is missing",
                    "data": None,
                    "status": status.HTTP_404_NOT_FOUND


                }
            )
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "message": "the given email does't exist",
                    "data": None,
                    "status": status.HTTP_404_NOT_FOUND
                }
            )
        else:
            if user.email_otp != otp:
                return Response(
                    {
                        'message': "incorrect otp",
                        "data": None,
                        "status": status.HTTP_400_BAD_REQUEST
                    }
                )

            user.status = "otp_verified"
            user.email_otp = ""
            user.save()
            return Response(
                {
                    'message': "your email is verified please login",
                    "data": None,
                    "status": status.HTTP_200_OK
                }
            )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.status == "otp_verified":
                    user.status = "login_done"
                    user.save()
                return Response({
                    "message": "login is successful",
                    "data": {"id": user.id, "email": user.email},
                    "status": status.HTTP_200_OK
                })


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(username) > 10 or len(username) < 10:
            messages.info(request, "Phone Number Must be 10 Digits")
            return redirect('/signup')

        if pass1 != pass2:
            messages.info(request, "Password is not Matching")
            return redirect('/signup')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "Phone Number is Taken")
                return redirect('/signup')

        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email is Taken")
                return redirect('/signup')

        except Exception as identifier:
            pass

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "User is Created Please Login")
        return redirect('/login')

    return render(request, "signup.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successful")
            return redirect('/home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')

    return render(request, "login.html")


def handleLogout(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')
