from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import BaseDetailView
from django.template.loader import get_template

from app.utility import candidate_module_function,constants
from app import models
from app.utility import queries

class CandidateFactSheet(BaseDetailView):
    def get(self, request, *args, **kwargs):
        candidate_id = request.GET.get("cid")
        candidate_obj = queries.get_candidate_details_by_id(candidate_id).first()
        source_info_obj = queries.get_model_by_candidate_id(models.CandidateSourceOfInformation, candidate_id).first()
        candidate_education = queries.get_model_by_candidate_id(models.CandidateEducationDetails, candidate_id)
        candidate_family = queries.get_model_by_candidate_id(models.CandidateFamilyDetails, candidate_id)
        candidate_work_experience = queries.get_model_by_candidate_id(models.CandidateWorkExperience, candidate_id)
        candidate_other_details = queries.get_model_by_candidate_id(models.CandidateOtherDetails,candidate_id).first()
        # retrieving attempted subjects of paper and percentage
        candidate_attended_subjects = models.CandidateResultIndividual.objects.values('paper_subject_id').annotate(
            count=Count('paper_subject_id')).filter(candidate=candidate_id).order_by()
        candidate_result_details = {}
        accuracy = None
        if models.CandidateResultIndividual.objects.filter(candidate=candidate_id,paper_subject_id__subject__subject=constants.TYPING_TEST):
            accuracy = models.CandidateResultIndividual.objects.filter(candidate=candidate_id, paper_subject_id__subject__subject=constants.TYPING_TEST).first().candidate_answer
        for subject in candidate_attended_subjects:
            candidate_subject_amrks = 0
            subject = queries.get_paper_setup_subject_map_by_id(subject['paper_subject_id'])
            for atmp_question_obj in queries.get_candidate_individual_result_by_id(candidate_id, subject):
                candidate_subject_amrks += atmp_question_obj.answer_marks

            # calculating percentage for each subject
            subject_percent = round((candidate_subject_amrks / subject.subject_marks) * 100, 2)
            subject = str(subject.subject)
            # print("subject : ", subject)
            candidate_result_details[subject] = subject_percent
            
            # print(candidate_result_details)
            

        # converting knowing source string into list
        source_info_list = None
        if source_info_obj:
            source_info_list = source_info_obj.source_of_info[1:len(source_info_obj.source_of_info)-1]
            source_info_list = source_info_list.split(',')
            source_info_list = [item.strip("' ") for item in source_info_list]

        template = get_template('candidate_fact_sheet.html')
        context = {
            "candidate_personal":candidate_obj,
            "candidate_source":source_info_obj,
            "education": candidate_education,
            "other_details":candidate_other_details,
            "subjects": candidate_result_details,
            "accuracy":accuracy,
            
        }
        
        # adding knowing sourde only if exist
        if source_info_list:
            context["source_list"] = source_info_list
        # adding family data only if exist
        if candidate_family:
            context["family_members"] = candidate_family

        # adding work experience only if exist
        if candidate_work_experience:
            context["experience"] = candidate_work_experience

        html = template.render(context)

        # converting html template to pdf with candidate context data
        pdf = candidate_module_function.render_to_pdf('candidate_fact_sheet.html',context)
        if pdf:
            response = HttpResponse(pdf,content_type="application/pdf")
            filename = f"factsheet_{context['candidate_personal'].first_name}{context['candidate_personal'].last_name}.pdf"
            content = f"inline; filename={filename}"
            download =  request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse(html)
