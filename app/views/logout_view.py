from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.detail import BaseDetailView

from app.utility import return_message


class Logout(BaseDetailView):

    def get(self, request, *args, **kwargs):
        """Signing out and deleting sessions"""
        try:
            del request.session['username']
            logout(request)
            messages.success(request, return_message.MESSAGE['logout'])
            return redirect('/')
        except Exception as e:
            messages.error(request, e)
        return redirect("/")
