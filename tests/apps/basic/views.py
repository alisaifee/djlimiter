from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from djlimiter.decorators import limit


def one(_):
    return HttpResponse("one")

def two(_):
    return HttpResponse("two")

@limit("1/second")
@require_http_methods(["GET"])
def three(_):
    return HttpResponse("three")
