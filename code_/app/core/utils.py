import datetime
from functools import wraps

from flask import request


def str_to_datetime(v) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(v, '%Y-%m-%d')
    except ValueError:
        return datetime.datetime.today()


def date_filter(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        today = datetime.datetime.today()
        start = request.args.get('start', datetime.datetime(2023, 8, 10), type=str_to_datetime)
        end = request.args.get('end', datetime.datetime(today.year, today.month, today.day),
                               type=str_to_datetime)
        start = start.replace(hour=0, minute=0, second=0)
        end = end.replace(hour=23, minute=59, second=59)
        kwargs.setdefault('start', start)
        kwargs.setdefault('end', end)
        return func(*args, **kwargs)

    return wrapped
