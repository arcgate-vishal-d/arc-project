import os
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.forms import MultipleChoiceQuestionForm, MCQSearchForm
from app.utility import queries, return_message, constants, question_module_functions
from app.models import MultipleChoiceQuestions, AllQuestions

@question_module_functions.superuser_required()
class MultiPleChoiceQuestion(LoginRequiredMixin, BaseDetailView):
    """ List view of all multiple choice question with search functionality and pagination"""

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        search_question = request.GET.get("question_title")
        search_subject = request.GET.get("subjects")
        initial_dict = {
            'question_title': search_question,
            'subjects': search_subject
        }

        data = queries.get_multiple_choice_question(
            search_question, search_subject)
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data'])

        paginator = Paginator(data, constants.PAGE_LIMIT)
        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['invalid_page'])

        multiple_choice_question_form = MultipleChoiceQuestionForm()
        multiple_choice_question_Search_form = MCQSearchForm(
            initial=initial_dict)
        query_params = ""
        if (search_question or search_subject):
            query_params = (
                f"&question_title={search_question}&subjects={search_subject}")
        context = {
            'query': query_params,
            "mcq_form": multiple_choice_question_form,
            "mcq_search_form": multiple_choice_question_Search_form,
            'data': page_obj,
            'initial_dict': initial_dict
        }
        return render(request, 'admin_multiple_choice_questions.html', context)

@question_module_functions.superuser_required()
class MCQViews(LoginRequiredMixin, BaseDetailView):

    def post(self, request, *args, **kwargs):

        user = queries.get_user_by_username(request.user)
        method = request.POST.get('method')
        subject = request.POST.get('subjects')

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/mulitple_choice_question')

        # getting subject instance for specified methods
        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/mulitple_choice_question')
            except Exception as e:
                messages.error(request, e)
                return redirect('/mulitple_choice_question')

        # checking special subjects should not be link with
        if question_module_functions.check_fixed_subjects(subject):
            messages.error(
                request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
            return redirect('/mulitple_choice_question')

        passage = request.POST.get('passage')
        if not passage:
            passage = None

        mcq_id = request.POST.get('mcq_id')
        question_title = request.POST.get('question_title')
        option_a = request.POST.get('optionA')
        option_b = request.POST.get('optionB')
        option_c = request.POST.get('optionC')
        option_d = request.POST.get('optionD')
        
        if question_module_functions.unique_options(option_a,option_b,option_c,option_d,method):
            messages.error(
                    request, return_message.MESSAGE['duplicate_options'])
            return redirect('/mulitple_choice_question')
        
        answer_key = request.POST.get('AnswerKey')
        if method:
            flag = True
            if not mcq_id:
                flag = False
            if flag:
                multiple_choice_question = queries.get_multiple_choice_question_by_id(
                    mcq_id)
                if multiple_choice_question is None:
                    flag = False
            if not flag:
                messages.error(request, return_message.MESSAGE['null_id'])
                return redirect('/mulitple_choice_question')

            all_question = queries.get_all_question_id(
                        multiple_choice_question.question_id.id)
            if method == "put":
                '''Updating an existing question'''
                try:
                    all_question.subject = subject
                    all_question.save()

                    multiple_choice_question.created_by = user
                    multiple_choice_question.question_title = question_title.strip()
                    multiple_choice_question.answer_key = question_module_functions.correct_ans(answer_key,
                                                                                                option_a, option_b,
                                                                                                option_c, option_d)
                    multiple_choice_question.optionA = option_a.strip()
                    multiple_choice_question.optionB = option_b.strip()
                    multiple_choice_question.optionC = option_c.strip()
                    multiple_choice_question.optionD = option_d.strip()
                    multiple_choice_question.passage = queries.get_passage_by_id(
                        passage)
                    multiple_choice_question.save()
                    messages.success(
                        request, return_message.MESSAGE['question_updated'])
                except Exception as e:
                    messages.error(request, e)
                return redirect('/mulitple_choice_question')

            if method == "delete":
                '''Deleting an existing question'''
                try:
                    all_question.delete()
                    messages.success(
                        request, return_message.MESSAGE['question_deleted'])
                    return redirect('/mulitple_choice_question')
                except Exception as e:
                    messages.error(request, e)
                    return redirect("/mulitple_choice_question")

        else:
            '''Create new question'''
            try:
                all_question_obj = AllQuestions()
                all_question_obj.subject = subject
                all_question_obj.type = constants.MULTIPLE_CHOICE_QUESTION
                all_question_obj.save()

                question_obj = MultipleChoiceQuestions()
                question_obj.question_id = all_question_obj
                question_obj.created_by = user
                question_obj.question_title = question_title.strip()
                question_obj.answer_key = question_module_functions.correct_ans(answer_key,
                                                                                option_a, option_b,
                                                                                option_c, option_d)
                question_obj.optionA = option_a.strip()
                question_obj.optionB = option_b.strip()
                question_obj.optionC = option_c.strip()
                question_obj.optionD = option_d.strip()
                question_obj.passage = queries.get_passage_by_id(passage)
                question_obj.save()
                messages.success(
                    request, return_message.MESSAGE['question_added'])
            except Exception as e:
                all_question_obj.delete()
                messages.error(request, e)
            return redirect('/mulitple_choice_question')
