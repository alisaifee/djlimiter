from functools import wraps
from limits.util import parse
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
        DECORATED.setdefault(_inner, []).append(
            LimitWrapper(parse(limit_value), key_function, None, per_method)
        )
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
