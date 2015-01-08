Decorators
----------
The decorators made available as instance methods of the :class:`Limiter`
instance are

.. currentmodule:: djlimiter

.. _ratelimit-decorator-limit:

:meth:`limit`
  There are a few ways of using this decorator depending on your preference and use-case.

  Single decorator
    The limit string can be a single limit or a delimiter separated string

      .. code-block:: python

         @limit("100/day;10/hour;1/minute")
         def my_view(request)
           ...

  Multiple decorators
    The limit string can be a single limit or a delimiter separated string
    or a combination of both.

        .. code-block:: python

           @limit("100/day")
           @limit("10/hour")
           @limit("1/minute")
           def my_view(request):
             ...

  Custom keying function
    By default rate limits are applied on per remote address basis. You can implement
    your own function to retrieve the key to rate limit by.

        .. code-block:: python

            def my_key_func(request):
              ...

            @limit("100/day", my_key_func)
            def my_view(request):
              ...

        .. note:: The key function must accept one argument which is a :class:`django.http.HttpRequest` object

  Dynamically loaded limit string(s)
    There may be situations where the rate limits need to be retrieved from
    sources external to the code (database, remote api, etc...). This can be
    achieved by providing a callable (which takes a single parameter - the :class:`django.http.HttpRequest` object)
    to the decorator. The callable should return a rate limit string in the :ref:`ratelimit-string`.


        .. code-block:: python

               from django.conf import settings

               def rate_limit_from_config(request):
                   return settings.CUSTOM_LIMIT

               @limit(rate_limit_from_config)
               def my_view(request):
                   ...

        .. danger:: The provided callable will be called for every request
           on the decorated route. For expensive retrievals, consider
           caching the response.

.. _ratelimit-decorator-shared-limit:

:meth:`shared_limit`
    For scenarios where a rate limit should be shared by multiple views
    (For example when you want to protect views using the same resource
    with an umbrella rate limit).

    Named shared limit

      .. code-block:: python

        mysql_limit = shared_limit("100/hour", scope="mysql")

        @mysql_limit
        def my_view_1(request):
           ...

        @mysql_limit
        def my_view_2(request):
           ...


    Dynamic shared limit: when a callable is passed as scope, the return value
    of the function will be used as the scope.

      .. code-block:: python

        def host_scope(request):
            return request.META['HTTP_HOST']

        host_limit = limiter.shared_limit("100/hour", scope=host_scope)

        @host_limit
        def my_view_1():
           ...

        @host_limit
        def my_view_2():
           ...


    .. note:: Shared rate limits provide the same conveniences as individual rate limits

        * Can be chained with other shared limits or individual limits
        * Accept keying functions
        * Accept callables to determine the rate limit value



.. _ratelimit-decorator-exempt:

:meth:`exempt`
  This decorator simply marks a view as being exempt from any rate limits.

