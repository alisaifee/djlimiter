from django.conf.urls import patterns
urlpatterns = patterns('tests.apps.simple.views',
    (r'^one/', 'one'),
    (r'^two/', 'two'),
    (r'^three/', 'three'),
)
