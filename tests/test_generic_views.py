from django.test import TestCase
import mock
import djlimiter
from tests import settings


class GenericViewTests(TestCase):


    def test_template_view_global_limits(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/generic/template/").status_code, 200)
            self.assertEqual(self.client.get("/generic/template/").status_code, 429)

    def test_template_view_specific_limit(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/generic/template-limited/").status_code, 200)
            self.assertEqual(self.client.get("/generic/template-limited/").status_code, 200)
            self.assertEqual(self.client.get("/generic/template-limited/").status_code, 429)

    def test_template_view_exempt(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/generic/template-exempt/").status_code, 200)
            self.assertEqual(self.client.get("/generic/template-exempt/").status_code, 200)
            self.assertEqual(self.client.get("/generic/template-exempt/").status_code, 200)
