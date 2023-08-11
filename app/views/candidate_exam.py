import os
import random
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.detail import BaseDetailView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from app import models
from app.utility import queries, constants, candidate_module_function
from app.ArcSheet import base_view


@method_decorator(never_cache, name="dispatch")
class CandidateExam(BaseDetailView):
    
    def get(self, request, *args, **kwargs):
        try:
            current_question = request.session['current_question']
        except:
            current_question = None

        update_question_id = request.GET.get("uid")
        new_duration = request.GET.get('hdnDurationget')
        attempted_ques_num = request.GET.get("ques_num")

        update_question_dict = {}
        if update_question_id:
            candidate_id_new = request.session['candidate_id']
            candidate_timer = models.CandidateDetails.objects.filter(
                id=candidate_id_new).first()
            # time penalty
            if float(candidate_timer.timer) < float(new_duration):
                candidate_timer.timer = float(candidate_timer.timer) - 1
            else:
                candidate_timer.timer = str(new_duration)
            candidate_timer.save()
            all_question_obj = queries.get_all_question_id(update_question_id)
            if all_question_obj.type == constants.IMAGE_MCQ:
                question_obj = queries.get_image_multiple_choice_question_by_allquestion_id(all_question_obj.id)
                update_question_dict[all_question_obj.subject] = [question_obj]
            if all_question_obj.type == constants.MULTIPLE_CHOICE_QUESTION:
                question_obj = queries.get_multiple_choice_question_by_allquestion_id(all_question_obj.id)
                update_question_dict[all_question_obj.subject] =  [question_obj]
            if all_question_obj.type == constants.SUBJECTIVE_QUESTION:
                question_obj = queries.get_subjectitve_question_by_allquestion_id(all_question_obj.id)
                update_question_dict[all_question_obj.subject] =  [question_obj]
            if all_question_obj.type == constants.IMAGE_BASED_SUBJECTIVE_QUESTION:
                question_obj = queries.get_image_subjectitve_question_by_allquestion_id(all_question_obj.id)
                update_question_dict[all_question_obj.subject] =  [question_obj]
            if all_question_obj.type == constants.MULTIPLE_IMAGE_CHOICE_QUESTION:
                question_obj = queries.get_multi_image_choice_question_by_allquestion_id(all_question_obj.id)
                update_question_dict[all_question_obj.subject] =  [question_obj]
        try:
            candidate_id_new = request.session['candidate_id']
            candidate_level = queries.get_candidate_details_by_id(candidate_id_new).first().test_level
            candidate_paper_set = models.PaperHistory.objects.filter(
                paper_set__test_level__test_level=candidate_level).last().paper_set

            # exam timer variable
            candidate_timer = queries.get_candidate_details_by_id(candidate_id_new).first()
            db_time = round(queries.get_candidate_details_by_id(candidate_id_new).first().timer, 2)
            diff = candidate_module_function.time_refresh(request)
            str_time_passes = diff / 60
            new_time = db_time - str_time_passes
            candidate_timer.timer = new_time
            candidate_timer.save()

            timer = queries.get_candidate_details_by_id(candidate_id_new).first().timer
            paper_id = candidate_paper_set.id
            paper_subjects = queries.get_paper_subject_map_by_paper_id(
                paper_id)

            # creating list of candidate attempted questions
            attempted_questions_query_set = queries.get_candidate_individual_result_Cid_PaperSetId(candidate_id_new,paper_id).all()
            attempted_question_dict = {}
            attempted_question_all_question_list = []
            for attempt_question in attempted_questions_query_set:
                attempt_question_type = attempt_question.subject_question_id.all_question_id.type
            
                if attempt_question_type == constants.IMAGE_MCQ:
                    attempted_question_all_question_list.append(queries.get_image_multiple_choice_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id).question_id)
                    attempted_question_dict[attempt_question] = (
                        queries.get_image_multiple_choice_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id))

                if attempt_question_type == constants.MULTIPLE_CHOICE_QUESTION:
                    attempted_question_all_question_list.append(queries.get_multiple_choice_question_by_allquestion_id(
                        attempt_question.subject_question_id.all_question_id).question_id)
                    attempted_question_dict[attempt_question] = (queries.get_multiple_choice_question_by_allquestion_id(
                        attempt_question.subject_question_id.all_question_id))

                if attempt_question_type == constants.SUBJECTIVE_QUESTION:
                    attempted_question_all_question_list.append(queries.get_subjectitve_question_by_allquestion_id(
                        attempt_question.subject_question_id.all_question_id).question_id)
                    attempted_question_dict[attempt_question] = (queries.get_subjectitve_question_by_allquestion_id(
                        attempt_question.subject_question_id.all_question_id))

                if attempt_question_type == constants.IMAGE_BASED_SUBJECTIVE_QUESTION:
                    attempted_question_all_question_list.append(queries.get_image_subjectitve_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id).question_id)
                    attempted_question_dict[attempt_question] = (
                        queries.get_image_subjectitve_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id))

                if attempt_question_type == constants.MULTIPLE_IMAGE_CHOICE_QUESTION:
                    attempted_question_all_question_list.append(queries.get_multi_image_choice_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id).question_id)
                    attempted_question_dict[attempt_question] = (
                        queries.get_multi_image_choice_question_by_allquestion_id(
                            attempt_question.subject_question_id.all_question_id))
            
            # when all questions are attempted 
            total_questions = 0
            for subject in paper_subjects:
                total_questions += subject.subject_questions
            candidate_attempted = queries.get_model_by_candidate_id(models.CandidateResultIndividual,candidate_id_new).all()

            if len(candidate_attempted) == total_questions:
                return redirect("/thank_you")

            paper_data = {}
            sheet_id = None
            for subject in paper_subjects:
                subject_question = []
                for question in queries.get_subject_question_data_paper_by_id(paper_id, subject):
                    subjective_question = queries.get_subjectitve_question_by_allquestion_id(
                        question.all_question_id.id)
                    if subjective_question:
                        subject_question.append(subjective_question)

                    image_based_subjective = queries.get_image_subjectitve_question_by_allquestion_id(
                        question.all_question_id.id)
                    if image_based_subjective:
                        subject_question.append(image_based_subjective)

                    image_based_mcq = queries.get_image_multiple_choice_question_by_allquestion_id(
                        question.all_question_id.id)
                    if image_based_mcq:
                        subject_question.append(image_based_mcq)

                    multiple_choice_question = queries.get_multiple_choice_question_by_allquestion_id(
                        question.all_question_id.id)
                    if multiple_choice_question:
                        subject_question.append(multiple_choice_question)

                    excel_question = queries.get_excel_question_by_allquestion_id(
                        question.all_question_id.id)
                    if excel_question:
                        subject_question.append(excel_question)
                        sheet_id = queries.get_candidate_details_by_id(candidate_id_new).first().sheet_id
                        base_view.make_sheet_public(sheet_id)
                    passage_question = queries.get_passage_question_by_allquestion_id(
                        question.all_question_id.id)
                    if passage_question:
                        subject_question.append(passage_question)

                    multi_image = queries.get_multi_image_choice_question_by_allquestion_id(
                        question.all_question_id.id)
                    if multi_image:
                        subject_question.append(multi_image)

                paper_data[subject] = subject_question
            #  non internet questions count
            non_internet_questions = 0
            number_of_attempt_question = queries.get_model_by_candidate_id(models.CandidateResultIndividual,candidate_id_new).all().count() + 1

            for subject,quesions in paper_data.items():
                if str(subject.subject) not in ["Excel","Typing Test"]:
                    non_internet_questions += int(subject.subject_questions)


            # random question + required no. of questions only
            random_generated_question = {}
            for subject, questioin_list in paper_data.items():
                attemp_ques_objects = queries.get_candidate_individual_result_Cid_paperSubjectID(candidate_id_new, subject).all()

                if subject.subject_questions == attemp_ques_objects.count():
                    continue

                if subject.subject_questions > attemp_ques_objects.count():
                    repeat_counter = True
                    while repeat_counter:

                        random_generated_question[subject] = random.sample(
                            questioin_list, 1)

                        # converting attempt questions objects to list
                        attempted_question_list = []
                        for attempted_question in attemp_ques_objects:
                            attempted_question_list.append(
                                attempted_question.subject_question_id.all_question_id)

                        # preventing the attempted question to render again
                        if random_generated_question[subject][0].question_id not in attempted_question_list:
                            # to fix the last question
                            if not current_question:
                                request.session['current_question'] = random_generated_question[subject][0].question_id.id
                            repeat_counter = False
                break


            candidate_status = queries.get_candidate_details_by_id(candidate_id_new).first().status
            if candidate_status <= 5:
                return redirect('/candidate_other_details') 
            
            # once generated random question can't be changed
            if current_question:
                for i in random_generated_question:
                    all_question_obj = queries.get_all_question_id(current_question)
                    if all_question_obj.type == constants.IMAGE_MCQ:
                        question_obj = queries.get_image_multiple_choice_question_by_allquestion_id(all_question_obj.id)
                        random_generated_question[i] = [question_obj]
                    if all_question_obj.type == constants.MULTIPLE_CHOICE_QUESTION:
                        question_obj = queries.get_multiple_choice_question_by_allquestion_id(all_question_obj.id)
                        random_generated_question[i] = [question_obj]
                    if all_question_obj.type == constants.SUBJECTIVE_QUESTION:
                        question_obj = queries.get_subjectitve_question_by_allquestion_id(all_question_obj.id)
                        random_generated_question[i] = [question_obj]
                    if all_question_obj.type == constants.IMAGE_BASED_SUBJECTIVE_QUESTION:
                        question_obj = queries.get_image_subjectitve_question_by_allquestion_id(all_question_obj.id)
                        random_generated_question[i] = [question_obj]
                    if all_question_obj.type == constants.MULTIPLE_IMAGE_CHOICE_QUESTION:
                        question_obj = queries.get_multi_image_choice_question_by_allquestion_id(all_question_obj.id)
                        random_generated_question[i] = [question_obj]

            context = {
                "candidate_paper_id": paper_id,
                "dict": random_generated_question,
                "atmpt":attempted_question_all_question_list,
                "timer": timer,
                "number_of_attempted_question":number_of_attempt_question,
                "non_internet_questions": non_internet_questions

            }
            if attempted_ques_num:
                context['ques_number'] = attempted_ques_num
            if update_question_dict:
                context["dict"] = update_question_dict
            if sheet_id:
                context['sheet_id'] = sheet_id

            attemp_subject_question = {}
            for i in paper_data:
                attempt_question = queries.get_candidate_individual_result_Cid_paperSubjectID(candidate_id_new, i).all().count()
                attemp_subject_question[i] = attempt_question
            context['attempt'] = attemp_subject_question
            selected_question = list(random_generated_question)[0]
            question_type = (
                random_generated_question[selected_question][0].question_id.type)


                # attempted_question_list.append(queries.)
            context["attempt_questions"] = attempted_question_dict
            if question_type in constants.REVIEWABEL_QUESTION_TYPES:
                return render(request, "candidate_exam_with_extra_column.html", context)
            if question_type in constants.NON_REVIEWABLE_QUESTION_TYPES:
                return render(request, "candidate_exam.html", context)

        except Exception as e:
            print(e)
            return redirect('/interview_homepage')

    def post(self, request, *args, **kwargs):
        candidate_id_new = request.session['candidate_id']

        new_duration = request.POST.get('hdnDuration')
        candidate_paper_id = request.POST.get("candidate_paper_id")
        question_id = request.POST.get('selectedQuestionID')
        candidate_answer = request.POST.get('txtAnswer')
        question_type = request.POST.get('QuestionType')
        subject = queries.get_model_by_allQuestionId(models.SubjectQuestionMap, question_id).first().paper_setup_subject_id.subject
        candidate_subject = queries.get_paper_setup_subject_map_by_subject_paperSetId(subject, candidate_paper_id).first()
        candidate_subject_question = queries.get_model_by_allQuestionId(models.SubjectQuestionMap, question_id).first()
        candidate_timer = queries.get_candidate_details_by_id(candidate_id_new).first()
        candidate_timer.timer = new_duration
        candidate_timer.save()

        candidate_result = models.CandidateResultIndividual.objects.filter(candidate=candidate_id_new,subject_question_id__all_question_id=question_id).first()
        if not candidate_result:
            candidate_result = models.CandidateResultIndividual()
        candidate_result.candidate = queries.get_candidate_details_by_id(candidate_id_new).first()

        candidate_result.paper_set_id = queries.get_paper_setup_description_by_id(
            candidate_paper_id)
        candidate_result.candidate_answer = candidate_answer
        candidate_result.subject_question_id = candidate_subject_question
        candidate_result.paper_subject_id = candidate_subject
        # marks per question based on subject
        total_question = candidate_subject.subject_questions
        question_mark = candidate_subject.subject_marks/total_question

        # skipped questions
        if candidate_answer is None and question_type != constants.EXCEL_QUESTIONS:
            candidate_result.answer_marks = 0
            candidate_result.candidate_answer = ""
            candidate_result.save()

        if question_type == constants.MULTIPLE_CHOICE_QUESTION:
            question = queries.get_multiple_choice_question_by_allquestion_id(
                question_id)
            if candidate_answer == question.answer_key:
                candidate_result.answer_status = constants.CORRECT
                candidate_result.answer_marks = question_mark
            else:
                candidate_result.answer_marks = 0
            candidate_result.save()

        if question_type == constants.IMAGE_BASED_SUBJECTIVE_QUESTION:
            question = queries.get_image_subjectitve_question_by_allquestion_id(
                question_id)
            if candidate_answer.lower() == question.answer_key.lower():
                candidate_result.answer_status = constants.CORRECT
                candidate_result.answer_marks = question_mark
            else:
                candidate_result.answer_marks = 0
            candidate_result.save()

        if question_type == constants.MULTIPLE_IMAGE_CHOICE_QUESTION:
            question = queries.get_multi_image_choice_question_by_allquestion_id(
                question_id)
            if candidate_answer == None:
                candidate_result.answer_marks = 0
            elif candidate_answer[7:] == question.answer_key:
                candidate_result.answer_status = constants.CORRECT
                candidate_result.answer_marks = question_mark
            else:
                candidate_result.answer_marks = 0
            candidate_result.save()

        if question_type == constants.IMAGE_MCQ:
            question = queries.get_image_multiple_choice_question_by_allquestion_id(
                question_id)
            if candidate_answer == question.answer_key:
                candidate_result.answer_status = constants.CORRECT
                candidate_result.answer_marks = question_mark
            else:
                candidate_result.answer_marks = 0
            candidate_result.save()

        if question_type == constants.SUBJECTIVE_QUESTION:
            question = queries.get_subjectitve_question_by_allquestion_id(
                question_id)
            if candidate_answer.lower() == question.answer_key.lower():
                candidate_result.answer_status = constants.CORRECT
                candidate_result.answer_marks = question_mark
            else:
                candidate_result.answer_marks = 0
            candidate_result.save()

        # typing test
        if question_type == 'Passage/Instruction':
            end_time = request.POST.get("endgame")
            start_time = request.POST.get("start")
            if start_time == "":
                start_time = 0
            question = queries.get_passage_question_by_allquestion_id(
                question_id)
            typing_test = candidate_module_function.typing_test(
                question.description, candidate_answer, end_time, start_time)
            accuracy = round(typing_test[0],2)
            speed = round(typing_test[1], 2)
            candidate_result.answer_status = constants.CORRECT
            candidate_result.candidate_answer = f"{speed}{' speed|accuracy '}{accuracy}"
            candidate_result.answer_marks = accuracy
            candidate_result.save()

        if question_type == constants.EXCEL_QUESTIONS:
            # sheet id of user
            sheet_id = request.POST.get("sheet_id")
            exam_sheet_id = request.POST.get("exam_sheet_id")
            get_sheet_user = base_view.get_sheet_data(sheet_id)
            get_sheet_hr = base_view.get_sheet_data(exam_sheet_id)
            marks = base_view.evaluate_results(get_sheet_hr, get_sheet_user)
            candidate_result.answer_status = constants.CORRECT
            candidate_result.candidate_answer = sheet_id
            candidate_result.answer_marks = marks
            candidate_result.save()
            base_view.make_sheet_private(sheet_id)

            profile_status = queries.get_candidate_details_by_id(candidate_id_new).first()
            profile_status.status = 7
            profile_status.save() 
        try:
            if request.session['current_question']:
               del request.session['current_question']
        except:
            return redirect("/exam")
        return redirect("/exam")
