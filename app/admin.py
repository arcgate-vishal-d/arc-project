from django.contrib import admin
from django.contrib import admin
from app.models import (
    PassageInstructionContents,
    MultipleChoiceQuestions,
    ImageBasedSubjectiveQuestions,
    ImageMultipleChoiceQuestions,
    AllQuestions, ExcelQuestions,
    Grades,
    PaperSetupDescription,
    TestLevels,
    PaperSetupSubjectMap,
    SubjectQuestionMap,
    MultipleImageChoiceQuestion,
    PaperHistory,
    CandidateDetails,
    CandidateEducationDetails,
    CandidateFamilyDetails,
    CandidateWorkExperience,
    CandidateSourceOfInformation,
    CandidateOtherDetails,
    CandidateResults,
    CandidateResultIndividual,
    CandidateDetails,
    CandidateResults,
    PersonalInterview,
    InterviewParameter,
)


@admin.register(PassageInstructionContents)
class AdminPassageInstructionContents(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'created_by',
                    'types', 'question_title', 'description', 'status']


@admin.register(MultipleChoiceQuestions)
class AdminMultipleChoiceQuestions(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'created_by', 'question_title', 'answer_key', 'optionA', 'optionB', 'optionC',
                    'optionD', 'passage', 'status']


@admin.register(ImageBasedSubjectiveQuestions)
class AdminImageBasedSubjectiveQuestions(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'created_by', 'question_title', 'answer_key',
                    'status']


@admin.register(AllQuestions)
class AdminPassageInstructionContents(admin.ModelAdmin):
    list_display = ['id','subject', 'type']


@admin.register(ImageMultipleChoiceQuestions)
class AdminImageMultipleChoiceQuestions(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'created_by', 'question_title', 'answer_key', 'optionA', 'optionB', 'optionC',
                    'optionD', 'status']


@admin.register(ExcelQuestions)
class AdminExcelQuestions(admin.ModelAdmin):
    list_display = ['question_id', 'created_by',
                    'sheet_id', 'question_title', 'description', 'type']


@admin.register(MultipleImageChoiceQuestion)
class AdminMultipleImageChoiceQuestion(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'created_by', 'question_title', 'answer_key', 'optionA', 'optionB', 'optionC',
                    'optionD', 'status']


@admin.register(Grades)
class AdminGrades(admin.ModelAdmin):
    list_display = ['title', 'grade_from', 'grade_to']


@admin.register(PaperSetupDescription)
class AdminPapersetup(admin.ModelAdmin):
    list_display = ['id', 'department', 'test_level',
                    'paper_description', 'paper_time', 'paper_time', 'paper_marks']


@admin.register(TestLevels)
class AdminTestLevels(admin.ModelAdmin):
    list_display = ['id', 'test_level', 'created_by']


@admin.register(PaperSetupSubjectMap)
class AdminPaperSetupSubjectMap(admin.ModelAdmin):
    list_display = ['id', 'paper_setup_id', 'subject', 'subject_time',
                    'subject_marks', 'subject_order', 'subject_questions']


@admin.register(SubjectQuestionMap)
class AdminSubjectQuestionMap(admin.ModelAdmin):
    list_display = ['id', 'paper_setup_id',
                    'paper_setup_subject_id', 'all_question_id']


@admin.register(PaperHistory)
class AdminPaperHistory(admin.ModelAdmin):
    list_display = ['id', 'paper_set',
                    'set_by', 'date']


@admin.register(CandidateDetails)
class AdminCandidateDetails(admin.ModelAdmin):
    list_display = ['id', 'test_level','sheet_id','first_name', 'last_name', 'email', 'gender', 'dob', 'mobile_no_1', 'mobile_no_2',
                    'present_address', 'permanent_address', 'district_present', 'district_permanent', 'status', 'profile_progress']


@admin.register(CandidateEducationDetails)
class AdminCandidateEducationDetails(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'qualifications', 'education_details', 'school_college',
                    'board_university', 'year_of_passing', 'division', 'percentage', 'medium']


@admin.register(CandidateFamilyDetails)
class AdminCandidateFamilyDetails(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'name',
                    'relation', 'occupation', 'dependent']


@admin.register(CandidateOtherDetails)
class AdminCandidateOtherDetails(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'service_commitment',
                    'salary_security', 'shift', 'expected_joining_date', 'salary_expected']


@admin.register(CandidateSourceOfInformation)
class AdminCandidateSourceOfInformation(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'previous_interviewed',
                    'previous_worked', 'source_of_info', 'newspaper', 'consultancy']


@admin.register(CandidateWorkExperience)
class AdminCandidateWorkExperience(admin.ModelAdmin):
    list_display = ['id', 'candidate', 'name_of_company', 'designation',
                    'joining_date', 'reliving_date', 'reason_of_leaving', 'last_salary']

@admin.register(CandidateResults)
class AdminCandidateResults(admin.ModelAdmin):
    list_display = ['id', 'candidate','grade']

@admin.register(CandidateResultIndividual)
class AdminCandidateResultIndividual(admin.ModelAdmin):
    list_display = ['id', 'candidate','paper_set_id','subject_question_id','paper_subject_id','answer_marks','candidate_answer','answer_status']



@admin.register(PersonalInterview)
class AdminPersonalInterview(admin.ModelAdmin):
    list_display = ['id', 'interviewer', 'candidate', 'parameter', 'action']


@admin.register(InterviewParameter)
class AdminInterviewParameter(admin.ModelAdmin):
    list_display = ['id', 'parameter','created_by' ]
