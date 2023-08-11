from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateWorkExperience
from app.utility import queries

class CandidateWorkExperienceDetailView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
        except KeyError:
            return redirect('/interview_homepage')
        work_exp = queries.get_model_by_candidate_id(CandidateWorkExperience,candidate_id_new).all()
        
        candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
        if candidate_status <= 2:
            return redirect('/candidate_family_details')
        
        if candidate_status == 3:
            profile_status = queries.get_candidate_details_by_id(candidate_id_new).first()
            profile_status.status = 4
            profile_status.save()

        context = {
            'work_exp': work_exp
        }
        return render(request, 'work_experience.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        work_exp_detail_id = request.POST.get('work_exp_delete')
        candidate_id = request.session['candidate_id']
        try:
            if method == 'delete':
                work_exp_details = CandidateWorkExperience.objects.filter(
                    id=work_exp_detail_id).first()
                work_exp_details.delete()

            else:
                candidate_obj = queries.get_candidate_details_by_id(candidate_id).first() 
                name_of_company = request.POST.get('name_of_company')
                designation = request.POST.get('designation')
                joining_date = request.POST.get('joining_date')
                reliving_date = request.POST.get('reliving_date')
                reason_of_leaving = request.POST.get('reason_of_leaving')
                last_salary = request.POST.get('last_salary')
                work_exp = CandidateWorkExperience()
                work_exp.candidate = candidate_obj               
                work_exp.name_of_company = name_of_company
                work_exp.designation = designation
                work_exp.joining_date = joining_date
                work_exp.reliving_date = reliving_date
                work_exp.reason_of_leaving = reason_of_leaving
                work_exp.last_salary = last_salary
                work_exp.save()

                profile_status = queries.get_candidate_details_by_id(candidate_id).first()
                profile_status.status = 4
                profile_status.save()

        except Exception:
            return redirect('/candidate_work_experience')

        return redirect('/candidate_work_experience')
