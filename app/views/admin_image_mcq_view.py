import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.utility import queries, return_message, constants, question_module_functions
from app.forms.admin_image_mcq_form import ImageMcqSearchForm, ImageMcqSettingForm
from app.models import ImageMultipleChoiceQuestions, AllQuestions

@question_module_functions.superuser_required()
class ImageBasedMcqView(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        """ List view of image based mcq with search functionality and pagination"""
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        search_question = request.GET.get("question_title")
        search_subject = request.GET.get("subject")

        initial_dict = {
            "question_title": search_question,
            "subject": search_subject
        }

        search_form = ImageMcqSearchForm(initial=initial_dict)
        image_mcq_form = ImageMcqSettingForm()
        data = queries.get_image_mcq(search_question, search_subject)
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
                f"&question_title={search_question}&subject={search_subject}")

        context = {
            'query': query_params,
            'data': page_obj,
            'search_form': search_form,
            'image_mcq_form': image_mcq_form,
            'question_title': search_question,
            'subject': search_subject
        }
        return render(request, "admin_image_MCQ.html", context)
      
@question_module_functions.superuser_required()   
class ImageBasedMcqPostView(LoginRequiredMixin, BaseDetailView):
    def post(self, request, *args, **kwargs):
        """Post Delete and Edit functionality """
        method = request.POST.get('method')
        subject = request.POST.get('subjects')

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/admin_image_mcq')
        # getting subject instance for specified methods
        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/admin_image_mcq')
            except Exception as e:
                messages.error(request, e)
                return redirect('/admin_image_mcq')

        # checking special subjects should not be link with
        if question_module_functions.check_fixed_subjects(subject):
            messages.error(
                request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
            return redirect('/admin_image_mcq')

        question_title = request.POST.get('question_title')
        optionA = request.POST.get('optionA')
        optionB = request.POST.get('optionB')
        optionC = request.POST.get('optionC')
        optionD = request.POST.get('optionD')

        if question_module_functions.unique_options(optionA,optionB,optionC,optionD, method):
            messages.error(
                    request, return_message.MESSAGE['duplicate_options'])
            return redirect('/admin_image_mcq')
        
        answer_key = request.POST.get('AnswerKey')

        mcq_id = request.POST.get('mcq_id')
        upload_image = request.FILES.get('image_upload')

        if method:
            question_flag = True
            if not mcq_id:
                question_flag = False
            if question_flag:
                questions_data = queries.get_image_mcq_by_id(mcq_id)
                if questions_data is None:
                    question_flag = False
            if not question_flag:
                messages.error(
                    request, return_message.MESSAGE['content_not_found'])
                return redirect("/admin_image_mcq")
            all_question = queries.get_all_question_id(questions_data.question_id.id)
            if method == "put":
                """Update existing questions"""
                try:
                    all_question.subject = subject
                    all_question.save()

                    questions_data.question_title = question_title.strip()
                    questions_data.answer_key = question_module_functions.correct_ans(
                        answer_key, optionA, optionB, optionC, optionD)
                    questions_data.optionA = optionA.strip()
                    questions_data.optionB = optionB.strip()
                    questions_data.optionC = optionC.strip()
                    questions_data.optionD = optionD.strip()
                    questions_data.created_by = queries.get_user_by_username(
                        request.user)

                    if upload_image is not None:
                        questions_data.image = upload_image
                    questions_data.save()
                    messages.success(
                        request, return_message.MESSAGE['question_updated'])
                    return redirect("/admin_image_mcq")
                except IntegrityError as e:
                    messages.error(request, e)
                    return redirect("/admin_image_mcq")

            elif method == "delete":
                """Delete existing question data"""
                try:
                    all_question.delete()
                    messages.success(
                        request, return_message.MESSAGE['question_deleted'])
                    return redirect("/admin_image_mcq")
                except Exception as e:
                    messages.error(request, e)
                    return redirect("/admin_image_mcq")

        else:
            """save new questions"""
            try:
                all_question_obj = AllQuestions()
                all_question_obj.subject = subject
                all_question_obj.type = constants.IMAGE_MCQ
                all_question_obj.save()

                question_new = ImageMultipleChoiceQuestions()
                question_new.question_id = all_question_obj
                question_new.question_title = question_title.strip()
                question_new.answer_key = question_module_functions.correct_ans(
                    answer_key, optionA, optionB, optionC, optionD)
                question_new.optionA = optionA.strip()
                question_new.optionB = optionB.strip()
                question_new.optionC = optionC.strip()
                question_new.optionD = optionD.strip()
                question_new.question_id.subject.subject = subject
                question_new.created_by = queries.get_user_by_username(
                    request.user)

                question_new.image = upload_image

                question_new.save()
                messages.success(
                    request, return_message.MESSAGE['question_added'])
                return redirect("/admin_image_mcq")
            except Exception as e:
                all_question_obj.delete()
                messages.error(request, e)
                return redirect("/admin_image_mcq")
