from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from app.utility import constants, return_message

from app.utility import constants, return_message


def check_fixed_subjects(subject):
    spl_subjects = ['Excel', 'Typing Test', 'Internet Search']
    if str(subject) in spl_subjects:
        return True

def correct_ans(radio_input: str, option_a, option_b, option_c, option_d):
    if radio_input == "optionA":
        radio_input = option_a
    elif radio_input == "optionB":
        radio_input = option_b
    elif radio_input == "optionC":
        radio_input = option_c
    else:
        radio_input = option_d
    return radio_input

def method_not_allowed(method, request):
    '''checking valid methods '''
    if method not in constants.ALLOWED_METHODS:
        messages.error(request, return_message.MESSAGE['wrong_method'])
        return True

def check_fixed_types(content):
    content_types = ['passage', 'typing', 'instructions']
    if str(content) in content_types:
        return False

def validate_check_null(value):
    if not value:
        raise  ValidationError("blank_field")

def unique_options(optionA,optionB,optionC,optionD,method):
    """Check if all four options of mcq type questions are unique """
    option_list = [optionA, optionB, optionC, optionD]
    if len(set(option_list)) < len(option_list):
        if method == "delete":
            return False
        return True
    return False

def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser
            
        return WrappedClass
    return wrapper

def admin_required():
    def wrapper(wrapped_staff):
        class WrappedClass(UserPassesTestMixin,wrapped_staff):
            def test_func(self):
                if self.request.user.is_staff:
                    return self.request.user.is_staff
                else:
                    return self.request.user.is_superuser
            
        return WrappedClass
    return wrapper
