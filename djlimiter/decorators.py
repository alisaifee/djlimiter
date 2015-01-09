from functools import wraps
from limits.util import parse, parse_many
from .util import LimitWrapper

DECORATED = {}
EXEMPT = []

def limit(limit_value, key_function=None, per_method=False):
    """
    decorator to be used for rate limiting individual views

    :param limit_value: rate limit string or a callable that returns a string.
     :ref:`ratelimit-string` for more details.
    :param function key_func: function/lambda to extract the unique identifier for
     the rate limit. defaults to remote address of the request.
    :param bool per_method: whether the limit is sub categorized into the http
     method of the request.
    """
    def __inner(fn):
        @wraps(fn)
        def _inner(*args, **kwargs):
            return fn(*args, **kwargs)
        if fn in DECORATED:
            DECORATED.setdefault(_inner, DECORATED.pop(fn))
        if callable(limit_value):
            DECORATED.setdefault(_inner, []).append(
                LimitWrapper(limit_value, key_function, None, per_method)
            )
        else:
            DECORATED.setdefault(_inner, []).extend([
                LimitWrapper(
                    list(parse_many(limit_value)), key_function, None, per_method
                )
            ])

        return _inner
    return __inner

def shared_limit(limit_value, scope, key_function=None):
    """
    decorator to be applied to multiple views sharing the same rate limit.

    :param limit_value: rate limit string or a callable that returns a string.
     :ref:`ratelimit-string` for more details.
    :param scope: a string or callable that returns a string
     for defining the rate limiting scope.
    :param function key_func: function/lambda to extract the unique identifier for
     the rate limit. defaults to remote address of the request.
    """
    def __inner(fn):
        @wraps(fn)
        def _inner(*args, **kwargs):
            return fn(*args, **kwargs)

        if fn in DECORATED:
            DECORATED.setdefault(_inner, DECORATED.pop(fn))
        if callable(limit_value):
            DECORATED.setdefault(_inner, []).append(
                LimitWrapper(limit_value, key_function, scope)
            )
        else:
            DECORATED.setdefault(_inner, []).extend([
                LimitWrapper(
                    list(parse_many(limit_value)), key_function, scope
                )
            ])
        return _inner
    return __inner



def exempt(fn):
    """
    decorator to mark a view or all views in a blueprint as exempt from rate limits.

    :param fn: the view to wrap.
    :return:
    """
    @wraps(fn)
    def __inner(*a, **k):
        return fn(*a, **k)
    EXEMPT.append(__inner)
    return __inner
