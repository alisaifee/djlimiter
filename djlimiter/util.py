import logging
from django.core.urlresolvers import resolve
from limits.util import parse


def get_ipaddr(request):
    """
    :return: the ip address for the current request (or 127.0.0.1 if none found)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


class LimitWrapper(object):
    """
    basic wrapper to encapsulate limits and their context
    """
    def __init__(self, limit, key_func, scope, per_method=False):
        self._limit = limit
        self.key_func = key_func
        self._scope = scope
        self.per_method = per_method

    def get_limit(self, request):
        return parse(self._limit(request)) if callable(self._limit) else self._limit

    def get_scope(self, request):
        return (
            self._scope(resolve(request.path).url_name) if callable(self._scope) else (
                self._scope if self._scope else resolve(request.path).url_name
            )
        )
class BlackHoleHandler(logging.StreamHandler):
    def emit(*_):
        return
