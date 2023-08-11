from django.shortcuts import render, redirect
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

from app.models import SubjectiveQuestions, AllQuestions
from app.utility import queries, return_message, constants, question_module_functions
from app.forms import SubjectiveQuestionForm, SearchSubjectiveQuestions

@question_module_functions.superuser_required()
class SubjectiveQuestionsView(LoginRequiredMixin, BaseDetailView):
    def get(self, request, *args, **kwargs):
        """ List view of all users with search functionality and pagination"""
        page = request.GET.get("page", constants.DEFAULT_PAGE)
        search_subject = request.GET.get('question_id')
        search_question = request.GET.get('question_title')
        initial_dict = {
            "question_id": search_subject,
            "question": search_question
        }
        
        add_subjective_question_form = SubjectiveQuestionForm()
        search_subjective_question_form = SearchSubjectiveQuestions(
            initial=initial_dict)
        data = queries.get_subjective_questions(
            question_id=search_subject, question=search_question)
        if not data.exists():
            messages.error(
                request, return_message.MESSAGE['subjective_question_not_found'])
        paginator = Paginator(data, constants.PAGE_LIMIT)

        try:
            page_obj = paginator.page(page)
            page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page) 
        except (PageNotAnInteger, InvalidPage):
            page_obj = None
            messages.error(request, return_message.MESSAGE['no_data'])
        query_params = ""
        if (search_subject or search_question):
            query_params = (
                    f"&question_id={search_subject}&question_title={search_question}")
        context = {
            'query': query_params,
            'data': page_obj,
            'add_subjective_question_form': add_subjective_question_form,
            'search_subjective_question_form': search_subjective_question_form,
            "question_id": search_subject,
            "question_title": search_question
        }
        return render(request, "admin_subjective_questions.html", context)
    
@question_module_functions.superuser_required()
class AddSubjectiveQuestionsView(LoginRequiredMixin, BaseDetailView):
    def post(self, request, *args, **kwargs):
        user = queries.get_user_by_username(request.user)
        method = request.POST.get('method')
        subject = request.POST.get('subjects')
        
        #checking whether the method is valid or not
        if question_module_functions.method_not_allowed(method,request):
            return redirect('/subjective_questions')
        
        # getting subject instance for specified methods 
        if method in ['put', '']:
            try:
                subject = queries.get_subject(subject).first()
                if subject is None:
                    messages.error(
                        request, return_message.MESSAGE['subject_not_found'])
                    return redirect('/subjective_questions')     
            except Exception as e:
                messages.error(request, e)
                return redirect('/subjective_questions')
            
        # checking special subjects should not be link with   
        if question_module_functions.check_fixed_subjects(subject):
            messages.error(
                request, f"{return_message.MESSAGE['subject_link_error']} {subject}")
            return redirect('/subjective_questions')
        
        passage = request.POST.get('passage')
        if not passage:
            passage = None
        question = request.POST.get('question_title')
        answer_key = request.POST.get('answer_key')
        instructions = request.POST.get('instructions')
        subjectquestionsID = request.POST.get('subjectquestionsID')

        if method:
            subjective_questions_data_flag = True
            if not subjectquestionsID:
                subjective_questions_data_flag = False
            if subjective_questions_data_flag:
                subjective_questions_data = queries.get_subjective_questions_by_id(
                    id=subjectquestionsID).first()
                if subjective_questions_data is None:
                    subjective_questions_data_flag = False
            if not subjective_questions_data_flag:
                messages.error(
                    request, return_message.MESSAGE['subjective_question_not_found'])
                return redirect('/subjective_questions')

            all_question = queries.get_all_question_id(
                        subjective_questions_data.question_id.id)
            if method == "put":
                """Update existing subjective question"""
                question = question.strip()
                answer_key = answer_key.strip()
                instructions = instructions.strip()
                try:
                    all_question.subject = subject
                    all_question.save()

                    subjective_questions_data.created_by = user
                    subjective_questions_data.question_title = question
                    subjective_questions_data.answer_key = answer_key
                    subjective_questions_data.instructions = instructions
                    subjective_questions_data.passage = queries.get_passage_by_id(
                        passage)
                    subjective_questions_data.save()
                    messages.success(
                        request, return_message.MESSAGE['subjective_question_update'])
                    return redirect('/subjective_questions')
                except Exception as e:
                    messages.error(request, e)
                    return redirect('/subjective_questions')

            if method == "delete":
                try:
                    all_question.delete()
                    messages.success(
                        request, return_message.MESSAGE['subjective_question_deleted'])
                    return redirect('/subjective_questions')
                except Exception as e:
                    messages.error(request, e)
                    return redirect('/subjective_questions')

        else:
            '''Create new subjective question'''
            try:
                all_question_obj = AllQuestions()
                all_question_obj.subject = subject
                all_question_obj.type = constants.SUBJECTIVE_QUESTION
                all_question_obj.save()

                question_obj = SubjectiveQuestions()
                question_obj.question_id = all_question_obj
                question_obj.created_by = user
                question_obj.question_title = question.strip()
                question_obj.answer_key = answer_key.strip()
                question_obj.passage = queries.get_passage_by_id(passage)
                question_obj.instructions = instructions.strip()
                question_obj.save()
                messages.success(
                    request, return_message.MESSAGE['subjective_question_added'])

            except Exception as e:
                all_question_obj.delete()
                messages.error(request, e)
            return redirect('/subjective_questions')
