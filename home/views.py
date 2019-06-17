from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import GalleryEntry, GalleryEntryCategory, GalleryEntryCategoryImage, GalleryEntryType
from PyPDF2 import PdfFileReader



# Renders a main gallery page
def index(request, args=None):
  # Gettina all the categories and category images
  categories = GalleryEntryCategory.objects.all()
  category_images = GalleryEntryCategoryImage.objects.all()
  # Ordered category images list
  cat_images_ordered = []

  # looping through all the categories and images
  for cat in categories:
    found_img = False

    # Finding a category image
    for cat_img in category_images:
      if cat_img.category == cat:
        cat_images_ordered.append("media/" + str(cat_img.category_image))
        found_img = True
    
    # if category image is not found, set it to default icon
    if found_img == False:
      cat_images_ordered.append("/static/home/img/cat-icon.png")
      pass

  context = {
    'categories': categories,
    'category_images': cat_images_ordered,
  }
  # Rendering view
  return render(request, 'home/index.html', context=context)



# Category View
def gallery_category(request, pk=None):
  if pk == None:
    print("No pk was given :(")
    return index(request)

  # Getting all of the objects in a category
  category = GalleryEntryCategory.objects.get(id=pk)
  video_objects = GalleryEntry.objects.filter(
      entry_category=category).filter(
          entry_type__type_name='Video')
  image_objects = GalleryEntry.objects.filter(
      entry_category=category).filter(
          entry_type__type_name='Image')
  presentation_objects = GalleryEntry.objects.filter(
      entry_category=category).filter(
          entry_type__type_name='Presentation')

  context = {
        "category_name": category.category_name,
        "video_objects": video_objects,
        "video_len": len(video_objects),
        "image_objects": image_objects,
        "image_len": len(image_objects),
        "presentation_objects": presentation_objects,
        "presentation_len": len(presentation_objects),
      }
  # Rendering gallery view
  return render(request, 'home/gallery.html', context=context)



# Video gallery view
def gallery_video(request, pk=None):
  # if pk != None:
    # Getting a video object to display
    # video_obj = GalleryEntry.objects.get(id=pk)
    # context = {'video_view': video_obj.entry_file_url}
    # Rendering view
    # return render(request, 'home/gallery_view_video.html', context=context)
  # else:
    # Getting all of the video objects, to display all of them
    # video_objects = GalleryEntry.objects.filter(entry_type__type_name='Video')
    # context = {'videos': video_objects}
    # Rendering view
    # return render(request, 'home/gallery_view_video.html', context=context)
  
  # Getting a video object to display
  video_obj = GalleryEntry.objects.get(id=pk)
  context = {'video_view': video_obj.entry_file_url}
  # Rendering view
  return render(request, 'home/gallery_view_video.html', context=context)



# Image gallery view
def gallery_image(request, pk=None):
  # Getting an image object to display 
  image_obj = GalleryEntry.objects.get(id=pk)
  context = {'image_view': image_obj}
  # Rendering view
  return render(request, 'home/gallery_view_image.html', context=context)



# Presentation gallery view
def gallery_presentation(request, pk=None):
  # Getting a presentation object
  presentation_obj = GalleryEntry.objects.get(id=pk)
  count = 1        # count of pages in a PDF file
  ratio_px = 3000  # how many pixels of height do we add per page

  # getting a PDF file
  filename = 'media/' + presentation_obj.entry_file_url.name
  # getting count of pages in a PDF file
  with open(filename, 'rb') as f:
    pdf = PdfFileReader(f)
    count = pdf.getNumPages()

  context = {
    'presentation_view': presentation_obj,
    'offset': int(count * ratio_px),
  }
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
    try:
      # getting category name and create it
      category_name = request.POST.get("cname", "None")
      editor_add_new_category(category_name)

      show_success = True
      success_msg = "Category '{}' added successfuly. \n".format(category_name)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Adding new entry
  if editor_type == "add_entry":
    try:
      # Getting an uploaded file
      entry_file = request.FILES['efile']
      fs = FileSystemStorage()
      filename = fs.save(entry_file.name, entry_file)
      # Getting file URL
      file_url = fs.url(filename)
      # Getting an entry data
      ename = request.POST.get("ename", "None")
      ecat_pk = int(request.POST.get("ecat", 0))
      ecat = GalleryEntryCategory.objects.get(id=ecat_pk)
      etype_pk = int(request.POST.get("etype", 0))
      etype = GalleryEntryType.objects.get(id=etype_pk)
      edesc = request.POST.get("edesc", "")
      efdesc = request.POST.get("efdesc", "")
      # Creating a new entry
      editor_add_new_entry(ename, etype, ecat, filename, edesc, efdesc)

      show_success = True
      success_msg = "Entry '{}' added to category '{}' successfuly.\n".format(ename, ecat.category_name)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Edit category name
  if editor_type == "edit_cat":
    try:
      # getting category pk
      cat_pk = int(request.POST.get("cat", 0))
      cat = GalleryEntryCategory.objects.get(id=cat_pk)
      # editing category name and saving it
      orig_cat_name = cat.category_name
      cat.category_name = request.POST.get("cat-name", "None")
      cat.save()
    
      show_success = True
      success_msg = "Changed '{}' to '{}'.".format(orig_cat_name, cat.category_name)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Edit entry
  ##-> Firsly, the category needs to be chosen
  ##-> Then the entry within the category
  ##-> Then the entry is edited
  ##-> Selecting category
  if editor_type == "edit_entry_select_cat":
    try:
      # Getting selected category pk, to find an entry in it
      selected_cat_pk = int(request.POST.get("cat", 0))
      if selected_cat_pk >= 0:
        # getting the category
        selected_cat = GalleryEntryCategory.objects.get(id=selected_cat_pk)
        # getting edit mode
        mode = request.POST.get("mode", "edit")
        c = { 
          # Getting all the entries of a category
          "entries": GalleryEntry.objects.filter(entry_category=selected_cat), 
          "mode": mode,
        }
        return render(request, 'home/gallery_editor_select_entry.html', context=c)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Selecting entry to edit 
  if editor_type == "edit_entry_select_entry":
    try:
      # getting selected entry pk
      selected_entry_pk = int(request.POST.get("entry_pk",0))
      selected_entry = GalleryEntry.objects.get(id=selected_entry_pk)
      # getting edit mode
      mode = request.POST.get("mode", "edit")
      # get data for context
      context = {
        "mode": mode,
        "epk": selected_entry_pk,
        "ename": selected_entry.entry_name,
        "ecat": selected_entry.entry_category.pk,
        "edesc": selected_entry.entry_desc,
        "efdesc": selected_entry.entry_desc_full,
        "categories": GalleryEntryCategory.objects.all(),
      }
      # render edit or delete page depending on context.mode
      return render(request, 'home/gallery_editor_edit_entry.html', context=context)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  
  # Saving entry edit
  if editor_type == "edit_entry_save_entry":
    try:
      # getting original entry pk
      entry_pk = request.POST.get("epk")
      # getting new entry values
      new_entry_name = request.POST.get("ename")
      new_entry_cat_pk = int(request.POST.get("ecat"))
      new_entry_cat = GalleryEntryCategory.objects.get(id=new_entry_cat_pk)
      new_entry_desc = request.POST.get("edesc")
      new_entry_desc_full = request.POST.get("efdesc")
      # overwriting old values with new ones
      entry = GalleryEntry.objects.get(id=entry_pk)
      entry.entry_name = new_entry_name
      entry.entry_category = new_entry_cat
      entry.entry_desc = new_entry_desc
      entry.entry_desc_full = new_entry_desc_full
      # saving an entry
      entry.save()

      show_success = True
      success_msg = "Entry edited successfuly."
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Deleting entry
  if editor_type == "edit_entry_delete_entry":
    try:
      # Getting entry pk and deleting it
      entry_pk = request.POST.get("epk")
      entry = GalleryEntry.objects.get(id=entry_pk)
      entry.delete()
    
      show_success = True
      success_msg = "Entry deleted successfuly."
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Delete category and all of its content
  if editor_type == "edit_entry_delete_cat":
    try:
      # Getting category pk
      selected_cat_pk = int(request.POST.get("cat", 0))
      if selected_cat_pk >= 0:
        selected_cat = GalleryEntryCategory.objects.get(id=selected_cat_pk)
        category_name = selected_cat.category_name
        category_pk = selected_cat.pk
        c = {
          "cname": category_name,
          "cpk": category_pk,
        }
        # Rendering category delete confirmation page
        return render(request, "home/gallery_editor_confirm_delete_cat.html", context=c)
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Confirming category delete
  if editor_type == "edit_confirm_delete_cat":
    try:
      # Getting category and all entries in it
      selected_cat_pk = int(request.POST.get("cpk", 0))
      selected_cat = GalleryEntryCategory.objects.get(id=selected_cat_pk)
      entries = GalleryEntry.objects.filter(entry_category=selected_cat),
      # Deleting category and entries
      selected_cat.delete()
      for e in entries:
        e.delete()
      
      show_success = True
      success_msg = "Category deleted successfuly."
    except Exception as e:
      show_error = True
      error_msg = "ERROR!"

  # Cancel something.
  if editor_type == "cancel":
    pass

  # Render context
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
  # Rendering editor html
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
