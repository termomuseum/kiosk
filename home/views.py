from django.shortcuts import render
from django.http import HttpResponse
from .models import GalleryEntry


def index(request):
  content = 'Hello, Kiosk!'
  return HttpResponse(content=content, content_type='text/plain')

def temp(request):
	obj = GalleryEntry.objects.get(entry_name='Poroshenko')
	video = obj.entry_file_url
	print(video)
	return render(request, 'home/home.html', {'obj':video})