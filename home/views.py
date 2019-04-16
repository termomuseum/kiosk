from django.shortcuts import render
from django.http import HttpResponse
from .models import GalleryEntry


def index(request):
  content = 'Hello, Kiosk!'
  return HttpResponse(content=content, content_type='text/plain')


def gallery_error(message="Error!"):
  return HttpResponse(content=message, content_type='text/plain')


def gallery_view_video(request, gallery_item_id=None):
  if gallery_item_id == None:
    return gallery_error("Error! No `gallery_item_id` given.")

  video_obj = GalleryEntry.objects.get(id=gallery_item_id)

  context = {
    'video_name': video_obj.entry_name,
    'video_url': video_obj.entry_file_url,
  }

  return render(request, 'home/gallery_view_video.html', context=context)
  


def gallery_view_image(request, gallery_item_id=None):
  pass


def gallery_view_presentation(request, gallery_item_id=None):
  pass


def temp(request):
	obj = GalleryEntry.objects.get(entry_name='Poroshenko')
	video = obj.entry_file_url
	print(video)
	return render(request, 'home/home.html', {'obj':video})