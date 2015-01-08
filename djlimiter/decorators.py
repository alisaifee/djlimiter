from functools import wraps
from limits.util import parse, parse_many
from .util import LimitWrapper

DECORATED = {}
EXEMPT = []

def limit(limit_value, key_function=None, per_method=False):
    """
    :param limit_value:
    :param key_function:
    :param per_method:
    :return:
    """
    def __inner(fn):
        @wraps(fn)
        def _inner(*args, **kwargs):
            return fn(*args, **kwargs)
        if callable(limit_value):
            DECORATED.setdefault(_inner, []).append(
                LimitWrapper(limit_value, key_function, None, per_method)
            )
        else:
            DECORATED.setdefault(_inner, []).extend([
                LimitWrapper(
                    lim, key_function, None, per_method
                ) for lim in parse_many(limit_value)
            ])

        return _inner
    return __inner


def exempt(fn):
    """
    :param fn:
    :return:
    """
    @wraps(fn)
    def __inner(*a, **k):
        return fn(*a, **k)
    EXEMPT.append(__inner)
    return __inner
