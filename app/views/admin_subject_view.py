from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

from app.models.subjects import Subjects
from app.utility import queries, return_message, constants, question_module_functions
from app.forms import SubjectForm

@question_module_functions.superuser_required()
class SubjectView(LoginRequiredMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        """ Show data using pagination"""
        add_subject_form = SubjectForm()
        Subject = queries.get_subject().all()
        paginator = Paginator(Subject, constants.PAGE_LIMIT)
        page = request.GET.get('page', constants.DEFAULT_PAGE)
        try:
            Subject_data = paginator.page(page)
            Subject_data.adjusted_elided_pages = paginator.get_elided_page_range(page)
        except (PageNotAnInteger, InvalidPage):
            Subject_data = None
            messages.error(request, return_message.MESSAGE['invalid_page'])
            
        context = {
            'add_subject_form': add_subject_form,
            'data': Subject_data,
            'page': page,
        }
        return render(request, 'admin_subject.html', context)

    def post(self, request, *args, **kwargs):
        """New Subject add"""
        method = request.POST.get('method')
        subjectId = request.POST.get('subjectID')
        subject_text = request.POST.get('subject')

        if method:
            update_subject_flag = True
            if not subjectId:
                update_subject_flag = False
            if update_subject_flag:
                update_subject = queries.get_subject(id=subjectId).first()
                if update_subject is None:
                    update_subject_flag = False
            if not update_subject_flag:
                messages.error(request, return_message.MESSAGE['subject_not_found'])
                return redirect('/subject')

            if method == "put":
                """Update existing subject"""
                try:
                    update_subject_data = subject_text.strip()
                    update_subject.subject = update_subject_data 
                    update_subject.created_by = queries.get_user_by_username(
                        request.user)
                    update_subject.save()
                    messages.success(
                        request, return_message.MESSAGE['subject_update'])
                    return redirect("/subject")

                except Exception as e:
                    messages.error(request, e)
                    return redirect("/subject")

            elif method == "delete":
                """Delete existing subject"""
                try:
                    update_subject.delete()
                    messages.success(
                        request, return_message.MESSAGE['subject_deleted'])
                    return redirect('/subject')
                except Exception as e:
                    messages.error(request, e)

        else:
            try:
                subject_data = Subjects()
                subject_data_value = subject_text.strip()
                subject_data.subject = subject_data_value
                subject_data.created_by = queries.get_user_by_username(
                    request.user)
                if queries.get_subject(subject_value=subject_data_value).first():
                    messages.error(
                        request, return_message.MESSAGE['subject_exists'])
                    return redirect('/subject')
                subject_data.save()
                messages.success(
                    request, return_message.MESSAGE['subject_added'])
                return redirect("/subject")

            except Exception as e:
                messages.error(request, e)
                return redirect('/subject')
