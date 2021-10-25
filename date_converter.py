import logging
import re


def configure_the_date(date: str) -> int:
    result = str()
    months_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                   "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    rfc822_pattern = re.compile(r"([0-3][0-9]) ([a-zA-Z]{3}) ([0-2][0-9][0-9][0-9])")
    non_rfc822_pattern = re.compile(r"([0-2]\d\d\d)-([0-1][0-9])-([0-3]\d)")
    if date[0].isdigit():
        match = non_rfc822_pattern.search(date)
        result += match.group(1) + match.group(2) + match.group(3)
    else:
        match = rfc822_pattern.search(date)
        result += match.group(3) + months_dict.get(match.group(2)) + match.group(1)
    return int(result)


def check_user_date(date: int):
    month_30_day_max = ["04", "06", "09", "11"]
    exception_flag = False
    if date < 0 or len(str(date)) != 8:
        exception_flag = True
    user_date = str(date)
    user_year = user_date[:4]
    if int(user_year) > 2021:
        exception_flag = True
    user_month = user_date[4:6]
    if int(user_month) > 12:
        exception_flag = True
    user_day = user_date[6:8]
    if int(user_day) > 31:
        exception_flag = True
    if user_month in month_30_day_max and int(user_day) > 30:
        exception_flag = True
    if user_month == "02" and int(user_day) > 29:
        exception_flag = True
    if exception_flag:
        logging.error(msg="Wrong date!")
        exit()
