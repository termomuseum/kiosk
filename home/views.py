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
def gallery_view_video(request, video_obj=None):
  context = {
    'video_name': video_obj.entry_name,
    'video_url': video_obj.entry_file_url,
    'video_desc': video_obj.entry_desc,
  }
  # Rendering view
  return render(request, 'home/gallery_view_video.html', context=context)
  

# Image gallery view
def gallery_view_image(request, image_obj=None):
  context = {
    'image_name': image_obj.entry_name,
    'image_url': image_obj.entry_file_url,
    'image_desc': image_obj.entry_desc,
    'image_desc_full': image_obj.entry_desc_full,
  }
  # Rendering view
  return render(request, 'home/gallery_view_image.html', context=context)


# Presentation gallery view
def gallery_view_presentation(request, presentation_obj=None):
  context = {
    'presentation_name':presentation_obj.entry_name,
    'presentation_url':presentation_obj.entry_file_url,
    'presentation_desc':presentation_obj.entry_desc,
    'presentation_desc_full':presentation_obj.entry_desc_full,
  }
  # Rendering view
  return render(request, 'home/gallery_view_presentation.html', context=context)

