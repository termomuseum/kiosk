from django.shortcuts import render
from django.http import HttpResponse
from .models import GalleryEntry


# Renders a main gallery page
def index(request, args=None):
  # Getting all the gallery items or entries
  # We separate them in different lists for 
  # their separation in a template
  video_objs = GalleryEntry.objects.filter(entry_type__type_name='Video')
  image_objs = GalleryEntry.objects.filter(entry_type__type_name='Image')
  presentation_objs = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
  
  context = {
    'video_objs': video_objs,
    'image_objs': image_objs,
    'presentation_objs': presentation_objs,
  }
  # Rendering view
  return render(request, 'home/index.html', context=context)


# Display an error when something's not right
def gallery_error(message="Error!"):
  return HttpResponse(content=message, content_type='text/plain')


# Main gallery view function, to view gallery items
# Directs to three other views depending on a entry type
# (Image, Video or Presentation)
def gallery_view(request, gallery_item_id=None):
  if gallery_item_id == None:
    return gallery_error("Error! No `gallery_item_id` given.")

  # Getting selected gallery object and its type
  gallery_obj = GalleryEntry.objects.get(id=gallery_item_id)
  gallery_obj_type = gallery_obj.entry_type.type_name

  # Directing to another view depending on the type
  if gallery_obj_type == 'Video':
    return gallery_view_video(request, gallery_obj)
  elif gallery_obj_type == 'Presentation':
    return gallery_view_presentation(request, gallery_obj)
  elif gallery_obj_type == 'Image':
    return gallery_view_image(request, gallery_obj)
  else:
    # If there was other unexpected type, we throw an error
    return gallery_error('Error! Type ' + gallery_obj_type + ' is not usable.')


# Video gallery view
def gallery_video(request, pk=None):
  if pk!=None:
      video_obj = GalleryEntry.objects.get(id=pk)
      context = {'video_view':video_obj.entry_file_url}
      # Rendering view
      return render(request, 'home/gallery_view_video.html', context=context)
  else:
      objects = GalleryEntry.objects.filter(entry_type__type_name='Video')
      context =  {'videos':objects}
      print(context)
      # Rendering view
      return render(request, 'home/gallery_view_video.html', context=context)

  

# Image gallery view
def gallery_image(request, pk=None):
  if pk!=None:
      image_obj = GalleryEntry.objects.get(id=pk)
      context = {'image_view':image_obj}
      # Rendering view
      return render(request, 'home/gallery_view_image.html', context=context)
  else:
      objects = GalleryEntry.objects.filter(entry_type__type_name='Image')
      context = {'images':objects}
      # Rendering view
      return render(request, 'home/gallery_view_image.html', context=context)


# Presentation gallery view
def gallery_presentation(request, pk=None):
  if pk!=None:
      presentation_obj = GalleryEntry.objects.get(id=pk)
      context = {'presentation_view':presentation_obj}
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)
  else:
      objects = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
      context = {'presentations':objects}
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)

