import re

def validate(value, type):
    result = False
    if type == 'c2':
        result = s2_val(value)
    elif type == 'c3':
        result = s3_val(value)
    elif type == 'i':
        result = i_val(value)
    elif type == 'em':
        result = mail_val(value)
    elif type == 't':
        result = tm_val(value)
    elif type == 'ds':
        result = wd_val(value)
    return result
    
def s2_val(str):
    return len(str) == 2 and all(char in set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for char in str)

def s3_val(str):
    return len(str) == 3 and all(char in set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for char in str)

def i_val(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def wd_val(string):
    strn = str(string)
    while len(strn) < 7:
        strn = '0' + strn
    return len(strn) == 7 and all(char in "01" for char in strn)

def tm_val(str):
    try:
        hours, minutes, seconds = map(int, str.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
            return True
        else:
            return False
    except (ValueError, IndexError):
        return False
    
def mail_val(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False    
