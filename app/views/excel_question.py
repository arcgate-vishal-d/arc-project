import os
import datetime
from datetime import timedelta
import pytz
from pytz import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.utility import (constants, queries, return_message,
                         question_module_functions)
from app.models import AllQuestions, ExcelQuestions
from app.forms import ExcelQuestionForm, ExcelImageForm
from app.ArcSheet.base_view import create_sheet, sheet_modified


@question_module_functions.superuser_required()
class ExcelQuestion(LoginRequiredMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", constants.DEFAULT_PAGE)

        data = queries.get_excel_question()
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data'])

        paginator = Paginator(data, constants.PAGE_LIMIT)
        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['invalid_page'])
        excel_form = ExcelQuestionForm()
        excel_image_form = ExcelImageForm()
        context = {
            "excel_form": excel_form,
            "excel_image_form": excel_image_form,
            'data': page_obj
        }
        return render(request, "admin_excel_questions.html", context)

    def post(self, request, *args, **kwargs):
        user = queries.get_user_by_username(request.user)
        method = request.POST.get('method')
        excel_title = request.POST.get('question_title')
        excel_description = request.POST.get('description')
        excel_id = request.POST.get('excel_id')
        subject = "Excel"

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/excel_question')

        # getting subject instance for specified methods
        subject = queries.get_subject_by_name(subject)

        if method:
            flag = True
            if not excel_id:
                flag = False
            if flag:
                excel_question = queries.get_excel_question(
                    excel_id).first()
                if excel_question is None:
                    flag = False
            if not flag:
                messages.error(request, return_message.MESSAGE['null_id'])
                return redirect('/excel_question')
            if method == "delete":
                '''Deleting an existing question'''
                try:
                    all_question = queries.get_all_question_id(
                        excel_question.question_id.id)
                    all_question.delete()
                    messages.success(
                        request, return_message.MESSAGE['question_deleted'])
                    return redirect('/excel_question')
                except Exception as e:
                    messages.error(request, e)
                    return redirect('/excel_question')
                   
            elif method == "put":
                try:
                    update_obj = ExcelQuestions.objects.filter(id=excel_id).first()
                    image = request.FILES.get('screenshot')
                    update_obj.screenshot = image
                    sheet_id = update_obj.sheet_id
                    modified_excel_dict = sheet_modified(sheet_id)
                    last_edited = (modified_excel_dict['modifiedTime'])
                    update_obj.excel_last_edited = last_edited
                    update_obj.save()
                    messages.success(
                        request, return_message.MESSAGE['question_update'])
                    return redirect('/excel_question')

                except Exception as e:
                    messages.error(request, e)
                    return redirect('/excel_question')

        else:
            '''Create new question'''
            try:
                if not excel_title:
                    messages.error(
                        request, return_message.MESSAGE['excel_without_title'])
                    return redirect('/excel_question')

                all_question_obj = AllQuestions()
                all_question_obj.subject = subject
                all_question_obj.type = constants.EXCEL_QUESTIONS
                all_question_obj.save()

                excel_obj = ExcelQuestions()
                excel_obj.question_id = all_question_obj
                excel_obj.created_by = user
                try:
                    excel_obj.sheet_id = create_sheet(excel_title)
                except Exception as e:
                    all_question_obj.delete()
                    messages.error(
                        request, return_message.MESSAGE['error_occur'])
                    return redirect('/excel_question')
                excel_obj.question_title = excel_title.strip()
                excel_obj.description = excel_description.strip()
                excel_obj.full_clean()
                excel_obj.save()
                messages.success(
                    request, return_message.MESSAGE['question_added'])
                return redirect('/excel_question')    
            except ValidationError as e:
                all_question_obj.delete()
                messages.error(request, e)
                return redirect('/excel_question')
