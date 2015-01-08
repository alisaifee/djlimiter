.. |travis-ci| image:: https://secure.travis-ci.org/alisaifee/djlimiter.png?branch=master
    :target: https://travis-ci.org/#!/alisaifee/djlimiter?branch=master
.. |coveralls| image:: https://coveralls.io/repos/alisaifee/djlimiter/badge.png?branch=master
    :target: https://coveralls.io/r/alisaifee/djlimiter?branch=master
.. |pypi| image:: https://pypip.in/v/djlimiter/badge.png
    :target: https://crate.io/packages/djlimiter/
.. |license| image:: https://pypip.in/license/djlimiter/badge.png
    :target: https://pypi.python.org/pypi/djlimiter/

*********
djlimiter
*********
|travis-ci| |coveralls| |pypi| |license|

djlimiter provides rate limiting features to django via a middleware.

Quickstart
===========

Add the rate limiter to your django projects' `settings.py` and enable a global rate limit for all
views in your project:

.. code-block:: python

   MIDDLEWARE_CLASSES += ("djlimiter.Limiter",)
   RATELIMIT_GLOBAL = "10/second"


If you only want to enable rate limits to certain endpoints, leave out the `RATELIMIT_GLOBAL` setting and
use the decorator approach instead in the respective view function:


.. code-block:: python

    @limit("10/second")
    def index(request):
       ...



For detailed documentation visit `Read the docs <http://djlimiter.readthedocs.org>`_



