from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class CandidateThankYou(BaseDetailView):

    def get(self, request, *args, **kwargs):
        try:
            del request.session['candidate_id']
            return render(request, "candidate_thank_you.html")
        except Exception:
            return redirect("/interview_homepage")
