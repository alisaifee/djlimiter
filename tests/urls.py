from django.conf.urls import patterns, include

urlpatterns = patterns('',
   (r'^simple/', include('tests.apps.simple.urls')),
)

