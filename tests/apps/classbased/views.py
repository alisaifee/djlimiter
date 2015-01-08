from django.http import HttpResponse
from django.views.generic import View
from djlimiter import limit, exempt


class One(View):
    def get(self, request):
        return HttpResponse('one')

class Two(View):
    def get(self, request):
        return HttpResponse('two')

class Three(View):
    def get(self, request):
        return HttpResponse('three')
