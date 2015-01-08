.. _pymemcache: https://pypi.python.org/pypi/pymemcache
.. _redis: https://pypi.python.org/pypi/redis

.. _ratelimit-conf:

Configuration
-------------
The following django settings are honored by the middleware.


``RATELIMIT_GLOBAL``
    A comma (or some other delimiter) separated string
    that will be used to apply a global limit on all
    routes. :ref:`ratelimit-string` for details.
``RATELIMIT_CALLBACK``
    The callback which will be called when a rate limit is hit.
    Defaults to a ``429`` status code being returned.
``RATELIMIT_KEY_FUNCTION``
    The default callable to use to derive the context of a request.
    This can either be the callable itself or a fully qualified path to a callable.
    The callable to accept a single request object as a parameter and return a string.
    Defaults to the ``ip address`` of the requesting user.
``RATELIMIT_STORAGE_URL``
    One of ``memory://``, ``redis://host:port`` or ``memcached://host:port``.
    Using the redis storage requires the installation of the `redis`_ package while memcached relies on `pymemcache`_.
``RATELIMIT_STRATEGY``
    The rate limiting strategy to use. :ref:`ratelimit-strategy` for details.
``RATELIMIT_HEADERS_ENABLED``
    Enables returning :ref:`ratelimit-headers`. Defaults to ``False``
``RATELIMIT_ENABLED``
    Overall kill switch for rate limits. Defaults to ``True``
``RATELIMIT_HEADER_LIMIT``
    Header for the current rate limit. Defaults to ``X-RateLimit-Limit``
``RATELIMIT_HEADER_RESET``
    Header for the reset time of the current rate limit. Defaults to ``X-RateLimit-Reset``
``RATELIMIT_HEADER_REMAINING``
    Header for the number of requests remaining in the current rate limit. Defaults to ``X-RateLimit-Remaining``
