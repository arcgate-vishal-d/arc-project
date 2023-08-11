from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateFamilyDetails
from app .utility import queries


class CandidateFamilyDetailView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
        except KeyError:
            return redirect('/interview_homepage')
        
        candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
        family_details = queries.get_model_by_candidate_id(CandidateFamilyDetails,candidate_id_new).all()
        if candidate_status <= 1:
            return redirect('/candidate_education_details')
        if family_details or candidate_status == 2:
            profile_status = queries.get_candidate_details_by_id(candidate_id_new).first()
            profile_status.status = 3
            profile_status.save()
            
        context = {
            'family_details': family_details
        }
        return render(request, 'family_detail.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        candidate_id = request.session['candidate_id']
        family_detail_id = request.POST.get('family_delete')
        try:
            if method == 'delete':
                details = CandidateFamilyDetails.objects.filter(
                    id=family_detail_id).first()
                details.delete()

            else:
                candidate_obj = queries.get_candidate_details_by_id(candidate_id).first() 
                name = request.POST.get('relation_name')
                relation = request.POST.get('relation')
                occupation = request.POST.get('occupation')
                dependent = request.POST.get('relation_dependent')
                family_details = CandidateFamilyDetails()
                family_details.candidate = candidate_obj
                family_details.name = name
                family_details.relation = relation
                family_details.occupation = occupation
                family_details.dependent = dependent
                family_details.save()

                profile_status = queries.get_candidate_details_by_id(candidate_id).first()
                profile_status.status = 3
                profile_status.save()

        except Exception:
            return redirect('/candidate_family_details')
        return redirect('/candidate_family_details')
