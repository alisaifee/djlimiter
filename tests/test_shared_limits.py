from django.test import TestCase
import mock
import djlimiter
from tests import settings


class GenericViewTests(TestCase):


    def test_shared_limits(self):
        with self.settings(
                MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ("djlimiter.Limiter",),
                RATELIMIT_GLOBAL = "1/second"
        ):
            self.assertEqual(self.client.get("/shared/one/").status_code, 200)
            self.assertEqual(self.client.get("/shared/two/").status_code, 200)
            self.assertEqual(self.client.get("/shared/three/").status_code, 429)

