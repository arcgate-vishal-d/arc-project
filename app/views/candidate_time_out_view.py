from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.conf import settings

from app import models
from app.utility import queries


class CandidateTimeOut(BaseDetailView):
    def get(self, request, *args, **kwargs):
        candidate_id = request.session['candidate_id']
        candidate_time = queries.get_candidate_details_by_id(candidate_id).first()
        candidate_time.timer = 0
        candidate_time.save()
        response_data = True
        return JsonResponse(response_data,safe=False)
