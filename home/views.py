from django.shortcuts import render
from django.http import HttpResponse
from .models import GalleryEntry


def index(request):
  video_objs = GalleryEntry.objects.filter(entry_type__type_name='Video')
  image_objs = GalleryEntry.objects.filter(entry_type__type_name='Image')
  presentation_objs = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
  
  context = {
    'video_objs': video_objs,
    'image_objs': image_objs,
    'presentation_objs': presentation_objs,
  }
  return render(request, 'home/index.html', context=context)


def gallery_error(message="Error!"):
  return HttpResponse(content=message, content_type='text/plain')


def gallery_view(request, gallery_item_id=None):
  if gallery_item_id == None:
    return gallery_error("Error! No `gallery_item_id` given.")

  gallery_obj = GalleryEntry.objects.get(id=gallery_item_id)
  gallery_obj_type = gallery_obj.entry_type.type_name

  if gallery_obj_type == 'Video':
    return gallery_view_video(request, gallery_obj)
  elif gallery_obj_type == 'Presentation':
    return gallery_view_presentation(request, gallery_obj)
  elif gallery_obj_type == 'Image':
    return gallery_view_image(request, gallery_obj)
  else:
    return gallery_error('Error! Type ' + gallery_obj_type + ' is not usable.')


def gallery_view_video(request, video_obj=None):
  context = {
    'video_name': video_obj.entry_name,
    'video_url': video_obj.entry_file_url,
    'video_desc': video_obj.entry_desc,
  }

  return render(request, 'home/gallery_view_video.html', context=context)
  

def gallery_view_image(request, image_obj=None):
  context = {
    'image_name': image_obj.entry_name,
    'image_url': image_obj.entry_file_url,
    'image_desc': image_obj.entry_desc,
    'image_desc_full': image_obj.entry_desc_full,
  }

  return render(request, 'home/gallery_view_image.html', context=context)


def gallery_view_presentation(request, presentation_obj=None):
  return HttpResponse(content=presentation_obj.entry_name, content_type='text/plain')


def temp(request):
	obj = GalleryEntry.objects.get(entry_name='Poroshenko')
	video = obj.entry_file_url
	print(video)
	return render(request, 'home/home.html', {'obj':video})