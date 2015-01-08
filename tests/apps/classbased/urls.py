from django.conf.urls import patterns
from djlimiter import limit
from djlimiter import exempt
from .views import One, Three, Two

urlpatterns = patterns('',
    (r'^one/', One.as_view()),
    (r'^two/', limit("2/second")(Two.as_view())),
    (r'^three/', exempt(Three.as_view())),
)
