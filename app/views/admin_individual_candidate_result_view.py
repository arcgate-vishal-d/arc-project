from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from app import models
from app.utility import queries, constants, return_message


class AdminIndividualResult(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        candidate_id = self.kwargs['candidate_id']
        candidate_details = queries.get_candidate_details_by_id(candidate_id)

        if not candidate_details:
            messages.error(
                request, return_message.MESSAGE['invalid_candidate'])
            return redirect("/admin_view_result")

        marks = models.CandidateResultIndividual.objects.filter(
            candidate=candidate_id).aggregate(Sum('answer_marks'))['answer_marks__sum']
        paper = queries.get_candidate_individual_result_by_id(candidate_id, None)
        if not paper:
            messages.error(request, return_message.MESSAGE['not_appeared'])
            return redirect("/admin_view_result")
        
        paper_id = paper.first().paper_set_id
        paper_subjects = queries.get_paper_subject_map_by_paper_id(paper_id)
        paper_data = {}
        candidate_answers = {}
        for subject in paper_subjects:
            subject_question = []
            for question in queries.get_candidate_individual_result_by_paperId_candidateId_paper_subId(paper_id, candidate_id, subject):
                candidate_answers[question.subject_question_id.all_question_id.id] = question
                
                subjective_question = queries.get_subjectitve_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if subjective_question:
                    subject_question.append(subjective_question)

                image_based_subjective = queries.get_image_subjectitve_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if image_based_subjective:
                    subject_question.append(image_based_subjective)

                image_based_mcq = queries.get_image_multiple_choice_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if image_based_mcq:
                    subject_question.append(image_based_mcq)

                multiple_choice_question = queries.get_multiple_choice_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if multiple_choice_question:
                    subject_question.append(multiple_choice_question)

                excel_question = queries.get_excel_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if excel_question:
                    subject_question.append(excel_question)

                passage_question = queries.get_passage_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if passage_question:
                    subject_question.append(passage_question)

                multi_image = queries.get_multi_image_choice_question_by_allquestion_id(
                    question.subject_question_id.all_question_id.id)
                if multi_image:
                    subject_question.append(multi_image)

            paper_data[subject] = subject_question
        context = {
            "candidate_details": candidate_details,
            "paper": paper,
            "marks": marks,
            "dict": paper_data,
            "paper_subjects": paper_subjects,
            "candidate_answers": candidate_answers,
        }
        return render(request, "admin_individual_candidate_result.html", context)

    def post(self, request, *args, **kwargs):
        candidate_id = str(self.kwargs['candidate_id'])
        candidate_result = request.POST.get("candidate_result")
        manual_marks = int(request.POST.get(candidate_result))
        candidate = models.CandidateResultIndividual.objects.filter(
            id=candidate_result).first()
        candidate.answer_marks = manual_marks
        candidate.answer_status = constants.INCORRECT if manual_marks == 0 else constants.CORRECT
        candidate.save()
        messages.success(
            request, return_message.MESSAGE['manual_marks'])
        return redirect("/individual_result/" + candidate_id)
