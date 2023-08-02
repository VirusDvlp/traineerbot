import re


def check_number(message) -> bool:
    '''User phone number must be start with "8" and has 10 digitals'''
    res = re.findall(r'(8[\d]{10}?)', message.text)
    return bool(res)
