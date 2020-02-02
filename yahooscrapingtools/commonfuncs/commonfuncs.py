import datetime


def get_year():
    today = datetime.datetime.now()
    if today.month < 8:
        today.replace(year=today.year - 1)
    return today.year
