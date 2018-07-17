from django import views
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from instagram.forms.auth import *

class SignUpView(views.View):
    def get(self, request):
        form = SignUpForm()
        return render(
            request = request,
            template_name = "sign_up_template.html",
            context = {"form" : form}
        )
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(
                request,
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )

            if user is not None:
                login(request, user)
                return redirect("http://insta-clone-app.herokuapp.com/insta/createprofile/" + str(user.id))
            else:
                return redirect("instagram:signup")

class LoginView(views.View):
    def get(self, request):
        form = LoginForm()
        return render(
            request = request,
            template_name= "login_template.html",
            context = {"form" : form}
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            if(user is not None):
                login(request, user)
                return redirect("instagram:homepage")
            else:
                return redirect("instagram:login")


def Logout_user(request):
    logout(request)
    return redirect("instagram:login")