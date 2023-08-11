import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utility import queries, return_message, question_module_functions
from app.models import SubjectQuestionMap, SubjectQuestionMap, SubjectQuestionMap

@question_module_functions.admin_required()
class PaperSetupDetails(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        paper_id = self.kwargs['id']
        paper_details = queries.get_paper_setup_description_by_id(paper_id)
        paper_subjects = queries.get_paper_subject_map_by_paper_id(paper_id)
        subject_linked_questions = {}
        all_entries_paper = queries.get_subject_question_data_paper_by_id(
            paper_id)

        for paper_subject in paper_subjects:
            subject_related_questions = []
            subject_related_questions.extend(queries.get_subjective_questions_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_multiple_choice_questions_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_image_multiple_choice_questions_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_image_subjective_questions_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_excel_questions_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_passage_instruction_content_by_subject(paper_subject.subject))
            subject_related_questions.extend(queries.get_multi_image_choice_question_by_subject(paper_subject.subject))

            subject_linked_questions[paper_subject] = subject_related_questions
        context = {
            "paper": paper_details,
            "subjects": paper_subjects,
            "dict": subject_linked_questions
        }
        if all_entries_paper:
            context['allEntry'] = all_entries_paper
        return render(request, 'paper_setup_details.html', context)

    def post(self, request, *args, **kwargs):
        question_combinations = request.POST.getlist('checked_questions')
        paper_id = self.kwargs['id']
        existing_paper_data = queries.get_subject_question_data_paper_by_id(
            paper_id)

        map_strings = []
        for map in existing_paper_data:
            map_string = (
                f"{map.paper_setup_id.id},{map.paper_setup_subject_id.subject.id},{map.all_question_id.id}")
            map_strings.append(map_string)
            if map_string not in question_combinations:
                map.delete()

        for combination in question_combinations:
            if combination not in map_strings:
                single_question_entry = combination.split(',')

                paper_obj = queries.get_paper_setup_description_by_id(single_question_entry[0])
                paper_subject_map_obj = queries.get_paper_subject_map_by_subject_id(
                    single_question_entry[1], single_question_entry[0])
                for index, question_id in enumerate(single_question_entry):
                    if index == 2:
                        subject_question_map = SubjectQuestionMap()
                        subject_question_map.paper_setup_id = paper_obj
                        subject_question_map.paper_setup_subject_id = paper_subject_map_obj
                        subject_question_map.all_question_id = queries.get_all_question_id(
                            question_id)
                        subject_question_map.save()

        messages.success(
                    request, return_message.MESSAGE['questions_linked'])
        return redirect("/paper_setup")
