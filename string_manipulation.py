import re
from datetime import datetime, timedelta


# REPLACING ALL SYMBOLS WITH SPACES
# C:\file\video\video_name.mp4 TO video name
def path_to_video_title(video_file):
    file_title = re.findall('([^\/]+$)', video_file)[0]
    try:
        file_title = re.sub('[^a-zA-Z0-9\n\.]', ' ', file_title)
    except Exception as e:
        print(e.message, e.args)
    file_title = file_title[0:file_title.find('.')]

    return file_title.title()


# C:\file\video\name.mp4 TO name.mp4
def path_to_video_name(video_file):
    return re.findall('([^\/]+$)', video_file)[0]


# REFORMATTING THE CALENDAR DATE, TO AN EASY TO READ DATE
def qdate_to_date(calendar_date):
    return calendar_date[calendar_date.find('(') + 1:calendar_date.find(')')]


# FROM \\ AND \ TO /
def double_backslash_to_slash(text):
    text = text.replace('\\\\', '/')
    text = text.replace('\\', '/')
    return text


# CHECK IF THERE ARE ANY LETTERS FROM A TO Z IN A STRING
def contains_letters(text):
    if re.search('[a-zA-Z]', text):
        return True


# COUNT HOW MANY NUMBERS THERE ARE IN A GIVEN STRING
def count_numbers_in_string(text):
    numbers = sum(character.isdigit() for character in text)
    # letters = sum(character.isalpha() for character in text)
    # spaces = sum(character.isspace() for character in text)
    return numbers


# COUNT THE SUMMARY OF NUMBERS IN A GIVEN STRING
def sum_digits_string(text):
    sum_digit = 0
    for x in text:
        if x.isdigit() == True:
            z = int(x)
            sum_digit = sum_digit + z

    return sum_digit


# REPLACE 5 TO 5-
def dash_after_number(text):
    text += '-'
    return text


# RETURNS TRUE IF A GIVEN STRING CONTAINS JUST NUMBERS AND DASHES
def allow_dash_number(text):
    if re.match('^[0-9-]*$', text):
        return True


# GET FILE NAME - REMOVE FILE EXTENSION
def get_file_name(file):
    return file.rsplit('.', 1)[0]


# CONVERT LIST TO A LONG STRING
def list_to_string(list_):
    list_ = map(str, list_)
    return list_


# CONVERT FRAMES LIST TO DATETIME LIST
def frame_to_time_list(df, fps):
    second_timestamps = (df[0] / fps).to_list()
    int_second_timestamps = [int(fl) for fl in second_timestamps]
    time_list = [str(timedelta(seconds=i)) for i in int_second_timestamps]
    return time_list


# CONVERT DATETIME TO INTEGER
def date_to_seconds(text):
    try:
        return sum(x * int(t) for x, t in zip([3600, 60, 1], text.split(':')))
    except ValueError as ve:
        print(ve)


# CONVERT INT LIST TO STRING
def int_list_to_string_list(ints):
    string_ints = [str(num) for num in ints]
    return string_ints


# RETURNS JUST NUMBERS FROM STRING THAT CONTAINS NUMBERS, SYMBOLS, AND LETTERS
def keep_numbers(text):
    return ''.join(c for c in text if c.isdigit())


# IF '123' RETURN 123 ELSE RETURN TEXT
def string_to_int_or_pass(text):
    try:
        text = int(text)
        return text
    except ValueError as ve:
        print(ve)
    return text


# FROM python3.y.z (tags/v.3.y.z.......) to 3.9
def keep_till_second_dot(text):
    text = re.findall('^(\d+\.\d)', text)[0]
    return text


# GETTING THE CURRENT DATE AND TIME
def get_date_time():
    now = datetime.now()  # current date and time
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H.%M.%S")
    return date, time


# GET EVERYTHING AFTER LAST SLASH
def get_after_last_slash(text):
    text = re.findall('([^\/]+$)', text)[0]
    return text


def fix_uuid(text):
    return text.replace('-', '')
