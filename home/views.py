from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  content = 'Hello, Kiosk!'
  return HttpResponse(content=content, content_type='text/plain')