import re

def format_string_from_tuple(data_tuple, filler=' '):
  formatted_string = "|  "
  for i in range(0, len(data_tuple), 2):
    if i + 1 < len(data_tuple):
      element = str(data_tuple[i])
      if len(element) < (data_tuple[i + 1] - 2):
        formatted_element = element.ljust(data_tuple[i + 1] - 3, filler)
      else:
        formatted_element = element[:(data_tuple[i + 1] - 3)]
    else:
      formatted_element = str(data_tuple[i])
    formatted_string += formatted_element + filler + '|' + '  '
  return formatted_string[:-1]

def s2_val(str):
    return len(str) == 2 and all(char in set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for char in str)

def s3_val(str):
    return len(str) == 3 and all(char in set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for char in str)

def nt_val(str):
    pattern = r"\d{4}[a-z]{1}\d{2}"
    return bool(re.match(pattern, str))

def n4_val(str):
    try:
        a = int(str)
        if a > 0 and a <= 9999:
            return True
        else:
            return False
    except ValueError:
        return False

def np_val(str):
    pattern = r"[A-Z]{2}\d{7}"
    return bool(re.match(pattern, str))

def fl_val(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def nu_val(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def wd_val(str):
    return len(str) == 7 and all(char in "01" for char in str)

def tm_val(str):
    try:
        hours, minutes, seconds = map(int, str.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
            return True
        else:
            return False
    except (ValueError, IndexError):
        return False
