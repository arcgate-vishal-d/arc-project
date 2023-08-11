from django.http import QueryDict
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.template.loader import get_template

from app.models import InterviewParameter, PersonalInterview, CandidateResults, InterviewParameter
from app.forms import AddParameterForm
from app.utility import queries, constants, return_message, candidate_module_functions


class AdminResultPersonalInterview(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        parameter_form = AddParameterForm()
        candidate_id = self.kwargs['candidate_id']
        candidate = queries.get_candidate_details_by_id(candidate_id).first()
        parameters = InterviewParameter.objects.all()

        context = {
            'parameter_form': parameter_form,
            'candidate': candidate,
            'parameters': parameters,
        }

        return render(request, 'admin_result_personal_interview.html', context)
    
    def post(self, request, *args, **kwargs):
        candidate_id = self.kwargs['candidate_id']
        data = QueryDict(request.body)
        method = request.POST.get('method')
        parameter_id = request.POST.get("parameter_id")
        if method == 'delete':
            try:
                InterviewParameter.objects.filter(id=parameter_id).delete()
                messages.success(
                    request, return_message.MESSAGE['content_deleted'])
                return redirect(f'/candidate_personal_interview/{candidate_id}')
            except Exception as e:
                    messages.error(request, e)
                    return redirect(f'/candidate_personal_interview/{candidate_id}')
        candidate = queries.get_candidate_details_by_id(candidate_id).first()
        parameters = InterviewParameter.objects.all()
        if PersonalInterview.objects.filter(candidate=candidate_id):
            PersonalInterview.objects.filter(candidate=candidate_id).delete()
        for parameter, action in data.items():
            if parameter == 'csrfmiddlewaretoken':
                continue
            score_instance = PersonalInterview()
            user = queries.get_user_by_username(request.user)
            candidate_instance = queries.get_candidate_details_by_id(candidate_id).first().id
            parameter_instance = InterviewParameter.objects.filter(parameter=parameter).first()
            score_instance.candidate_id = candidate_instance
            score_instance.parameter = parameter_instance
            score_instance.interviewer = user
            score_instance.action = action
            score_instance.save()

        
        parameter = request.POST.get('parameter')
        if parameter:
            user_instance =  queries.get_user_by_username(request.user)
            parameter_instance = InterviewParameter()
            parameter_instance.parameter = parameter
            parameter_instance.created_by = user_instance
            parameter_instance.save()
            messages.success(
                    request, return_message.MESSAGE['content_added'])
            return redirect(f'/candidate_personal_interview/{candidate_id}')

        interview_results = PersonalInterview.objects.filter(candidate=candidate_id)
        interviewer = interview_results.first()
        context = {
            'candidate': candidate,
            'parameters': parameters,
            'interview_results': interview_results,
            'interviewer':interviewer,
        }
        # return render(request,'candidate_personal_interview_pdf.html',context)
        template = get_template('candidate_personal_interview_pdf.html')
        html = template.render(context)

        # converting html template to pdf with candidate context data
        pdf = candidate_module_functions.render_to_pdf('candidate_personal_interview_pdf.html',context)
        if pdf:
            response = HttpResponse(pdf,content_type="application/pdf")
            filename = f"personal_interview_{context['candidate'].first_name}{context['candidate'].last_name}.pdf"
            content = f"inline; filename={filename}"
            download =  request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse(html)
