.. _recipes:

Recipes
=======


Custom Rate limit domains
-------------------------

By default, all rate limits are applied on a per ``remote address`` basis.
However, you can easily customize your rate limits to be based on any other
characteristic of the incoming request. On a django settings level this can be achieved
by settings the ``RATELIMIT_KEY_FUNCTION`` to either point to a callable or a fully qualified
path to a callable. This callable should:

 * Expect a single :class:`django.http.HttpRequest` object as a parameter.
 * Return a string that classifies the request.


Using Django Class Views
------------------------

If you are using a class based approach to defining view functions, the regular
method of decorating a view function to apply a per route rate limit will not
work. You can add rate limits to your views by using the following approach (also
described in :ref:`django:decorating-class-based-views`).


.. code-block:: python


    class MyView(django.views.generic):
        def get(self):
            return HttpResponse("get")

        def put(self):
            return HttpResponse("put")

.. code-block:: python

        urlpatterns = patterns('',
            (r'^myview/', limit("2/second")(MyView.as_view())),
        )


.. note:: This approach is limited to either sharing the same rate limit for
 all http methods of a given :class:`django.views.generic.View` or applying the declared
 rate limit independently for each http method (to accomplish this, pass in ``True`` to
 the ``per_method`` keyword argument to :meth:`limit`).


