from django.conf.urls import patterns
from django.views.generic import TemplateView
from djlimiter import limit, exempt

urlpatterns = patterns('',
    (r'^template/', TemplateView.as_view(template_name="generic/template.html")),
    (r'^template-limited/', limit("2/second")(TemplateView.as_view(template_name="generic/template.html"))),
    (r'^template-exempt/', exempt(TemplateView.as_view(template_name="generic/template.html"))),
)
