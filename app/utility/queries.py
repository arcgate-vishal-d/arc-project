from django.contrib.auth.models import User
from app import models
from typing import Optional
from app.utility import constants


def sort_order(order=constants.MODIFIED, desc=True):
    """ Generic function to change the sort order of queries """
    return f"-{order}" if desc else order


def get_all_user(username: str, email: str, role: str):
    """ Query to get all users """
    query_set = User.objects
    if username:
        query_set = query_set.filter(username__icontains=username)
    if email:
        query_set = query_set.filter(email__icontains=email)
    if role:
        if role == constants.ADMINISTRATOR:
            superuser = True
            staff = True
        elif role == constants.ADMIN:
            superuser = False
            staff = True
        elif role == constants.INTERVIEWER:
            superuser = False
            staff = False
        query_set = query_set.filter(is_superuser=superuser, is_staff=staff)
    return query_set.all().order_by(sort_order(constants.DATE_JOINED))


def get_user_by_id(id: int):
    """ Query to get user by id """
    return User.objects.filter(id=id).first()


def get_user_by_username(username: str):
    """ Query to get user by username """
    return User.objects.filter(username=username).first()


def get_subject(id: int = None, subject_value: str = None):
    """ Query for indivisual subject"""
    query_set = models.Subjects.objects
    if id:
        query_set = query_set.filter(id=id)
    if subject_value:
        query_set = query_set.filter(subject=subject_value)
    return query_set.order_by(sort_order())


def get_image_subjective_question(question: str, subject: int):
    """ Search question query"""
    query_set = models.ImageBasedSubjectiveQuestions.objects
    if question:
        query_set = query_set.filter(question_title__icontains=question)
    if subject:
        query_set = query_set.filter(question_id__subject=subject)
    return query_set.order_by(sort_order())


def get_image_subjective_by_id(id: int):
    """Get question instance by it's id"""
    return models.ImageBasedSubjectiveQuestions.objects.filter(id=id).first()


def get_multiple_choice_question(question: str, subject: int):
    """Query for all multiple choice question data and search"""
    query_set = models.MultipleChoiceQuestions.objects
    if question:
        query_set = query_set.filter(question_title__icontains=question)
    if subject:
        query_set = query_set.filter(question_id__subject=subject)
    return query_set.all().order_by(sort_order())


def get_candidate_result_and_interviewer(from_date, to_date):
    query_set = models.CandidateDetails.objects
    if (from_date == to_date) and from_date is not None and to_date is not None:
        query_set = query_set.filter(created__contains = from_date)
    else:
        if from_date:
            query_set = query_set.filter(created__gte=from_date)
        if to_date:
            query_set = query_set.filter(created__lte=to_date)
    return query_set.all().order_by(sort_order())


def get_multiple_choice_question_by_id(mcq_id: int):
    '''Query to get single MCQ by id'''
    return models.MultipleChoiceQuestions.objects.filter(id=mcq_id).first()


def get_passage(types: str, title: str):
    """ Query for passage data """
    query_set = models.PassageInstructionContents.objects
    if types:
        query_set = query_set.filter(types=types)
    if title:
        query_set = query_set.filter(question_title__icontains=title)
    return query_set.all().order_by(sort_order())


def get_passage_by_id(id: int):
    """Get passage by it's id"""
    return models.PassageInstructionContents.objects.filter(id=id).first()


def get_passage_by_title(title: str):
    """Get passage by it's title"""
    return models.PassageInstructionContents.objects.filter(question_title=title).first()


def get_image_mcq(question_title: str, subject: str):
    """ Query for all image based mcq data"""
    query_set = models.ImageMultipleChoiceQuestions.objects
    if question_title:
        query_set = query_set.filter(question_title__icontains=question_title)
    if subject:
        query_set = query_set.filter(question_id__subject=subject)
    return query_set.all().order_by(sort_order())


def get_image_mcq_by_id(id: int):
    """Get image based multiple question instance by it's id"""
    return models.ImageMultipleChoiceQuestions.objects.filter(id=id).first()


def get_all_question_id(id: int):
    """Query for updating subject with the help of question id"""
    return models.AllQuestions.objects.filter(id=id).first()


def get_subjective_questions(question_id: Optional[int], question: Optional[str]):
    """Search filter query for question and subject"""
    query_set = models.SubjectiveQuestions.objects
    if question_id:
        query_set = query_set.filter(question_id__subject=question_id)
    if question:
        query_set = query_set.filter(question_title__icontains=question)
    return query_set.all().order_by(sort_order())


def get_subjective_questions_by_id(id: int):
    """Search Query for subjective question through id"""
    return models.SubjectiveQuestions.objects.filter(id=id)


def get_grades(id: int = None):
    query_set = models.Grades.objects
    if id:
        query_set = query_set.filter(id=id)
    return query_set.all()


def get_excel_question(id: int = None):
    query_set = models.ExcelQuestions.objects
    if id:
        query_set = query_set.filter(id=id)
    return query_set.all().order_by(sort_order())


def get_subject_by_name(subject: str):
    return models.Subjects.objects.filter(subject=subject).first()


def get_subjective_questions_by_subject(subject: str):
    """get all subjective questions by specific given subject"""
    return models.SubjectiveQuestions.objects.filter(question_id__subject=subject)


def get_multiple_choice_questions_by_subject(subject: str):
    """get all multiple choice questions by specific given subject"""
    return models.MultipleChoiceQuestions.objects.filter(question_id__subject=subject)


def get_image_multiple_choice_questions_by_subject(subject: str):
    """get all image based multiple choice questions by specific given subject"""
    return models.ImageMultipleChoiceQuestions.objects.filter(question_id__subject=subject)


def get_excel_questions_by_subject(subject: str):
    """get all excel questions by specific given subject"""
    return models.ExcelQuestions.objects.filter(question_id__subject=subject)


def get_image_subjective_questions_by_subject(subject: str):
    """get all image based subjective questions by specific given subject"""
    return models.ImageBasedSubjectiveQuestions.objects.filter(question_id__subject=subject)


def get_passage_instruction_content_by_subject(subject: str):
    """get all passage instruction content by specific given subject"""
    return models.PassageInstructionContents.objects.filter(question_id__subject=subject)


def get_multi_image_choice_question_by_subject(subject: str):
    """get all multi imagge choice by specific given subject"""
    return models.MultipleImageChoiceQuestion.objects.filter(question_id__subject=subject)


def get_paper_setup_description_by_id(id: int):
    return models.PaperSetupDescription.objects.filter(id=id).first()


def get_paper_subject_by_paper():
    return models.PaperSetupSubjectMap.objects.all().order_by(sort_order())


def get_paper_subject_map_by_paper_id(id: int):
    return models.PaperSetupSubjectMap.objects.filter(paper_setup_id=id).order_by(sort_order('subject_order', False))


def get_paper_subject_map_by_subject_id(id: int, paper_id):
    return models.PaperSetupSubjectMap.objects.filter(paper_setup_id=paper_id, subject_id=id).first()


def get_paper_subject_map_by_paper_id_subject_id(paper_id: int, subject_id: int):
    return models.PaperSetupSubjectMap.objects.filter(subject=subject_id, paper_setup_id=paper_id).first()


def get_test_level():
    return models.TestLevels.objects.all().order_by(sort_order())


def get_test_level_by_id(id: int):
    return models.TestLevels.objects.filter(id=id)


def get_subject_question_data_paper_by_id(paper_id: int, subject_id=None):
    query_set = models.SubjectQuestionMap.objects
    if paper_id:
        query_set = query_set.filter(paper_setup_id=paper_id)
    if subject_id:
        query_set = query_set.filter(paper_setup_subject_id=subject_id)
    return query_set.all()


def get_subjectitve_question_by_allquestion_id(allquestion_id: int):
    return models.SubjectiveQuestions.objects.filter(question_id=allquestion_id).first()


def get_image_subjectitve_question_by_allquestion_id(allquestion_id: int):
    return models.ImageBasedSubjectiveQuestions.objects.filter(question_id=allquestion_id).first()


def get_image_multiple_choice_question_by_allquestion_id(allquestion_id: int):
    return models.ImageMultipleChoiceQuestions.objects.filter(question_id=allquestion_id).first()


def get_multiple_choice_question_by_allquestion_id(allquestion_id: int):
    return models.MultipleChoiceQuestions.objects.filter(question_id=allquestion_id).first()


def get_excel_question_by_allquestion_id(allquestion_id: int):
    return models.ExcelQuestions.objects.filter(question_id=allquestion_id).first()


def get_passage_question_by_allquestion_id(allquestion_id: int):
    return models.PassageInstructionContents.objects.filter(question_id=allquestion_id).first()


def get_multi_image_choice_question_by_allquestion_id(allquestion_id: int):
    return models.MultipleImageChoiceQuestion.objects.filter(question_id=allquestion_id).first()


def get_multiple_image_choice_que_by_id(id: int):
    return models.MultipleImageChoiceQuestion.objects.filter(id=id).first()


def get_multiple_img_choice_que_all(question_title: str, subject: str):
    """ Query for all multiple image choice question data"""
    query_set = models.MultipleImageChoiceQuestion.objects
    if question_title:
        query_set = query_set.filter(question_title__icontains=question_title)
    if subject:
        query_set = query_set.filter(question_id__subject=subject)
    return query_set.all().order_by(sort_order())


def get_paper_description(id: int = None, test_level: int = None):
    query_set = models.PaperSetupDescription.objects
    if id:
        query_set = query_set.filter(id=id)
    if test_level:
        query_set = query_set.filter(test_level=test_level)

    return query_set.all().order_by(sort_order())


def get_candidate_details_by_id(id: int):
    return models.CandidateDetails.objects.filter(id=id)


def get_candidate_individual_result_by_id(candidate: int, paper_subject: None):
    query_set = models.CandidateResultIndividual.objects
    if candidate:
        query_set = query_set.filter(candidate=candidate)
    if paper_subject:
        query_set = query_set.filter(paper_subject_id=paper_subject)
    return query_set


def get_candidate_individual_result_by_paperId_candidateId_paper_subId(paper_id: int, candidate_id: int, paper_subject: int):
    return models.CandidateResultIndividual.objects.filter(paper_set_id=paper_id, candidate=candidate_id, paper_subject_id=paper_subject)


def get_paper_setup_subject_map_by_id(id: int):
    return models.PaperSetupSubjectMap.objects.filter(id=id).first()


def get_model_by_candidate_id(model, candidate_id: int):
    return model.objects.filter(candidate=candidate_id)

def get_candidate_details_by_id(candidate_id):
    return models.CandidateDetails.objects.filter(
                id=candidate_id)

def get_personal_interview_mappming_by_candidate_and_teamlead_id(teamlead, candidate):
    return models.PersonalInterviewMap.objects.filter(interviewer_id=teamlead, interviewee_id=candidate).first()


def get_candidate_individual_result_Cid_PaperSetId(candidate_id, paper_id):
    return models.CandidateResultIndividual.objects.filter(
                candidate_id=candidate_id, paper_set_id=paper_id)


def get_candidate_individual_result_Cid_paperSubjectID(candidate_id, subject_id):
    return models.CandidateResultIndividual.objects.filter(
                    candidate_id=candidate_id, paper_subject_id=subject_id)


def get_model_by_allQuestionId(model, all_question_id):
   return model.objects.filter(
            all_question_id=all_question_id)

def get_paper_setup_subject_map_by_subject_paperSetId(subject, paper_id):
    return models.PaperSetupSubjectMap.objects.filter(
            subject=subject, paper_setup_id=paper_id)


def get_candidate_individual_res_by_Cid_sub_id_all_question_id(candidate_id, all_question_id):
    models.CandidateResultIndividual.objects.filter(candidate=candidate_id,subject_question_id__all_question_id=all_question_id)


