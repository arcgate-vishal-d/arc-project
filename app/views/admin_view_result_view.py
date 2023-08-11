import json
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import QueryDict, JsonResponse
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger
from django.contrib.auth.models import User

from app.models import CandidateResultIndividual, CandidateResults, CandidateDetails, PaperSetupSubjectMap, Grades, PersonalInterviewMap
from app.utility import queries, constants, return_message


class AdminViewResult(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        team_lead = request.GET.get('team_lead')

        # set team lead if the loggeg in user is interviewer
        logged_in_user = queries.get_user_by_id(request.user.id)
        if not logged_in_user.is_staff:
            team_lead = logged_in_user.id
        if not from_date and to_date:
            messages.error(request, return_message.MESSAGE['date_range_error'])
        data = queries.get_candidate_result_and_interviewer(from_date, to_date)
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data_for_search'])

        if team_lead:
            candidate_list = []
            for candidate in data:
                search_team_lead = queries.get_personal_interview_mappming_by_candidate_and_teamlead_id(team_lead,candidate.id)

                if search_team_lead is not None:
                    candidate_id = search_team_lead.interviewee.id
                    candidate_object = queries.get_candidate_details_by_id(candidate_id).first()
                    candidate_list.append(candidate_object)
            if candidate_list:
                data = candidate_list

        paginator = Paginator(data, constants.PAGE_LIMIT)
        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
            if team_lead and not candidate_list:
                messages.error(request, return_message.MESSAGE['no_data'])
                page_obj = None
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['invalid_page'])

        query_params = ''
        if (from_date or to_date or team_lead):
            query_params = (
                f"&from_date={from_date}&to_date={to_date}&team_lead={team_lead}")
        interviewer = User.objects.all()
        context = {
            'query': query_params,
            'interviewer': interviewer,
            'candidates_details': page_obj,
            'data': page_obj,
            'from_date': from_date,
            'to_date': to_date,
            'tl': str(team_lead)

        }
        if not team_lead or not logged_in_user.is_staff:
            del context['tl']

        return render(request, 'admin_result_view.html', context)

    def post(self, request, *args, **kwargs):

        # delete request for selected scenerio
        method = request.POST.get('method')
        if method == "delete":
            candiate_id = request.POST.get('candidate_id')
            team_lead_id = request.POST.get('teamlead')
            map_obj = queries.get_personal_interview_mappming_by_candidate_and_teamlead_id(
                team_lead_id, candiate_id)
            if map_obj:
                messages.success(
                    request, return_message.MESSAGE['user_delete'])
                map_obj.delete()
            else:
                messages.error(
                    request, return_message.MESSAGE['user_not_found'])

            return redirect(f'/admin_view_result?team_lead={team_lead_id}')

        data = QueryDict(request.body)
        data = dict(data)
        for key, value in data.items():
            if key == 'SelectedTeamLeadID':
                for interviewer_id in value:
                    interviewee_id = interviewer_id

            if key == "forwarded_candidate":
                for interviewee_id in value:
                    if interviewer_id: 
                        if not queries.get_personal_interview_mappming_by_candidate_and_teamlead_id(interviewer_id, interviewee_id):
                            forward_instance = PersonalInterviewMap()
                            forward_instance.interviewer_id = interviewer_id
                            forward_instance.interviewee_id = interviewee_id
                            forward_instance.save()
                        messages.success(request, return_message.MESSAGE['export_success'])
                    else:
                        messages.error(
                    request, return_message.MESSAGE['error_occur'])
        return redirect('/admin_view_result')


class AdminViewResultDetails(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get('row_id')
        candidate_attended_subjects = CandidateResultIndividual.objects.values('paper_subject_id').annotate(
            count=Count('paper_subject_id')).filter(candidate=candidate_id).order_by()
        candidate_result_details = {}
        for subject in candidate_attended_subjects:
            candidate_subject_amrks = 0
            subject = queries.get_paper_setup_subject_map_by_id(
                subject['paper_subject_id'])
            for atmp_question_obj in queries.get_candidate_individual_result_by_id(candidate_id, subject):
                candidate_subject_amrks += atmp_question_obj.answer_marks

            # calculating percentage for each subject
            subject_percent = (candidate_subject_amrks /
                               subject.subject_marks)*100
            subject = str(subject.subject)
            candidate_result_details[subject] = subject_percent

        grades = []
        for grade in Grades.objects.all():
            grade_name = grade.title
            grade.title = {}
            grade.title['title'] = grade_name
            grade.title['from'] = grade.grade_from
            grade.title['to'] = grade.grade_to
            grades.append(grade.title)
        resp_data = [candidate_result_details, grades]
        return JsonResponse(resp_data, safe=False)
