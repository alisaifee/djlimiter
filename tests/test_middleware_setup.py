from django.test import TestCase
import mock
import djlimiter
from tests import settings


class MiddlewareSetupTests(TestCase):


    def test_middleware_installed(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "2/second"
        ):
            with mock.patch("djlimiter.Limiter", wraps = djlimiter.Limiter) as limiter:
                self.assertEqual(self.client.get("/simple/one/").status_code, 200)
                self.assertEqual(limiter.call_count, 1)

    def test_middleware_initialized(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "2/second",
        ):
            with mock.patch("djlimiter.Limiter", wraps = djlimiter.Limiter) as limiter:
                limiter.return_value = mock.Mock(wraps=djlimiter.Limiter())
                self.assertEqual(self.client.get("/simple/two/").status_code, 200)
                self.assertEqual(self.client.get("/simple/two/").status_code, 200)
                self.assertEqual(limiter().process_request.call_count, 2)
                self.assertEqual(self.client.get("/simple/two/").status_code, 429)
                self.assertEqual(limiter().process_request.call_count, 3)
