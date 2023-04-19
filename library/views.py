from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # SOME LOGIC HERE
    return HttpResponse('Hello world!')

