from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateEducationDetails, CandidateDetails
from app.ArcSheet import base_view
from app.utility import queries
import threading


class CandidateEducationalDetailView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
        except KeyError:
            return redirect('/interview_homepage')
        
        candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
        edu_details = queries.get_model_by_candidate_id(
            CandidateEducationDetails,candidate_id_new).all()
        username_edu = queries.get_candidate_details_by_id(candidate_id_new).first()
        if candidate_status == 0:
            return redirect('/candidate_personal_details')
        if edu_details:
            profile_status = queries.get_candidate_details_by_id(candidate_id_new).first()
            profile_status.status = 2
            profile_status.save()

        context = {
            'edu_details': edu_details,
            'edu_username': username_edu
        }

        # thread for creating sheet for the user
        flag =True
        candidate_sheet = CandidateDetails.objects.filter(id=candidate_id_new).first().sheet_id
        if candidate_sheet:
            flag = False
        while flag:
            try:
                t1 = threading.Thread(
                    target=base_view.create_candidate_sheet, args=(candidate_id_new,))
                # starting thread 1
                t1.start()
                flag=False
            except Exception as e:
                print("Error: unable to start thread")

        return render(request, 'education.html', context)

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        edu_detail_id = request.POST.get('edu_delete')
        candidate_id = request.session['candidate_id']

        try:
            if method == 'delete':
                details = CandidateEducationDetails.objects.filter(
                    id=edu_detail_id).first()
                details.delete()

                if not queries.get_model_by_candidate_id(CandidateEducationDetails, candidate_id):
                    profile_status = queries.get_candidate_details_by_id(candidate_id).first()
                    profile_status.status = 1
                    profile_status.save()

            else:
                qualification = request.POST.get('qualifications')
                education_details = request.POST.get('education_details')
                school_college = request.POST.get('school_college')
                board_university = request.POST.get('board_university')
                year_of_passing = request.POST.get('year_of_passing')
                percentage = request.POST.get('percentage')
                division = request.POST.get('division')
                medium = request.POST.get('medium')

                edu_info = CandidateEducationDetails()
                candidate_obj = queries.get_candidate_details_by_id(candidate_id).first()       
                edu_info.candidate = candidate_obj
                edu_info.qualifications = qualification
                edu_info.education_details = education_details
                edu_info.school_college = school_college
                edu_info.board_university = board_university
                edu_info.year_of_passing = year_of_passing
                edu_info.percentage = percentage
                edu_info.division = division
                edu_info.medium = medium
                edu_info.save()

                profile_status = queries.get_candidate_details_by_id(candidate_id).first()
                profile_status.status = 2
                profile_status.save()
        except Exception as e:
            return redirect('/candidate_education_details')

        return redirect('/candidate_education_details')
