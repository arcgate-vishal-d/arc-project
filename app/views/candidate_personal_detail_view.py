from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.models import CandidateDetails, TestLevels, PaperHistory
from app.utility import queries


class CandidatePersonalView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        test_levels = TestLevels.objects.all()
        username = CandidateDetails.objects.all()
        context = {
            'test_levels': test_levels,
            'username': username
        }
        return render(request, "personal_Details.html", context)

    def post(self, request, *args, **kwargs):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            test_level = request.POST.get('test_level')
            email = request.POST.get('email')
            dob = request.POST.get('dob')
            mobile_1 = request.POST.get('mobile_1')
            mobile_2 = request.POST.get('mobile_2')
            present_add = request.POST.get('present_address')
            permanent_add = request.POST.get('permanent_address')
            present_dist = request.POST.get('present_district')
            permanent_dist = request.POST.get('permanent_district')

            test_level_instance = TestLevels.objects.filter(
                id=test_level).first()

            try:
                session_id = request.session['candidate_id']
                candidate_info = CandidateDetails.objects.filter(
                    id=session_id).first()
            except Exception:
                candidate_info = CandidateDetails()
                candidate_info.status = 1
            candidate_paper_set_time = PaperHistory.objects.filter(
                    paper_set__test_level__test_level=test_level_instance).last().paper_set.paper_time

            candidate_info.first_name = first_name
            candidate_info.last_name = last_name
            candidate_info.gender = gender
            candidate_info.email = email
            candidate_info.dob = dob
            candidate_info.mobile_no_1 = mobile_1
            if mobile_2:
                candidate_info.mobile_no_2 = mobile_2
            candidate_info.present_address = present_add
            candidate_info.permanent_address = permanent_add
            candidate_info.test_level = test_level_instance
            candidate_info.district_present = present_dist
            candidate_info.district_permanent = permanent_dist
            candidate_info.status = 1
            candidate_info.timer = candidate_paper_set_time
            candidate_info.save()
            candidate_id = candidate_info.id
            request.session['candidate_id'] = candidate_id

            return redirect('/candidate_education_details')
        except Exception as e:
            print(e)
            return redirect('/interview_homepage')
