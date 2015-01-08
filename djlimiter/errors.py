from django.http import HttpResponse


class RateLimitExceeded(HttpResponse):
    """
    exception raised when a rate limit is hit (status code: 429).
    """
    status_code = 429
    def __init__(self, limit):
        super(RateLimitExceeded, self).__init__(str(limit))