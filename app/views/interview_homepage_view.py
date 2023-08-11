from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView


class InterviewHomePage(BaseDetailView):
    def get(self, request, *args, **kwargs):
        return render(request, 'interview_homepage.html')
