from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.models import MultipleImageChoiceQuestion, AllQuestions
from app.utility import queries, return_message, constants, question_module_functions
from app.forms.multiple_image_choice_que_form import MICQForms, MICQSearchForm

@question_module_functions.superuser_required()
class MultipleImageChoiceQuestionGetView(LoginRequiredMixin, BaseDetailView):
    """Search filter, pagination and get all data on reload functionality """

    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', constants.DEFAULT_PAGE)
        search_question = request.GET.get('question_title')
        search_subject = request.GET.get('subject')

        initial_dict = {
            "question_title": search_question,
            "subject": search_subject
        }

        form = MICQForms()
        search_form = MICQSearchForm(initial_dict)

        data = queries.get_multiple_img_choice_que_all(
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
        query_params = ""
        if (search_question or search_subject):
            query_params = (
                f"&question_title={search_question}&subject={search_subject}"
            )

        context = {
            'query': query_params,
            'data': page_obj,
            'search_form': search_form,
            'form': form,
            'question_title': search_question,
            'subject': search_subject
        }
        return render(request, "multiple_image_choice_que.html", context)

@question_module_functions.superuser_required()
class MultipleImageChoiceQuestionPostView(LoginRequiredMixin, BaseDetailView):
    """Add, Update and Delete Multiple image choice question"""

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        subject_id = request.POST.get('subjects')

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/multiple_img_choice_que')

         # getting subject instance for specified methods
        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject_id).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/multiple_img_choice_que')
            except Exception as e:
                messages.error(request, e)
                return redirect('/multiple_img_choice_que')

            # checking special subjects should not be link with
            if question_module_functions.check_fixed_subjects(subject):
                messages.error(
                    request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
                return redirect('/multiple_img_choice_que')

        question_id = request.POST.get('question_id')
        question_title = request.POST.get("question_title")
        answer_key = request.POST.get('AnswerKey')
        optionA = request.FILES.get('optionA')
        optionB = request.FILES.get('optionB')
        optionC = request.FILES.get('optionC')
        optionD = request.FILES.get('optionD')

        if method:
            question_flag = bool(question_id)
            if question_flag:
                question_data = queries.get_multiple_image_choice_que_by_id(
                    question_id)
                if question_data is None:
                    question_flag = False
            if not question_flag:
                messages.error(
                    request, return_message.MESSAGE['content_not_found'])
                return redirect("/multiple_img_choice_que")

            all_question = queries.get_all_question_id(
                question_data.question_id.id)
            if method == 'put':
                '''Updating an existing question'''
                try:
                    question_title = question_title.strip()

                    all_question_obj = AllQuestions()
                    all_question_obj.subject = queries.get_subject(
                        subject_id).first()
                    all_question_obj.type = constants.MULTIPLE_IMAGE_CHOICE_QUESTION
                    all_question_obj.save()

                    que_update = queries.get_multiple_image_choice_que_by_id(
                        question_id)

                    que_update.question_title = question_title
                    que_update.question_id = all_question_obj

                    

                    # Update image
                    if optionA is not None:
                        que_update.optionA = optionA
                    if optionB is not None:
                        que_update.optionB = optionB
                    if optionC is not None:
                        que_update.optionC = optionC
                    if optionD:
                        que_update.optionD = optionD

                    # Update option
                    if answer_key == 'optionA':
                        que_update.answer_key = que_update.optionA
                    elif answer_key == 'optionB':
                        que_update.answer_key = que_update.optionB
                    elif answer_key == 'optionC':
                        que_update.answer_key = que_update.optionC
                    else:
                        que_update.answer_key = que_update.optionD

                    que_update.save()

                    messages.success(
                        request, return_message.MESSAGE['question_update'])
                    return redirect('/multiple_img_choice_que')

                except Exception as e:
                    messages.error(request, e)
                    return redirect('/multiple_img_choice_que')

            elif method == 'delete':
                """Delete existing question"""
                try:
                    all_question.delete()
                    messages.success(request,
                                     return_message.MESSAGE['question_deleted']
                                     )
                    return redirect("/multiple_img_choice_que")

                except Exception as e:
                    messages.error(request, e)
                    return redirect("/multiple_img_choice_que")

        else:
            """Add new question"""
            try:

                all_question_obj = AllQuestions()
                all_question_obj.subject = queries.get_subject(
                    subject_id).first()
                all_question_obj.type = constants.MULTIPLE_IMAGE_CHOICE_QUESTION
                
                all_question_obj.save()

                add_question = MultipleImageChoiceQuestion()
                add_question.question_id = all_question_obj
                add_question.question_title = question_title.strip()
                add_question.optionA = optionA
                add_question.optionB = optionB
                add_question.optionC = optionC
                add_question.optionD = optionD

                if answer_key == 'optionA':
                    add_question.answer_key = add_question.optionA
                elif answer_key == 'optionB':
                    add_question.answer_key = add_question.optionB
                elif answer_key == 'optionC':
                    add_question.answer_key = add_question.optionC
                else:
                    add_question.answer_key = add_question.optionD

                add_question.question_id.subject.subject = subject
                add_question.created_by = queries.get_user_by_username(
                    request.user)
                add_question.save()

                messages.success(
                    request, return_message.MESSAGE['question_added']
                )
                return redirect('/multiple_img_choice_que')

            except Exception as e:
                all_question_obj.delete()
                messages.error(request, e)

        return redirect('/multiple_img_choice_que')
