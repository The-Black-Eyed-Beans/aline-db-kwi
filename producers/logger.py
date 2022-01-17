import logging

from datetime import date


def get_info_logger():
    logs = logging.getLogger('Data Producer')
    logs.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%m-%d-%Y %H:%M:%S')
    console.setFormatter(formatter)

    logs.addHandler(console)

    return logs


def get_debug_logger():
    logs = logging.getLogger('Data Producer Debug')
    logs.setLevel(logging.DEBUG)

    today = date.today()

    file = logging.FileHandler('logs/debug_' + str(today) + '.log')
    file.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%m-%d-%Y %H:%M:%S')
    file.setFormatter(formatter)
    console.setFormatter(formatter)

    logs.addHandler(file)
    logs.addHandler(console)

    return logs


def get_error_logger():
    logs = logging.getLogger('Data Producer Errors')
    logs.setLevel(logging.ERROR)

    today = date.today()

    file = logging.FileHandler('logs/error_' + str(today) + '.log')
    file.setLevel(logging.ERROR)

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', '%m-%d-%Y %H:%M:%S')
    file.setFormatter(formatter)
    console.setFormatter(formatter)

    logs.addHandler(file)
    logs.addHandler(console)

    return logs
