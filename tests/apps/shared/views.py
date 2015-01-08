from django.http import HttpResponse
from djlimiter import shared_limit


shared = shared_limit("2/second", "shared")

@shared
def one(_):
    return HttpResponse("one")

@shared
def two(_):
    return HttpResponse("two")

@shared
def three(_):
    return HttpResponse("three")



