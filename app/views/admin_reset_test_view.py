import os
import datetime
from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from app import models
from app.utility import return_message


@method_decorator(never_cache, name="dispatch")
class ResetTest(LoginRequiredMixin,BaseDetailView):
    def get(self, request, *args, **kwargs):
        today=date.today()
        candidate_status = models.CandidateDetails.objects.filter(modified__contains=today).order_by('-modified')
        context = {
            "candidates": candidate_status,
        }
        return render(request, 'admin_reset_test.html', context)


    def post(self, request, *args, **kwargs):
        candidate_id = request.POST.get('SelectedCandidate')
        logout(request)
        candidate_obj = models.CandidateDetails.objects.filter(id=candidate_id).first()
        request.session["candidate_id"] = candidate_obj.id
        return redirect('/exam')
