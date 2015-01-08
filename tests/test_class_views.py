from django.test import TestCase

from tests import settings


class ClassViewTests(TestCase):


    def test_class_views_global(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/classbased/one/").status_code, 200)
            self.assertEqual(self.client.get("/classbased/one/").status_code, 429)

    def test_class_views_limited(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/classbased/two/").status_code, 200)
            self.assertEqual(self.client.get("/classbased/two/").status_code, 200)
            self.assertEqual(self.client.get("/classbased/two/").status_code, 429)

    def test_class_views_exempt(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/classbased/three/").status_code, 200)
            self.assertEqual(self.client.get("/classbased/three/").status_code, 200)
