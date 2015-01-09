
djlimiter
---------
Rate limiting middleware for Django applications

.. toctree::
    :hidden:

    config
    string-notation
    decorators
    strategy
    recipes
    api


.. currentmodule:: djlimiter

Usage
-----
Quick start
===========
Add the rate limiter to your django projects' `settings.py` and enable a global rate limit for all
views in your project:

.. code-block:: python

   MIDDLEWARE_CLASSES += ("djlimiter.Limiter",)
   RATELIMIT_GLOBAL = "10/second; 50/hour"


In one of the apps' view:


.. code-block:: python

    @limit("5/second")
    def index(request):
        ...

    @exempt
    def ping(request):
        ...

The above example will result in the following characteristics being applied to the django project:

* A global rate limit of 10 per second, and 50 per hour applied to all routes.
* The ``index`` route will have an explicit rate limit of 5/second
* The ``ping`` route will be exempt from any global rate limits.


Every time a request exceeds the rate limit, the view function will not get called and instead
a `429 <http://tools.ietf.org/html/rfc6585#section-4>`_ http error will be raised.

Refer to :ref:`recipes` for more examples.

References
----------
* `Redis rate limiting pattern #2 <http://redis.io/commands/INCR>`_
* `DomainTools redis rate limiter <https://github.com/DomainTools/rate-limit>`_
* `limits: python rate limiting utilities <https://limits.readthedocs.org>`_

.. include:: ../../HISTORY.rst
