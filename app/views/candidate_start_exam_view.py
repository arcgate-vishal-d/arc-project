from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView

from app.utility import queries
from app import models


class ExamStartView(BaseDetailView):

    def get(self, request, *args, **kwargs):
        try:
            candidate_id_new = request.session['candidate_id']
            candidate_level = queries.get_candidate_details_by_id(candidate_id_new).first().test_level
            paper_set = models.PaperHistory.objects.filter(paper_set__test_level__test_level = candidate_level).last().paper_set
            paper_data = models.PaperSetupSubjectMap.objects.filter(paper_setup_id__paper_title = paper_set)

            candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
            if candidate_status <= 5:
                return redirect('/candidate_other_details')

            context = {
                "paper_set": paper_set,
                "paper_data": paper_data,
            }
            
            return render(request, "candidate_start_exam.html", context)
        except KeyError:
            return redirect('/interview_homepage')
