from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app import models
from app.utility import constants, return_message, queries, question_module_functions
from app.forms import GradeForms

@question_module_functions.admin_required()
class PaperSetup(LoginRequiredMixin, BaseDetailView):
    """Get paper setup panel"""

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        grade_form = GradeForms()
        data_grade = queries.get_grades()
        data = queries.get_paper_description()
        subject_data = queries.get_subject()
        test_level = queries.get_test_level()

        edit_paper_id = request.GET.get('paperID')
        edit_paper_data = queries.get_paper_setup_description_by_id(edit_paper_id)
        paper_subjects_data = queries.get_paper_subject_map_by_paper_id(edit_paper_id)
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data'])

        paginator = Paginator(data, constants.PAGE_LIMIT)
        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['invalid_page'])

        context = {
            'data': page_obj,
            'exist_data': data,
            'subject_data': subject_data,
            'test_levels': test_level,
            'grade_form': grade_form,
            'grade_data': data_grade,
        }
        if edit_paper_data:
            context['edit_paper_data'] = edit_paper_data
            context['paper_subjects_data'] = paper_subjects_data
            context['edit_paper_id'] = edit_paper_id

        return render(request, "admin_paper_setup.html", context)

@question_module_functions.admin_required()
class PaperSetupPost(LoginRequiredMixin, BaseDetailView, UpdateView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        paper_id = request.POST.get('paperID')
        department = request.POST.get('SelectedDepartmentID')
        paper_title = request.POST.get('PaperSetName')
        paper_description = request.POST.get('Descriptions')
        paper_marks = request.POST.get('TotalMarks')
        paper_time = request.POST.get('TotalTime')
        test_level_id = request.POST.get('test_level_id')

        if method == "delete":
            try:
                delete_paper = queries.get_paper_setup_description_by_id(
                    paper_id)
                delete_paper.delete()
                messages.success(
                    request, return_message.MESSAGE['paper_deleted'])
                return redirect('/paper_setup')
            except Exception as e:
                messages.error(request, e)
                return redirect('/paper_setup')

        else:
            try:
                """post method"""
                if not paper_id:
                    paper_desc_obj = models.PaperSetupDescription()
                else:
                    paper_desc_obj = queries.get_paper_setup_description_by_id(paper_id)

                paper_desc_obj.department = department
                paper_desc_obj.paper_title = paper_title
                paper_desc_obj.paper_description = paper_description
                paper_desc_obj.paper_marks = paper_marks
                paper_desc_obj.paper_time = paper_time
                paper_desc_obj.test_level = queries.get_test_level_by_id(
                    test_level_id).first()

                # save paper only when a subject is checked
                if request.POST.getlist('subject_chk') == []:
                    messages.error(
                        request, return_message.MESSAGE['Select_subject'])
                    return redirect('/paper_setup')
                    
                else:
                    paper_desc_obj.save()

                selected_subject = request.POST.getlist('subject_chk')
                map_strings = []
                if paper_id:
                    existing_paper_subject = queries.get_paper_subject_map_by_paper_id(
                        paper_id)

                    for map in existing_paper_subject:
                        map_string = (
                            f"{map.paper_setup_id.id},{map.subject.id}")
                        map_strings.append(map_string)
                        if map_string not in selected_subject:
                            map.delete()

                for selected in selected_subject:
                    single_subject = selected.split(',')
                    subject_id = int(single_subject[1])
                    if selected not in map_strings:
                        subject_id = request.POST.get(
                            f'subject_title_{subject_id}')
                        paper = models.PaperSetupSubjectMap()
                        paper.paper_setup_id = paper_desc_obj
                        paper.subject_questions = request.POST.get(
                            f'subject_questions_{subject_id}')
                        paper.subject_marks = request.POST.get(
                            f'subject_marks_{subject_id}')
                        paper.subject = queries.get_subject(
                            id=subject_id).first()
                        paper.subject_time = request.POST.get(
                            f'subject_time_{subject_id}')
                        paper.subject_order = request.POST.get(
                            f'subject_order_{subject_id}')
                        paper.save()
                    else:
                        existing_paper = queries.get_paper_subject_map_by_paper_id_subject_id(paper_id, subject_id)
                        existing_paper.subject_questions = request.POST.get(f'subject_questions_{subject_id}')
                        existing_paper.subject_order = request.POST.get(f'subject_order_{subject_id}')
                        existing_paper.subject_marks = request.POST.get(f'subject_marks_{subject_id}')
                        existing_paper.subject_time = request.POST.get(f'subject_time_{subject_id}')
                        existing_paper.save()

                messages.success(
                    request, return_message.MESSAGE['task_completed'])
                return redirect(f'/paper_setup_details/paper/{paper_desc_obj.id}')
            
            except Exception as e:
                messages.error(request, e)

                return redirect('/paper_setup')

@question_module_functions.admin_required()
class PaperSetupRequestView(LoginRequiredMixin, BaseDetailView):
    """Grade post delete view"""

    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        grade_id = request.POST.get('grade_id')
        grade_title = request.POST.get('grade')
        grade_from = request.POST.get('from_field')
        grade_to = request.POST.get('to_field')

        # checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method, request):
            return redirect('/paper_setup')

        if method:
            flag = True
            if not grade_id:
                flag = False
            if flag:
                excel_question = queries.get_grades(grade_id).first()
                if excel_question is None:
                    flag = False
            if not flag:
                messages.error(request, return_message.MESSAGE['null_id'])
                return redirect('/paper_setup')

        if method == 'delete':
            try:
                grade_instance = queries.get_grades(grade_id)
                grade_instance.delete()
                messages.success(
                    request, return_message.MESSAGE['grade_deleted'])
                return redirect("/paper_setup")
            except Exception as e:
                messages.error(request, e)

        else:
            try:
                for grd in queries.get_grades():
                    if grd.grade_from <= float(grade_from) <= grd.grade_to:
                        messages.error(
                            request, f'{return_message.MESSAGE["grade_exist"]} {grd.title}')
                        return redirect('/paper_setup')
                    if grd.grade_from <= float(grade_to) <= grd.grade_to:
                        messages.error(
                            request, f'{return_message.MESSAGE["grade_exist"]} {grd.title}')
                        return redirect('/paper_setup')
                    if float(grade_to) > 100.00:
                        messages.error(
                            request, f'{return_message.MESSAGE["grade_range"]} {grd.title}')
                        return redirect('/paper_setup')
                grade_obj = models.Grades()
                grade_obj.title = grade_title
                grade_obj.grade_from = grade_from
                grade_obj.grade_to = grade_to
                grade_obj.save()
                messages.success(request, return_message.MESSAGE['grade_add'])

            except Exception as e:
                messages.error(request, e)

            return redirect("/paper_setup")
