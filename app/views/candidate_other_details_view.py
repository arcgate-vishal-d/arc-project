from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateOtherDetails
from app.utility import queries

class CandidateOtherDetailView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
        except KeyError:
            return redirect('/interview_homepage')
        
        candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
        if candidate_status <=4:
            return redirect('/candidate_source_of_info')
        
        return render(request, 'other_details.html')

    def post(self, request, *args, **kwargs):
        service_commitment = request.POST.get('service_commitment')
        salary_deposit = request.POST.get('salary_deposit')
        shift = request.POST.get('shift')
        expected_joining_date = request.POST.get('expected_joining_date')
        salary_expected = request.POST.get('salary_expected')
        candidate_id = request.session['candidate_id']
        candidate_obj = queries.get_candidate_details_by_id(candidate_id).first()

        if existing_details := queries.get_model_by_candidate_id(CandidateOtherDetails,candidate_id).first():
            existing_details.service_commitment = service_commitment
            existing_details.salary_security = salary_deposit
            existing_details.shift = shift
            existing_details.expected_joining_date = expected_joining_date
            existing_details.salary_expected = salary_expected
            existing_details.save()

        else:
            other_details = CandidateOtherDetails()
            other_details.candidate = candidate_obj
            other_details.service_commitment = service_commitment
            other_details.salary_security = salary_deposit
            other_details.shift = shift
            other_details.expected_joining_date = expected_joining_date
            other_details.salary_expected = salary_expected
            other_details.save()

            profile_status = queries.get_candidate_details_by_id(candidate_id).first()
            profile_status.status = 6
            profile_status.profile_progress = 'Complete'
            profile_status.save()

        return redirect("/exam_start")
