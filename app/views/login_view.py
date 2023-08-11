from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests

from app.forms import LoginForm
from app.utility import return_message,constants


class Login(BaseDetailView):

    def get(self, request, *args, **kwargs):
        """Render login page with django forms"""
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "layout/login.html", context)

    def post(self, request, *args, **kwargs):
        """Authenticate user and check credentials"""
        try:
            username = request.POST.get("username").strip()
            password = request.POST.get("password")
            
            data = {
                "EMail": username,
                "Password": password,
                "LoginType": "Assessment"
            }
            response = requests.post(constants.ARCCRM_LOGIN_URL, json=data)
            if response.status_code == 200 and response.json()['ResourceID']:
                user = User.objects.filter(email=username).first()
                if user:
                    login(request, user)
                    request.session['username'] = username
                    messages.success(request, return_message.MESSAGE['login'])
                    return redirect('/dashboard')
                else:
                    form = LoginForm()
                context = {
                    "form": form
                }
                messages.error(request, return_message.MESSAGE['not_authorized'])
                return render(request, "layout/login.html", context)
            else:
                form = LoginForm()
            context = {
                "form": form
            }
            messages.error(request, return_message.MESSAGE['invalid_credentials'])
            return render(request, "layout/login.html", context)
        except Exception as e:
            messages.error(request,return_message.MESSAGE['error_occur'])
            return redirect("/")
