from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger

from app.forms.image_subjective_question_form import ImageSubjectiveQuestionForm, ImgSubjectiveQueSearchForm
from app .models import ImageBasedSubjectiveQuestions, AllQuestions
from app.utility import return_message, constants, queries, question_module_functions

@question_module_functions.superuser_required()
class ImageSubjectiveQuestionView(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        """ List view of all image based subjective questions with search functionality and pagination"""
        search_question = request.GET.get('question')
        search_subject = request.GET.get('subjects')
        initial_dict = {
            "question": search_question,
            "subjects": search_subject,
        }
        add_question_form = ImageSubjectiveQuestionForm()
        search_question_form = ImgSubjectiveQueSearchForm(initial=initial_dict)
        data = queries.get_image_subjective_question(
            search_question, search_subject)
        if not data.exists():
            messages.error(request, return_message.MESSAGE['no_data'])

        page = request.GET.get("page", constants.DEFAULT_PAGE)
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
                f"&question={search_question}&subject={search_subject}")
        context = {
            'query': query_params,
            'data': page_obj,
            'question_form': add_question_form,
            'search_form': search_question_form
        }

        return render(request, 'admin_Image_subjective_questions.html', context)

@question_module_functions.superuser_required()
class IBSQViews(LoginRequiredMixin, BaseDetailView):

    def post(self, request, *args, **kwargs):
        """This function contain Add, Update and Delete function of Image based subjective questions"""
        method = request.POST.get('method')
        subject_id = request.POST.get('subjects')

        if question_module_functions.method_not_allowed(method, request):
            return redirect('/img_subjective')

        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject_id).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/img_subjective')
            except Exception as e:
                messages.error(request, e)
                return redirect("/img_subjective")

            if question_module_functions.check_fixed_subjects(subject):
                messages.error(
                    request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
                return redirect('/img_subjective')

        question_title = request.POST.get('question_title')
        answer_key = request.POST.get('answer_key')
        upload_image = request.FILES.get('image_upload')
        question_id = request.POST.get('question_id')

        if method:
            question_flag = True
            if not question_id:
                question_flag = False
            if question_flag:
                question_data = queries.get_image_subjective_by_id(
                    question_id)
                if question_data is None:
                    question_flag = False
            if not question_flag:
                messages.error(request,
                               return_message.MESSAGE['question_not_found']
                               )
                return redirect("/img_subjective")

            all_question_obj = queries.get_all_question_id(question_data.question_id.id)
            if method == "put":
                """Update existing question"""
                try:
                    question_title = question_title.strip()
                    answer_key = answer_key.strip()

                    all_question_obj = AllQuestions()
                    all_question_obj.subject = queries.get_subject(
                        subject_id).first()
                    all_question_obj.type = constants.IMAGE_BASED_SUBJECTIVE_QUESTION
                    all_question_obj.save()

                    que_update = queries.get_image_subjective_by_id(
                        question_id)

                    que_update.question_title = question_title
                    que_update.answer_key = answer_key
                    que_update.question_id = all_question_obj
                    if upload_image is not None:
                        que_update.image = upload_image

                    que_update.save()
                    messages.success(request,
                                     return_message.MESSAGE['question_update']
                                     )
                    return redirect("/img_subjective")

                except Exception as e:
                    messages.error(request, e)
                    return redirect("/img_subjective")

            elif method == "delete":
                """Delete existing question"""
                try:
                    all_question_obj.delete()
                    messages.success(request,
                                     return_message.MESSAGE['question_deleted']
                                     )
                    return redirect("/img_subjective")

                except Exception as e:
                    messages.error(request, e)
                    return redirect("/img_subjective")

        else:
            """Add new questions"""
            try:
                question_title = question_title.strip()
                answer_key = answer_key.strip()

                add_question = ImageBasedSubjectiveQuestions()
                user_instance = queries.get_user_by_username(request.user)

                all_question_obj = AllQuestions()
                all_question_obj.subject = queries.get_subject(
                    subject_id).first()
                all_question_obj.type = constants.IMAGE_BASED_SUBJECTIVE_QUESTION
                all_question_obj.save()

                add_question.created_by = user_instance
                add_question.question_title = question_title
                add_question.answer_key = answer_key
                add_question.question_id = all_question_obj
                add_question.image = upload_image

                add_question.save()
                messages.success(request,
                                 return_message.MESSAGE['question_added']
                                 )

            except Exception as e:
                all_question_obj.delete()
                messages.error(request, e)

            return redirect("/img_subjective")
