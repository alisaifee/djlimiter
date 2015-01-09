from django.conf.urls import patterns
urlpatterns = patterns('tests.apps.shared.views',
    (r'^one/', 'one'),
    (r'^two/', 'two'),
    (r'^three/', 'three'),
    (r'^four/', 'four'),
    (r'^five/', 'five'),
)
