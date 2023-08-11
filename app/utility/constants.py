""" Constants for user role """
ADMINISTRATOR = "1"
ADMIN = "2"
INTERVIEWER = "3"

ACTIVE = "1"
PAGE_LIMIT = 10
DEFAULT_PAGE = 1
MODIFIED = 'modified'
DATE_JOINED = 'date_joined'
STATUS = [
    ('0', 'InActive'),
    ('1', 'Active'),
]
MULTIPLE_CHOICE_QUESTION = "multiple choice question"
ALLOWED_METHODS = ["", 'put', 'delete']
SUBJECTIVE_QUESTION = "subjective question"
IMAGE_MCQ = 'image based MCQ'
EXCEL_QUESTIONS = 'excel questions'
IMAGE_BASED_SUBJECTIVE_QUESTION = "Image based subjective question"
PASSAGE_INSTRUCTION = "Passage/Instruction"
MULTIPLE_IMAGE_CHOICE_QUESTION = "Multiple Image Choice Question"
MULTIPLE_IMAGE_CHOICE_QUESTION = "Multiple Image Choice Question"
# type of passage content model
TYPING = "typing"
TYPING_TEST = "Typing Test"
CORRECT = "Correct"
INCORRECT = "Incorrect"

# reviewable and non reviewable question types
REVIEWABEL_QUESTION_TYPES = ['multiple choice question','subjective question',
                             'image based MCQ','Image based subjective question',
                             'Multiple Image Choice Question']
NON_REVIEWABLE_QUESTION_TYPES = ['Passage/Instruction','excel questions']

ARCCRM_LOGIN_URL = "https://api.arccrm.com/api/InterviewLearningUser/validate"
