from django.shortcuts import render
from django.http import HttpResponse


def index(request):
  content = 'Hello, Kiosk! :)'
  return HttpResponse(content=content, content_type='text/plain')


def view_image(request):
  # return ...
  pass


def view_video(request):
  # return ...
  pass


def view_presentation(request):
  # return ...
  pass


def temp(request):
	return render(request, 'home/home.html')
