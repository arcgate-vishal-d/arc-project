from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateSourceOfInformation
from app.utility import queries

class CandidateSourceOfInformationView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
        except KeyError:
            return redirect('/interview_homepage')
        candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
        if candidate_status <=3:
            return redirect('/candidate_work_experience')
       
        return render(request, 'source_of_info.html')

    def post(self, request, *args, **kwargs):
        interviewed = request.POST.get('interviewed')
        worked = request.POST.get('worked')
        information_for_hiring = request.POST.getlist('information_for_hiring')
        consultancy = request.POST.get('consultancy_name')
        candidate_id = request.session['candidate_id']
        candidate_obj = queries.get_candidate_details_by_id(candidate_id).first()

        if existing_details := queries.get_model_by_candidate_id(CandidateSourceOfInformation,candidate_id).first():
            existing_details.previous_interviewed = interviewed
            existing_details.previous_worked = worked
            existing_details.source_of_info = information_for_hiring
            existing_details.consultancy = consultancy
            existing_details.save()

        else:
            source_of_info = CandidateSourceOfInformation()
            source_of_info.candidate = candidate_obj
            source_of_info.previous_interviewed = interviewed
            source_of_info.previous_worked = worked
            source_of_info.source_of_info = information_for_hiring
            source_of_info.consultancy = consultancy
            source_of_info.save()

            profile_status = queries.get_candidate_details_by_id(candidate_id).first()
            profile_status.status = 5
            profile_status.save()

        return redirect('/candidate_other_details')
