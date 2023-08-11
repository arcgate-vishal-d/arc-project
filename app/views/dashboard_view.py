from django.shortcuts import render
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class Dashboard(LoginRequiredMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        return render(request, "admin_dashboard.html")
