# coding: utf-8
from django.http import HttpResponse
from django.views import generic


class HomeView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('200 ;)', status=200)
