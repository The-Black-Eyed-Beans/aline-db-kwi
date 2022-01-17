import os

from dotenv import load_dotenv

load_dotenv()


def get_api():
    return os.getenv('ALINE_API')


def get_bank_api():
    return get_api() + '/banks'


def get_branch_api():
    return get_api() + '/branches'


def get_trans_api():
    return get_api() + '/transactions'


def get_applicant_api():
    return get_api() + '/applicants'


def get_application_api():
    return get_api() + '/applications'


def get_user_api():
    return get_api() + '/users'
