from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # SOME LOGIC HERE
    print(f'This is my amazing update!')
    return HttpResponse('Hello world!')

