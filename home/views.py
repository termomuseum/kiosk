# from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import GalleryEntry, GalleryEntryCategory, GalleryEntryCategoryImage, GalleryEntryType
from PyPDF2 import PdfFileReader


# register = template.Library()
# @register.filter
# def get_at_index(list, index):
#   return list[index]


# Renders a main gallery page
def index(request, args=None):
  # Getting all the gallery items or entries
  # We separate them in different lists for
  # their separation in a template
  # video_objs = GalleryEntry.objects.filter(entry_type__type_name='Video')
  # image_objs = GalleryEntry.objects.filter(entry_type__type_name='Image')
  # presentation_objs = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
  categories = GalleryEntryCategory.objects.all()
  category_images = GalleryEntryCategoryImage.objects.all()

  cat_images_ordered = []

  print("\n[Begin Debug]")
  for cat in categories:
    found_img = False

    for cat_img in category_images:
      if cat_img.category == cat:
        cat_images_ordered.append("media/" + str(cat_img.category_image))
        found_img = True
        print(cat)
        print(cat_img)

    if found_img == False:
      # set to default image
      cat_images_ordered.append("/static/home/img/cat-icon.png")
      pass


  print("[End Debug]\n")

  context = {
    'categories': categories,
    'category_images': cat_images_ordered,
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

      count = 1
      ratio_px = 3000

      filename = 'media/' + presentation_obj.entry_file_url.name
      with open(filename, 'rb') as f:
        pdf = PdfFileReader(f)
        count = pdf.getNumPages()
      print("Count of PDF pages: {}".format(count))

      context = {
          'presentation_view': presentation_obj,
          'offset': int(count * ratio_px),
          }
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)
  else:
      presentation_objects = GalleryEntry.objects.filter(entry_type__type_name='Presentation')
      context = {'presentations': presentation_objects}
      # Rendering view
      return render(request, 'home/gallery_view_presentation.html', context=context)




# Editor view
def editor(request):
  debug_field = ""
  success_msg = ""
  error_msg = ""
  show_success = False
  show_error = False
  show_debug = False

  if request.method == "GET":
    debug_field += "Method: GET\n"
  elif request.method == "POST":
    debug_field += "Method: POST\n"

  editor_type = request.POST.get("ed", "None")
  debug_field += "ed: {}\n".format(editor_type)

  # Adding new category
  if editor_type == "add_cat":
    category_name = request.POST.get("cname", "None")
    editor_add_new_category(category_name)

    show_success = True
    success_msg = "Category '{}' added successfuly. \n".format(category_name)

  # Adding new entry
  if editor_type == "add_entry":
    # Getting an uploaded file
    entry_file = request.FILES['efile']
    fs = FileSystemStorage()
    filename = fs.save(entry_file.name, entry_file)
    # Getting file URL
    file_url = fs.url(filename)
    debug_field += "Filename: {}\n".format(filename)
    debug_field += "File url: {}\n".format(file_url)
    # Getting an entry data
    ename = request.POST.get("ename", "None")
    ecat_pk = int(request.POST.get("ecat", "None"))
    ecat = GalleryEntryCategory.objects.get(id=ecat_pk)
    etype_pk = int(request.POST.get("etype", "None"))
    etype = GalleryEntryType.objects.get(id=etype_pk)
    edesc = request.POST.get("edesc", "")
    efdesc = request.POST.get("efdesc", "")
    # Creating a new entry
    editor_add_new_entry(ename, etype, ecat, filename, edesc, efdesc)

    show_success = True
    success_msg = "Entry '{}' added to category '{}' successfuly.\n".format(ename, ecat.category_name)


  context = {
    "show_debug": show_debug,
    "debug_field": debug_field,

    "show_success_msg": show_success,
    "success_msg": success_msg,

    "show_error": show_error,
    "error_msg": error_msg,

    "categories": GalleryEntryCategory.objects.all(),
    "entry_types": GalleryEntryType.objects.all(),
  }

  return render(request, 'home/gallery_editor.html', context=context)


def editor_add_new_category(cname):
  GalleryEntryCategory.objects.create(category_name=cname)


def editor_add_new_entry(ename, etype, ecat, efile_url, edesc, efdesc):
  GalleryEntry.objects.create(
    entry_name=ename,
    entry_type=etype,
    entry_category=ecat,
    entry_file_url=efile_url,
    entry_desc=edesc,
    entry_desc_full=efdesc
    )
