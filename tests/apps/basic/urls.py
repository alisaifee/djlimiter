from django.conf.urls import patterns
urlpatterns = patterns('tests.apps.basic.views',
    (r'^one/', 'one'),
    (r'^two/', 'two'),
    (r'^three/', 'three'),
    (r'^four/', 'four'),
)
