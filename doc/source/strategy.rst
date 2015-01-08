.. _ratelimit-strategy:

Rate limiting strategies
------------------------
djlimiter comes with three different rate limiting strategies built-in. Pick
the one that works for your use-case by specifying it in your django settings as
``RATELIMIT_STRATEGY`` (one of ``fixed-window``, ``fixed-window-elastic-expiry``,
or ``moving-window``). The default configuration is ``fixed-window``.


Fixed Window
============
This is the most memory efficient strategy to use as it maintains one counter
per resource and rate limit. It does however have its drawbacks as it allows
bursts within each window - thus allowing an 'attacker' to by-pass the limits.
The effects of these bursts can be partially circumvented by enforcing multiple
granularities of windows per resource.

For example, if you specify a ``100/minute`` rate limit on a route, this strategy will
allow 100 hits in the last second of one window and a 100 more in the first
second of the next window. To ensure that such bursts are managed, you could add a second rate limit
of ``2/second`` on the same route.

Fixed Window with Elastic Expiry
================================
This strategy works almost identically to the Fixed Window strategy with the exception
that each hit results in the extension of the window. This strategy works well for
creating large penalties for breaching a rate limit.

For example, if you specify a ``100/minute`` rate limit on a route and it is being
attacked at the rate of 5 hits per second for 2 minutes - the attacker will be locked
out of the resource for an extra 60 seconds after the last hit. This strategy helps
circumvent bursts.

Moving Window
=============
.. warning:: The moving window strategy is only implemented for the ``redis`` and ``in-memory``
    storage backends. The strategy requires using a list with fast random access which
    is not very convenient to implement with a memcached storage.

This strategy is the most effective for preventing bursts from by-passing the
rate limit as the window for each limit is not fixed at the start and end of each time unit
(i.e. N/second for a moving window means N in the last 1000 milliseconds). There is
however a higher memory cost associated with this strategy as it requires ``N`` items to
be maintained in memory per resource and rate limit.

.. _ratelimit-headers:

Rate-limiting Headers
---------------------

If the configuration is enabled, information about the rate limit with respect to the
route being requested will be added to the response headers. Since multiple rate limits
can be active for a given route - the rate limit with the lowest time granularity will be
used in the scenario when the request does not breach any rate limits.

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

============================== ================================================
``X-RateLimit-Limit``          The total number of requests allowed for the
                               active window
``X-RateLimit-Remaining``      The number of requests remaining in the active
                               window.
``X-RateLimit-Reset``          UTC seconds since epoch when the window will be
                               reset.
============================== ================================================

.. warning:: Enabling the headers has an additional cost with certain storage / strategy combinations.

    * Memcached + Fixed Window: an extra key per rate limit is stored to calculate
      ``X-RateLimit-Reset``
    * Redis + Moving Window: an extra call to redis is involved during every request
      to calculate ``X-RateLimit-Remaining`` and ``X-RateLimit-Reset``

The header names can be customised if required by using django settings (:ref:`ratelimit-conf`).

