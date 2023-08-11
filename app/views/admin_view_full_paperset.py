from django.shortcuts import render
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.utility import queries, question_module_functions
from app import models

@question_module_functions.admin_required()
class ViewFullPaperSet(LoginRequiredMixin, BaseDetailView):
    def get(self, request,  *args, **kwargs):
        paper_id = self.kwargs['paper_id']
        paper_information = queries.get_paper_setup_description_by_id(paper_id)
        paper_subjects = queries.get_paper_subject_map_by_paper_id(paper_id)
        paper_data = {}
        for subject in paper_subjects:
            subject_question = []
            for question in queries.get_subject_question_data_paper_by_id(paper_id, subject):

                subjective_question = queries.get_subjectitve_question_by_allquestion_id(
                    question.all_question_id.id)
                if subjective_question:
                    subject_question.append(subjective_question)

                image_based_subjective = queries.get_image_subjectitve_question_by_allquestion_id(
                    question.all_question_id.id)
                if image_based_subjective:
                    subject_question.append(image_based_subjective)

                image_based_mcq = queries.get_image_multiple_choice_question_by_allquestion_id(
                    question.all_question_id.id)
                if image_based_mcq:
                    subject_question.append(image_based_mcq)

                multiple_choice_question = queries.get_multiple_choice_question_by_allquestion_id(
                    question.all_question_id.id)
                if multiple_choice_question:
                    subject_question.append(multiple_choice_question)

                excel_question = queries.get_excel_question_by_allquestion_id(
                    question.all_question_id.id)
                if excel_question:
                    subject_question.append(excel_question)

                passage_question = queries.get_passage_question_by_allquestion_id(
                    question.all_question_id.id)
                if passage_question:
                    subject_question.append(passage_question)

                multi_image = queries.get_multi_image_choice_question_by_allquestion_id(
                    question.all_question_id.id)
                if multi_image:
                    subject_question.append(multi_image)

            paper_data[subject] = subject_question

        context = {
            "paper": paper_information,
            "dict": paper_data,
        }
        return render(request, 'admin_view_full_paperset.html', context)
