from django.shortcuts import render
from django.http import HttpResponse
from .models import GalleryEntry, GalleryEntryCategory


# Renders a main gallery page
def index(request, args=None):
  # Getting all the gallery items or entries
  # We separate them in different lists for 
  # their separation in a template
  # video_objs = GalleryEntry.objects.filter(entry_type__type_name='Video')
  # image_objs = GalleryEntry.objects.filter(entry_type__type_name='Image')
  # presentation_objs = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
  categories = GalleryEntryCategory.objects.all()

  context = {
    'categories': categories,
    # 'video_objs': video_objs,
    # 'image_objs': image_objs,
    # 'presentation_objs': presentation_objs,
  }
  # Rendering view
  return render(request, 'home/index.html', context=context)


# Category View
def gallery_category(request, pk=None):
  if pk == None:
    print("No pk was given :(")
    return index(request) 
  
  category = GalleryEntryCategory.objects.get(id=pk)
  video_objects = GalleryEntry.objects.filter(entry_category=category).filter(entry_type__type_name='Video')
  image_objects = GalleryEntry.objects.filter(entry_category=category).filter(entry_type__type_name='Image')
  presentation_objects = GalleryEntry.objects.filter(entry_category=category).filter(entry_type__type_name='Presentation')

  context = {
        "category_name": category.category_name,
        "video_objects": video_objects,
        "video_len": len(video_objects),
        "image_objects": image_objects,
        "image_len": len(image_objects),
        "presentation_objects": presentation_objects,
        "presentation_len": len(presentation_objects),
      }
  return render(request, 'home/gallery.html', context=context)



# Video gallery view
def gallery_video(request, pk=None):
  if pk != None:
      video_obj = GalleryEntry.objects.get(id=pk)
      context = {'video_view': video_obj.entry_file_url}
      # Rendering view
      return render(request, 'home/gallery_view_video.html', context=context)
  else:
      video_objects = GalleryEntry.objects.filter(entry_type__type_name='Video')
      context = {'videos': video_objects}
      print(context)
      # Rendering view
      return render(request, 'home/gallery_view_video.html', context=context)

  

# Image gallery view
def gallery_image(request, pk=None):
  if pk!=None:
      image_obj = GalleryEntry.objects.get(id=pk)
      context = {'image_view': image_obj}
      # Rendering view
      return render(request, 'home/gallery_view_image.html', context=context)
  else:
      image_objects = GalleryEntry.objects.filter(entry_type__type_name='Image')
      context = {'images': image_objects}
      # Rendering view
      return render(request, 'home/gallery_view_image.html', context=context)


# Presentation gallery view
def gallery_presentation(request, pk=None):
  if pk!=None:
      presentation_obj = GalleryEntry.objects.get(id=pk)
      context = {'presentation_view': presentation_obj}
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)
  else:
      presentation_objects = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
      context = {'presentations': presentation_objects}
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)

