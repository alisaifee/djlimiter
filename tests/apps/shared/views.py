from django.http import HttpResponse
from djlimiter import shared_limit

def func(_):
    return "4/second; 5/hour"

shared = shared_limit("2/second", "shared")
shared_dynamic = shared_limit(func, "shared_dynamic")
@shared
def one(_):
    return HttpResponse("one")

@shared
def two(_):
    return HttpResponse("two")

@shared
def three(_):
    return HttpResponse("three")

@shared_dynamic
def four(_):
    return HttpResponse("four")

@shared
@shared_dynamic
def five(_):
    return HttpResponse("five")

