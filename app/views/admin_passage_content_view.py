import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.utility import queries, return_message, constants, question_module_functions
from app.forms.admin_passage_content_form import PassageContentSearchForm, PassageSettingForm
from app.models import PassageInstructionContents, AllQuestions

@question_module_functions.superuser_required()
class PassageContentView(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        """ List view of all users with search functionality and pagination"""
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        search_types = request.GET.get("types")
        search_title = request.GET.get("question_title")
        initial_dict = {
            "types": search_types,
            "title": search_title
        }
        search_form = PassageContentSearchForm(initial=initial_dict)
        passage_form = PassageSettingForm()

        data = queries.get_passage(search_types, search_title)
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
        if (search_types or search_title):
            query_params = (
                f"&types={search_types}&title={search_title}")

        context = {
            'query': query_params,
            'data': page_obj,
            'search_form': search_form,
            'passage_form': passage_form,
            'types': search_types,
            'title': search_title
        }
        return render(request, "admin_passage_content.html", context)

@question_module_functions.superuser_required()
class PassageContentPOSTView(LoginRequiredMixin, BaseDetailView):
    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/passage_content')

        types = request.POST.get('types')
        title = request.POST.get('question_title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        subject = request.POST.get('subjects')

        # getting subject instance for specified methods
        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/passage_content')
            except Exception as e:
                messages.error(request, e)
                return redirect('/passage_content')

        #Type typing link with typing test
        if types == constants.TYPING and str(subject) != constants.TYPING_TEST:
            messages.error(
                    request, f"{return_message.MESSAGE['typing_test_type']} {subject}")
            return redirect('/passage_content')

        # checking special subjects should not be link with
        if types != constants.TYPING:
            if question_module_functions.check_fixed_subjects(subject):
                messages.error(
                    request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
                return redirect('/passage_content')

        passageID = request.POST.get('passageID')

        # Handling content type error
        if question_module_functions.check_fixed_types(types):
            messages.error(
                request, f"{types} {return_message.MESSAGE['content_type_error']} ")
            return redirect('/passage_content')

        if method:
            passage_flag = True
            if not passageID:
                passage_flag = False
            if passage_flag:
                content_data = queries.get_passage_by_id(passageID)
                if content_data is None:
                    passage_flag = False
            if not passage_flag:
                messages.error(
                    request, return_message.MESSAGE['content_not_found'])
                return redirect("/passage_content")

            all_question = queries.get_all_question_id(
                content_data.question_id.id)
            if method == "put":
                """Update existing contents"""
                title = title.strip()
                description = description.strip()
                try:
                    all_question.subject = subject
                    all_question.save()

                    content_data.types = types
                    content_data.question_title = title
                    content_data.description = description
                    content_data.status = status
                    content_data.created_by = queries.get_user_by_username(
                        request.user)
                    content_data.save()
                    messages.success(
                        request, return_message.MESSAGE['content_updated'])
                    return redirect("/passage_content")

                except IntegrityError as e:
                    messages.error(
                        request, return_message.MESSAGE['content_exist'])
                    return redirect("/passage_content")

            elif method == 'delete':
                """Delete existing content data"""
                try:
                    all_question.delete()
                    messages.success(
                        request, return_message.MESSAGE['content_deleted'])
                    return redirect("/passage_content")
                except Exception as e:
                    messages.error(request, e)
                    return redirect("/passage_content")

        else:
            """ save new content"""
            try:
                all_question_obj = AllQuestions()
                all_question_obj.subject = subject
                all_question_obj.type = constants.PASSAGE_INSTRUCTION
                all_question_obj.save()

                content_new = PassageInstructionContents()
                title = title.strip()
                content_new .question_id = all_question_obj
                description = description.strip()
                content_new.types = types
                content_new.question_title = title
                content_new.description = description
                content_new.status = status
                content_new.created_by = queries.get_user_by_username(
                    request.user)
                if queries.get_passage_by_title(title):
                    messages.error(
                        request, return_message.MESSAGE['content_exist'])
                    return redirect('/passage_content')
                content_new.save()
                messages.success(
                    request, return_message.MESSAGE['content_added'])
                return redirect("/passage_content")

            except Exception as e:
                messages.error(request, e)
                return redirect('/passage_content')
