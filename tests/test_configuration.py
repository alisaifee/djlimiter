from django.test import TestCase
import mock
import time
import djlimiter
from tests import settings


callback = mock.Mock()
callback.return_value = None

class ConfigurationTests(TestCase):


    def test_headers(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second",
                RATELIMIT_HEADERS_ENABLED = True
        ):
            start = int(time.time())
            resp = self.client.get("/basic/one/")
            self.assertEqual(resp["X-RateLimit-Limit"], '1')
            self.assertEqual(resp["X-RateLimit-Remaining"], '0')
            self.assertEqual(resp["X-RateLimit-Reset"], str(start + 1))

    def test_callback_path(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second",
                RATELIMIT_HEADERS_ENABLED = True,
                RATELIMIT_CALLBACK = "tests.test_configuration.callback"

        ):
            self.assertEqual(self.client.get("/basic/one/").status_code, 200)
            self.assertEqual(self.client.get("/basic/one/").status_code, 200)
            self.assertTrue(callback.call_count, 2)

    def test_callback_callable(self):
        cb = mock.Mock()
        cb.return_value = None
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second",
                RATELIMIT_HEADERS_ENABLED = True,
                RATELIMIT_CALLBACK = cb

        ):
            self.assertEqual(self.client.get("/basic/one/").status_code, 200)
            self.assertEqual(self.client.get("/basic/one/").status_code, 200)
            self.assertTrue(cb.call_count, 2)

    def test_callback_invalid(self):
        cb = mock.Mock()
        cb.return_value = None
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second",
                RATELIMIT_HEADERS_ENABLED = True,
                RATELIMIT_CALLBACK = "tests.test_configuration.fubar"

        ):
            with mock.patch("djlimiter.middleware.logging") as logging:
                self.assertEqual(self.client.get("/basic/one/").status_code, 200)
                self.assertEqual(self.client.get("/basic/one/").status_code, 200)
                self.assertTrue(logging.getLogger().error.call_count, 1)
