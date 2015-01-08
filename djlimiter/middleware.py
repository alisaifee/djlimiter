from django.conf import settings

from django.core.urlresolvers import resolve
from limits.storage import storage_from_string
from limits.strategies import STRATEGIES
from limits.errors import ConfigurationError
from limits.util import parse_many
from .decorators import DECORATED
from .util import get_ipaddr, LimitWrapper
from .errors import RateLimitExceeded

class C:
    ENABLED = "RATELIMIT_ENABLED"
    HEADERS_ENABLED = "RATELIMIT_HEADERS_ENABLED"
    STORAGE_URL = "RATELIMIT_STORAGE_URL"
    STRATEGY = "RATELIMIT_STRATEGY"
    GLOBAL_LIMITS = "RATELIMIT_GLOBAL"
    HEADER_LIMIT = "RATELIMIT_HEADER_LIMIT"
    HEADER_REMAINING = "RATELIMIT_HEADER_REMAINING"
    HEADER_RESET = "RATELIMIT_HEADER_RESET"
    DEFAULT_KEY_FUNCTION = "RATELIMIT_KEY_FUNCTION"
    CALLBACK = "RATELIMIT_CALLBACK"

class HEADERS:
    RESET = 1
    REMAINING = 2
    LIMIT = 3


class Limiter(object):
    def __init__(self):
        self.enabled = getattr(settings, C.ENABLED, True)
        self.headers_enabled = getattr(settings, C.HEADERS_ENABLED, False)
        self.strategy = getattr(settings, C.STRATEGY, 'fixed-window')
        if self.strategy not in STRATEGIES:
            raise ConfigurationError("Invalid rate limiting strategy %s" % self.strategy)
        self.storage = storage_from_string(getattr(settings, C.STORAGE_URL, "memory://"))
        self.limiter = STRATEGIES[self.strategy](self.storage)
        self.key_function = getattr(settings, C.DEFAULT_KEY_FUNCTION, get_ipaddr)
        conf_limits = getattr(settings, C.GLOBAL_LIMITS, "")
        self.global_limits = []
        if conf_limits:
            self.global_limits = [
                LimitWrapper(
                    limit, self.key_function, None, False
                ) for limit in parse_many(conf_limits)
            ]
        self.header_mapping = {
            HEADERS.RESET : getattr(settings,C.HEADER_RESET, "X-RateLimit-Reset"),
            HEADERS.REMAINING : getattr(settings,C.HEADER_REMAINING, "X-RateLimit-Remaining"),
            HEADERS.LIMIT : getattr(settings,C.HEADER_LIMIT, "X-RateLimit-Limit"),
        }
        self.callback = getattr(settings, C.CALLBACK, self.__raise_exceeded )



    def __raise_exceeded(self, limit):
        return RateLimitExceeded(limit)


    def process_request(self, request):
        func = resolve(request.path).func
        name = resolve(request.path).url_name if func else ""
        limits = self.global_limits
        if name:
            if func in DECORATED:
                limits = DECORATED[func]
        limit_for_header = None
        failed_limit = None
        for lim in limits:
            limit_scope = lim.get_scope(request) or name
            if not limit_for_header or lim.get_limit() < limit_for_header[0]:
                limit_for_header = (lim.get_limit(), (lim.key_func or self.key_function)(request), limit_scope)
            if lim.per_method:
                limit_scope += ":%s" % request.method
            if not self.limiter.hit(lim.get_limit(), (lim.key_func or self.key_function)(request), limit_scope):
                failed_limit = lim.get_limit()
                limit_for_header = (lim.get_limit(), (lim.key_func or self.key_function)(request), limit_scope)

        request.view_rate_limit = limit_for_header
        if failed_limit:
            return self.__raise_exceeded(failed_limit)

    def process_response(self, request, response):
        current_limit = getattr(request, "view_rate_limit", None)
        if self.headers_enabled and current_limit:
            window_stats = self.limiter.get_window_stats(*current_limit)
            response[self.header_mapping[HEADERS.LIMIT]] = str(current_limit[0].amount)
            response[self.header_mapping[HEADERS.REMAINING]] = window_stats[1]
            response[self.header_mapping[HEADERS.RESET]] = window_stats[0]
        return response





