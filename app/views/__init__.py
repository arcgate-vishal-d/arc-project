from .login_view import Login
from .logout_view import Logout
from .dashboard_view import Dashboard
from .admin_user_view import (
    AdminUser,
    UserSettingsView
)
from .admin_subject_view import SubjectView
from .image_subjective_question_view import (
    ImageSubjectiveQuestionView,
    IBSQViews
)
from .admin_passage_content_view import (
    PassageContentView,
    PassageContentPOSTView
)
from .admin_image_mcq_view import (
    ImageBasedMcqView,
    ImageBasedMcqPostView,
)
from .admin_multiple_choice_questions import (
    MultiPleChoiceQuestion,
    MCQViews
)
from .admin_subjective_questions_view import (
    SubjectiveQuestionsView,
    AddSubjectiveQuestionsView
)
from .excel_question import ExcelQuestion
from .multiple_img_choice_que_view import (
    MultipleImageChoiceQuestionGetView,
    MultipleImageChoiceQuestionPostView
)
from .admin_paper_setup_view import (
    PaperSetup,
    PaperSetupRequestView,
    PaperSetupPost
)
from .paper_setup_details import PaperSetupDetails
from .admin_view_full_paperset import ViewFullPaperSet
from .admin_set_todays_paper import SetTodaysPaper
from .admin_reset_test_view import ResetTest
from .admin_view_result_view import AdminViewResult, AdminViewResultDetails
from .admin_individual_candidate_result_view import AdminIndividualResult
from .admin_result_personal_interview import AdminResultPersonalInterview

from .interview_homepage_view import InterviewHomePage
from .candidate_start_exam_view import ExamStartView
from .candidate_exam import CandidateExam
from .candidate_personal_detail_view import CandidatePersonalView
from .candidate_education_details_view import CandidateEducationalDetailView
from .candidate_work_exp_view import CandidateWorkExperienceDetailView
from .candidate_source_of_info_view import CandidateSourceOfInformationView
from .candidate_family_details_view import CandidateFamilyDetailView
from .candidate_other_details_view import CandidateOtherDetailView
from .candidate_fact_sheet_views import CandidateFactSheet
from .candidate_time_out_view import CandidateTimeOut
from .candidate_thanks_view import CandidateThankYou

from .error_handle import (
    error_401,
    error_403,
    error_404,
    error_405,
    error_500
)
